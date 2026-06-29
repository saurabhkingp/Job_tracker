from fastlite import database
import datetime
import hashlib

# Setup SQLite Database and Models via fastlite
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
