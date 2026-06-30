import os
import datetime
import hashlib
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    
    class PostgresTable:
        def __init__(self, db_conn, table_name):
            self.conn = db_conn
            self.table_name = table_name
            self.dataclass_type = None

        def create(self, **kwargs):
            pk_col = kwargs.pop('pk', 'id')
            cols = []
            for col_name, col_type in kwargs.items():
                if col_name == pk_col:
                    cols.append(f"{col_name} SERIAL PRIMARY KEY")
                elif col_type == int:
                    cols.append(f"{col_name} INTEGER")
                elif col_type == str:
                    cols.append(f"{col_name} TEXT")
                else:
                    cols.append(f"{col_name} TEXT")
            
            cols_str = ", ".join(cols)
            query = f"CREATE TABLE IF NOT EXISTS {self.table_name} ({cols_str});"
            with self.conn.cursor() as cur:
                cur.execute(query)

        @property
        def columns_dict(self):
            query = "SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name = %s;"
            with self.conn.cursor() as cur:
                cur.execute(query, (self.table_name,))
                rows = cur.fetchall()
                return {r[0]: True for r in rows}

        def add_column(self, col_name, col_type):
            type_str = "INTEGER" if col_type == int else "TEXT"
            query = f"ALTER TABLE {self.table_name} ADD COLUMN {col_name} {type_str};"
            with self.conn.cursor() as cur:
                cur.execute(query)

        def dataclass(self):
            table_name = self.table_name
            class DynamicModel(dict):
                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                def __getattr__(self, name):
                    if name in self:
                        return self[name]
                    if name in ('id', 'user_id', 'company', 'title', 'status', 'date_applied', 'url', 'notes', 'username', 'password'):
                        return None
                    raise AttributeError(f"'{table_name}' object has no attribute '{name}'")
                def __setattr__(self, name, value):
                    self[name] = value
                def get(self, key, default=None):
                    return super().get(key, default)
            
            self.dataclass_type = DynamicModel
            return DynamicModel

        def insert(self, obj):
            data = obj if isinstance(obj, dict) else obj.__dict__
            # Skip 'id' since it's serial autoincrement
            data_to_insert = {k: v for k, v in data.items() if k != 'id'}
            
            cols = ", ".join(data_to_insert.keys())
            placeholders = ", ".join(["%s"] * len(data_to_insert))
            query = f"INSERT INTO {self.table_name} ({cols}) VALUES ({placeholders}) RETURNING id;"
            
            with self.conn.cursor() as cur:
                cur.execute(query, list(data_to_insert.values()))
                inserted_id = cur.fetchone()[0]
                if not isinstance(obj, dict):
                    obj.id = inserted_id
                return obj

        def update(self, obj):
            data = obj if isinstance(obj, dict) else obj.__dict__
            id_val = data.get('id')
            if id_val is None:
                raise ValueError("Update requires an id field.")
            
            set_cols = []
            vals = []
            for k, v in data.items():
                if k != 'id':
                    set_cols.append(f"{k} = %s")
                    vals.append(v)
            vals.append(id_val)
            
            query = f"UPDATE {self.table_name} SET {', '.join(set_cols)} WHERE id = %s;"
            with self.conn.cursor() as cur:
                cur.execute(query, vals)

        def delete(self, id_val):
            query = f"DELETE FROM {self.table_name} WHERE id = %s;"
            with self.conn.cursor() as cur:
                cur.execute(query, (id_val,))

        def rows_where(self, where_clause, where_args=None):
            if where_args is None:
                where_args = []
            where_clause = where_clause.replace('?', '%s')
            query = f"SELECT * FROM {self.table_name} WHERE {where_clause};"
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, where_args)
                rows = cur.fetchall()
                if self.dataclass_type:
                    return [self.dataclass_type(**r) for r in rows]
                return rows

        def count_where(self, where_clause, where_args=None):
            if where_args is None:
                where_args = []
            where_clause = where_clause.replace('?', '%s')
            query = f"SELECT COUNT(*) FROM {self.table_name} WHERE {where_clause};"
            with self.conn.cursor() as cur:
                cur.execute(query, where_args)
                count = cur.fetchone()[0]
                return count

        @property
        def count(self):
            query = f"SELECT COUNT(*) FROM {self.table_name};"
            with self.conn.cursor() as cur:
                cur.execute(query)
                count = cur.fetchone()[0]
                return count

        def __getitem__(self, item):
            query = f"SELECT * FROM {self.table_name} WHERE id = %s;"
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, (item,))
                row = cur.fetchone()
                if row is None:
                    raise KeyError(f"No row with id {item}")
                if self.dataclass_type:
                    return self.dataclass_type(**row)
                return row

        def __call__(self, where=None, where_args=None):
            if where is None:
                query = f"SELECT * FROM {self.table_name};"
                where_args = []
            else:
                where = where.replace('?', '%s')
                query = f"SELECT * FROM {self.table_name} WHERE {where};"
            
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, where_args or [])
                rows = cur.fetchall()
                if self.dataclass_type:
                    return [self.dataclass_type(**r) for r in rows]
                return rows

    class PostgresDatabase:
        def __init__(self, conn_url):
            self.conn = psycopg2.connect(conn_url)
            self.conn.autocommit = True
            
            # Map of table instances
            self.tables = {}

            class TableAccessor:
                def __init__(self, db_instance):
                    self.db_instance = db_instance
                def __getattr__(self, name):
                    if name not in self.db_instance.tables:
                        self.db_instance.tables[name] = PostgresTable(self.db_instance.conn, name)
                    return self.db_instance.tables[name]
                def __contains__(self, name):
                    query = "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_schema = 'public' AND table_name = %s);"
                    with self.db_instance.conn.cursor() as cur:
                        cur.execute(query, (name,))
                        return cur.fetchone()[0]
            
            self.t = TableAccessor(self)

    db = PostgresDatabase(DATABASE_URL)
else:
    from fastlite import database
    db = database('jobs.db')

# Setup Users table
users = db.t.users
if 'users' not in db.t:
    users.create(
        id=int,
        username=str,
        password=str, # Hashed password
        pk='id'
    )
User = users.dataclass()

# Setup Jobs table
jobs = db.t.jobs
if 'jobs' not in db.t:
    jobs.create(
        id=int,
        user_id=int,
        company=str,
        title=str,
        status=str,        # 'Wishlist', 'Applied', 'Interviewing', 'Offer', 'Rejected'
        date_applied=str,  # 'YYYY-MM-DD'
        url=str,
        notes=str,
        pk='id'
    )
else:
    # Migration: Add user_id column if it doesn't exist in existing jobs table
    if 'user_id' not in jobs.columns_dict:
        jobs.add_column('user_id', int)

# Map to dynamic dataclass for inserts and updates
Job = jobs.dataclass()


# Database Seeding Logic per User
def seed_jobs_for_user(user_id):
    sample_jobs = [
        {
            "user_id": user_id,
            "company": "Google",
            "title": "Senior Software Engineer",
            "status": "Wishlist",
            "date_applied": "",
            "url": "https://careers.google.com",
            "notes": "Discussed role with recruiter on LinkedIn. Need to practice algorithms."
        },
        {
            "user_id": user_id,
            "company": "Stripe",
            "title": "Backend Engineer",
            "status": "Applied",
            "date_applied": (datetime.date.today() - datetime.timedelta(days=4)).isoformat(),
            "url": "https://stripe.com/jobs",
            "notes": "Applied with recruiter referral. Checked portal: Application under review."
        },
        {
            "user_id": user_id,
            "company": "Meta",
            "title": "Production Engineer",
            "status": "Interviewing",
            "date_applied": (datetime.date.today() - datetime.timedelta(days=10)).isoformat(),
            "url": "https://metacareers.com",
            "notes": "Passed phone screening! Technical onsite scheduled for next Thursday."
        },
        {
            "user_id": user_id,
            "company": "Netflix",
            "title": "Senior Product Designer",
            "status": "Offer",
            "date_applied": (datetime.date.today() - datetime.timedelta(days=15)).isoformat(),
            "url": "https://netflix.com/jobs",
            "notes": "Onsite completed. Received offer letter! Reviewing compensation package."
        },
        {
            "user_id": user_id,
            "company": "Amazon",
            "title": "Cloud Architect",
            "status": "Rejected",
            "date_applied": (datetime.date.today() - datetime.timedelta(days=22)).isoformat(),
            "url": "https://amazon.jobs",
            "notes": "Passed loop but rejected on system design alignment. Reapply in 1 year."
        }
    ]
    for j in sample_jobs:
        jobs.insert(Job(**j))


# Password hashing helper
def hash_password(pwd):
    return hashlib.sha256(pwd.encode()).hexdigest()
