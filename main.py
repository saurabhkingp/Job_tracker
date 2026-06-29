from fasthtml.common import *
from fastlite import database
import pandas as pd
import datetime
import hashlib
from starlette.responses import Response

# 1. Session Authentication Middleware & Beforeware Setup
login_redir = RedirectResponse('/login', status_code=303)

def before_auth(req, sess):
    auth = req.scope['auth'] = sess.get('auth', None)
    path = req.scope['path']
    # Allow login, signup, logout, static files, and favicon to bypass authentication
    if not auth and path not in ('/login', '/signup', '/logout') and not path.startswith('/static'):
        return login_redir

bware = Beforeware(before_auth, skip=[r'/login', r'/signup', r'/logout', r'/static/.*', r'/favicon\.ico'])

# Initialize FastHTML App with Beforeware and Session configuration
app, rt = fast_app(
    pico=False,
    before=bware,
    hdrs=(
        # Tailwind CSS CDN
        Script(src="https://cdn.tailwindcss.com"),
        # SortableJS CDN for Kanban drag-and-drop
        Script(src="https://cdnjs.cloudflare.com/ajax/libs/Sortable/1.15.2/Sortable.min.js"),
        # Custom Tailwind Configuration
        Script("""
            tailwind.config = {
                theme: {
                    extend: {
                        fontFamily: {
                            sans: ['Inter', 'sans-serif'],
                        }
                    }
                }
            }
        """),
        # Inter Google Font
        Link(rel="stylesheet", href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap"),
        # Styling for scrollbars, dialog backdrops, and Sortable drag states
        Style("""
            /* Custom Scrollbar Styles */
            ::-webkit-scrollbar {
                width: 6px;
                height: 6px;
            }
            ::-webkit-scrollbar-track {
                background: #090d16;
            }
            ::-webkit-scrollbar-thumb {
                background: #1e293b;
                border-radius: 4px;
            }
            ::-webkit-scrollbar-thumb:hover {
                background: #334155;
            }
            /* SortableJS drag effects */
            .sortable-ghost {
                opacity: 0.35;
                border: 2px dashed #3b82f6 !important;
                background-color: rgb(30 58 138 / 0.2) !important;
            }
            .sortable-chosen {
                transform: rotate(-1deg);
                box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.6);
            }
            /* Native dialog backdrop blur */
            dialog::backdrop {
                background-color: rgba(2, 6, 23, 0.7);
                backdrop-filter: blur(4px);
            }
        """)
    )
)

# 2. Setup SQLite Database and Models via fastlite
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


# 3. Database Seeding Logic per User
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


# 4. Helper Functions & Safe HTML SVGs
SafeHtml = NotStr

def briefcase_svg():
    return SafeHtml("""
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-briefcase text-blue-500"><path d="M16 20V4a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/><rect width="20" height="14" x="2" y="6" rx="2"/></svg>
    """)

def search_svg():
    return SafeHtml("""
    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-search absolute left-3.5 top-3 text-slate-500"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
    """)

def edit_svg():
    return SafeHtml("""
    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-pencil"><path d="M12 20h9"/><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4Z"/></svg>
    """)

def trash_svg():
    return SafeHtml("""
    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-trash-2"><path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/><line x1="10" x2="10" y1="11" y2="17"/><line x1="14" x2="14" y1="11" y2="17"/></svg>
    """)

def calendar_svg():
    return SafeHtml("""
    <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-calendar mr-1.5"><path d="M8 2v4"/><path d="M16 2v4"/><rect width="18" height="18" x="3" y="4" rx="2"/><path d="M3 10h18"/></svg>
    """)

def external_link_svg():
    return SafeHtml("""
    <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-external-link mr-1.5"><path d="M15 3h6v6"/><path d="M10 14 21 3"/><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/></svg>
    """)

def close_svg():
    return SafeHtml("""
    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-x"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
    """)

def download_svg():
    return SafeHtml("""
    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-download mr-1.5"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" x2="12" y1="15" y2="3"/></svg>
    """)

def markdown_svg():
    return SafeHtml("""
    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-file-text mr-1.5"><path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M10 9H8"/><path d="M16 13H8"/><path d="M16 17H8"/></svg>
    """)

def log_out_svg():
    return SafeHtml("""
    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-log-out mr-1.5"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" x2="9" y1="12" y2="12"/></svg>
    """)

def eye_on_svg():
    return """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-eye"><path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/></svg>"""

def eye_off_svg():
    return """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-eye-off"><path d="M9.88 9.88a3 3 0 1 0 4.24 4.24"/><path d="M10.73 5.08A10.43 10.43 0 0 1 12 5c7 0 10 7 10 7a13.16 13.16 0 0 1-1.67 2.68"/><path d="M6.61 6.61A13.52 13.52 0 0 0 2 12s3 7 10 7a9.74 9.74 0 0 0 5.39-1.61"/><line x1="2" x2="22" y1="2" y2="22"/></svg>"""

def get_count_badge_class(status):
    colors = {
        'Wishlist': 'bg-slate-500/20 text-slate-300 border-slate-500/30',
        'Applied': 'bg-blue-500/20 text-blue-300 border-blue-500/30',
        'Interviewing': 'bg-amber-500/20 text-amber-300 border-amber-500/30',
        'Offer': 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30',
        'Rejected': 'bg-rose-500/20 text-rose-300 border-rose-500/30'
    }
    color_class = colors.get(status, 'bg-slate-500/20 text-slate-300')
    return f"px-2.5 py-0.5 rounded-full text-xs font-semibold border {color_class}"


# 5. UI Layout Components
def column_header(status, count):
    return Div(
        Div(
            Span(status, cls="font-bold text-white text-sm tracking-wider uppercase"),
            Span(
                str(count),
                id=f"count-{status}",
                cls=get_count_badge_class(status)
            ),
            cls="flex justify-between items-center"
        ),
        cls="pb-3 border-b border-slate-800/80 mb-4"
    )

def job_card(job):
    return Div(
        Div(
            Div(
                Span(job.company, cls="text-xs font-semibold uppercase tracking-wider text-slate-400"),
                Div(
                    Button(
                        edit_svg(),
                        hx_get=f"/job/{job.id}/edit",
                        hx_target="#modal-content",
                        hx_swap="innerHTML",
                        cls="text-slate-400 hover:text-white transition-colors"
                    ),
                    Button(
                        trash_svg(),
                        hx_delete=f"/job/{job.id}",
                        hx_confirm=f"Are you sure you want to delete {job.title} at {job.company}?",
                        hx_target="#toast-container",
                        hx_swap="innerHTML",
                        cls="text-slate-400 hover:text-rose-500 transition-colors ml-2.5"
                    ),
                    cls="flex items-center"
                ),
                cls="flex justify-between items-start"
            ),
            H3(job.title, cls="text-sm font-bold text-white mt-1 line-clamp-1"),
            Div(
                calendar_svg(),
                Span(f"Applied: {job.date_applied}" if job.date_applied else "Wishlisted", cls="text-xs text-slate-400 ml-1"),
                cls="flex items-center mt-2.5 text-slate-400"
            ),
            (
                A(
                    external_link_svg(),
                    "View Listing",
                    href=job.url,
                    target="_blank",
                    cls="inline-flex items-center text-xs text-blue-400 hover:text-blue-300 transition-colors mt-2"
                ) if job.url else ""
            ),
            (
                P(
                    job.notes,
                    cls="text-xs text-slate-300 bg-slate-950/45 p-2 rounded border border-slate-800/60 mt-3 line-clamp-2"
                ) if job.notes else ""
            ),
            cls="p-4"
        ),
        id=f"card-{job.id}",
        data_id=str(job.id),
        cls="job-card cursor-grab active:cursor-grabbing bg-slate-900/60 border border-slate-800 hover:border-slate-700/80 rounded-xl shadow-lg transition-all duration-200 hover:-translate-y-0.5",
    )

def render_dropzone_content(user_id, status, search_query=""):
    if search_query:
        # SQL case-insensitive search scoped by user_id
        col_jobs = jobs(
            where="user_id = ? AND status = ? AND (company LIKE ? OR title LIKE ?)",
            where_args=[user_id, status, f"%{search_query}%", f"%{search_query}%"]
        )
    else:
        col_jobs = jobs(where="user_id = ? AND status = ?", where_args=[user_id, status])
    
    cards = [job_card(j) for j in col_jobs]
    return Div(*cards,
               id=f"dropzone-{status}",
               data_status=status,
               cls="kanban-dropzone space-y-3 min-h-[450px] p-2 rounded-xl transition-colors duration-200")

def kanban_board(user_id, search_query=""):
    columns_html = []
    statuses = ["Wishlist", "Applied", "Interviewing", "Offer", "Rejected"]
    for status in statuses:
        if search_query:
            count = jobs.count_where("user_id = ? AND status = ? AND (company LIKE ? OR title LIKE ?)", [user_id, status, f"%{search_query}%", f"%{search_query}%"])
        else:
            count = jobs.count_where("user_id = ? AND status = ?", [user_id, status])
        
        col_html = Div(
            column_header(status, count),
            render_dropzone_content(user_id, status, search_query),
            cls="bg-slate-900/20 border border-slate-900 rounded-2xl p-4 flex flex-col flex-1"
        )
        columns_html.append(col_html)
    
    return Div(*columns_html, id="kanban-board", cls="grid grid-cols-1 lg:grid-cols-5 gap-6")

def job_form(job=None):
    is_edit = job is not None
    title_text = "Edit Job Application" if is_edit else "Add New Job Application"
    action_url = f"/job/{job.id}/edit" if is_edit else "/job/new"
    
    company_val = job.company if is_edit else ""
    title_val = job.title if is_edit else ""
    status_val = job.status if is_edit else "Wishlist"
    date_val = job.date_applied if is_edit else datetime.date.today().isoformat()
    url_val = job.url if is_edit else ""
    notes_val = job.notes if is_edit else ""
    
    statuses = ["Wishlist", "Applied", "Interviewing", "Offer", "Rejected"]
    options = [Option(s, value=s, selected=(s == status_val)) for s in statuses]
    
    return Div(
        Div(
            H2(title_text, cls="text-lg font-extrabold text-white"),
            Button(
                close_svg(),
                onclick="document.getElementById('job-modal').close()",
                cls="text-slate-400 hover:text-white transition-colors"
            ),
            cls="flex justify-between items-center mb-6"
        ),
        Form(
            (Input(type="hidden", name="id", value=str(job.id)) if is_edit else ""),
            
            Div(
                Label("Company *", cls="block text-xs font-semibold text-slate-400 uppercase mb-1"),
                Input(type="text", name="company", value=company_val, required=True, placeholder="e.g. Google, Stripe",
                      cls="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white placeholder-slate-600 focus:outline-none focus:border-blue-500 transition-colors"),
                cls="mb-4"
            ),
            
            Div(
                Label("Job Title *", cls="block text-xs font-semibold text-slate-400 uppercase mb-1"),
                Input(type="text", name="title", value=title_val, required=True, placeholder="e.g. Software Engineer",
                      cls="w-full bg-slate-955 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white placeholder-slate-600 focus:outline-none focus:border-blue-500 transition-colors"),
                cls="mb-4"
            ),
            
            Div(
                Div(
                    Label("Status", cls="block text-xs font-semibold text-slate-400 uppercase mb-1"),
                    Select(*options, name="status",
                           cls="w-full bg-slate-955 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-blue-500 transition-colors"),
                ),
                Div(
                    Label("Date Applied", cls="block text-xs font-semibold text-slate-400 uppercase mb-1"),
                    Input(type="date", name="date_applied", value=date_val,
                          cls="w-full bg-slate-955 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-blue-500 transition-colors"),
                ),
                cls="grid grid-cols-2 gap-4 mb-4"
            ),
            
            Div(
                Label("Listing URL", cls="block text-xs font-semibold text-slate-400 uppercase mb-1"),
                Input(type="url", name="url", value=url_val, placeholder="https://careers.google.com/...",
                      cls="w-full bg-slate-955 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white placeholder-slate-600 focus:outline-none focus:border-blue-500 transition-colors"),
                cls="mb-4"
            ),
            
            Div(
                Label("Notes", cls="block text-xs font-semibold text-slate-400 uppercase mb-1"),
                Textarea(notes_val, name="notes", rows=3, placeholder="Requirements, salary, interview stages...",
                         cls="w-full bg-slate-955 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white placeholder-slate-600 focus:outline-none focus:border-blue-500 transition-colors"),
                cls="mb-6"
            ),
            
            Div(
                Button("Cancel", type="button", onclick="document.getElementById('job-modal').close()",
                       cls="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg text-sm font-semibold transition-colors mr-2"),
                Button("Save Application", type="submit",
                       cls="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-lg text-sm font-bold transition-all shadow-md hover:shadow-blue-600/20"),
                cls="flex justify-end"
            ),
            hx_post=action_url,
            hx_target="#toast-container",
            hx_swap="innerHTML"
        ),
        cls="p-1"
    )

def main_layout(user_id, username, search_query=""):
    board = kanban_board(user_id, search_query)
    analytics = get_analytics_view(user_id)
    
    return Div(
        Div(
            # Header View
            Header(
                Div(
                    Div(
                        briefcase_svg(),
                        H1("Job Tracker", cls="text-xl font-black text-white tracking-tight ml-2"),
                        cls="flex items-center"
                    ),
                    # Action Trigger Buttons and User Badge
                    Div(
                        Div(
                            Span(f"Welcome, {username}", cls="text-sm font-medium text-slate-350 mr-4"),
                            A(
                                log_out_svg(),
                                "Logout",
                                href="/logout",
                                cls="inline-flex items-center text-xs font-semibold px-2.5 py-1.5 bg-slate-900 border border-slate-800 hover:bg-slate-800 hover:border-slate-700 text-slate-300 rounded-lg transition-colors mr-2"
                            ),
                            cls="flex items-center mr-4 border-r border-slate-900 pr-4"
                        ),
                        Button(
                            "+ Add Job",
                            hx_get="/job/new",
                            hx_target="#modal-content",
                            hx_swap="innerHTML",
                            cls="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white text-sm font-bold rounded-xl transition-all shadow-md hover:shadow-blue-600/20 flex items-center"
                        ),
                        cls="flex items-center"
                    ),
                    cls="flex justify-between items-center"
                ),
                cls="mb-8 border-b border-slate-900 pb-6"
            ),
            
            # Interactive Filter Bar
            Div(
                Div(
                    search_svg(),
                    Input(type="text", name="q", value=search_query, placeholder="Search company or title...",
                          hx_get="/search", hx_trigger="keyup changed delay:150ms", hx_target="#kanban-container", hx_swap="innerHTML",
                          cls="w-full bg-slate-900/60 border border-slate-850 rounded-xl pl-10 pr-4 py-2 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-slate-700 transition-colors"),
                    cls="relative max-w-xs w-full"
                ),
                cls="mb-6 flex justify-between items-center"
            ),
            
            # Kanban Board Box
            Div(board, id="kanban-container", cls="mb-10"),
            
            # Analytics Dashboard Box
            analytics,
            
            cls="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8"
        ),
        cls="min-h-screen bg-slate-955 text-slate-100 font-sans selection:bg-blue-500/30 selection:text-white"
    )

def toast_notification(message, type="success"):
    bg_color = "bg-emerald-950/95 border-emerald-800/80 text-emerald-300" if type == "success" else "bg-rose-955/95 border-rose-800/80 text-rose-350"
    toast_id = f"toast-{int(datetime.datetime.now().timestamp() * 1000)}"
    return Div(
        Span(message, cls="text-xs font-semibold"),
        Script(f"""
            setTimeout(() => {{
                let el = document.getElementById('{toast_id}');
                if (el) {{
                    el.style.opacity = '0';
                    setTimeout(() => el.remove(), 400);
                }}
            }}, 3000);
        """),
        id=toast_id,
        cls=f"{bg_color} border px-4 py-2.5 rounded-xl shadow-lg transition-all duration-300 ease-in-out opacity-100 flex items-center justify-between min-w-[260px]",
    )


# 6. Isolated Analytics & Export Layer
def get_analytics_view(user_id):
    rows = list(jobs.rows_where("user_id = ?", [user_id]))
    if not rows:
        return Div(
            Div(
                H2("Analytics Summary", cls="text-base font-bold text-white mb-2"),
                P("No job data recorded yet. Add applications to display dashboard statistics.", cls="text-slate-400 text-sm py-4 text-center"),
                cls="bg-slate-900/40 border border-slate-900 rounded-2xl p-6"
            ),
            id="analytics-dashboard"
        )
    
    df = pd.DataFrame(rows)
    total = len(df)
    
    status_counts = df['status'].value_counts().to_dict()
    wishlist = status_counts.get('Wishlist', 0)
    applied = status_counts.get('Applied', 0)
    interviewing = status_counts.get('Interviewing', 0)
    offer = status_counts.get('Offer', 0)
    rejected = status_counts.get('Rejected', 0)
    
    active_statuses = ['Applied', 'Interviewing', 'Offer', 'Rejected']
    active_df = df[df['status'].isin(active_statuses)]
    active_count = len(active_df)
    interview_or_offer = len(df[df['status'].isin(['Interviewing', 'Offer'])])
    
    interview_rate = (interview_or_offer / active_count * 100) if active_count > 0 else 0.0
    
    return Div(
        Div(
            H2("Analytics Summary", cls="text-base font-extrabold text-white"),
            Div(
                A(
                    download_svg(),
                    "Export CSV",
                    href="/export/csv",
                    cls="inline-flex items-center text-xs font-semibold px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg transition-colors border border-slate-700/80 mr-2"
                ),
                A(
                    markdown_svg(),
                    "Export Markdown",
                    href="/export/markdown",
                    cls="inline-flex items-center text-xs font-semibold px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg transition-colors border border-slate-700/80"
                ),
                cls="flex items-center"
            ),
            cls="flex justify-between items-center mb-6"
        ),
        
        # Numbers Metric Row
        Div(
            metric_card("Total Applications", str(total), "bg-slate-900/30 border-slate-850", "text-white"),
            metric_card("Interview Success", f"{interview_rate:.1f}%", "bg-slate-900/30 border-slate-850", "text-blue-400"),
            metric_card("Offers Received", str(offer), "bg-slate-900/30 border-slate-850", "text-emerald-400"),
            metric_card("Rejections", str(rejected), "bg-slate-900/30 border-slate-850", "text-rose-400"),
            cls="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6"
        ),
        
        # Pipeline Percentage Breakdown
        Div(
            H3("Pipeline Stage Distribution", cls="text-xs font-bold text-slate-400 uppercase tracking-wider mb-4"),
            Div(
                pipeline_bar("Wishlist", wishlist, total, "bg-slate-500"),
                pipeline_bar("Applied", applied, total, "bg-blue-500"),
                pipeline_bar("Interviewing", interviewing, total, "bg-amber-500"),
                pipeline_bar("Offer", offer, total, "bg-emerald-500"),
                pipeline_bar("Rejected", rejected, total, "bg-rose-500"),
                cls="space-y-3 bg-slate-950/40 p-4 rounded-xl border border-slate-900"
            ),
            cls="mt-2"
        ),
        id="analytics-dashboard",
        cls="bg-slate-900/40 border border-slate-900 rounded-2xl p-6 shadow-md"
    )

def metric_card(label, value, bg_class, text_class):
    return Div(
        Span(label, cls="text-xs text-slate-400 font-semibold uppercase tracking-wider"),
        Div(value, cls=f"text-xl font-black mt-1.5 {text_class}"),
        cls=f"{bg_class} border rounded-xl p-4 shadow-sm"
    )

def pipeline_bar(label, count, total, bar_color):
    pct = (count / total * 100) if total > 0 else 0
    return Div(
        Div(
            Span(label, cls="text-xs font-bold text-slate-350"),
            Span(f"{count} ({pct:.0f}%)", cls="text-xs font-bold text-slate-400"),
            cls="flex justify-between text-xs mb-1"
        ),
        Div(
            Div(style=f"width: {pct}%", cls=f"h-1.5 rounded-full {bar_color} transition-all duration-500"),
            cls="h-1.5 w-full bg-slate-900 rounded-full overflow-hidden"
        ),
        cls="py-0.5"
    )

def df_to_markdown(df):
    if df.empty:
        return ""
    cols = list(df.columns)
    headers = " | ".join(cols)
    separator = " | ".join(["---"] * len(cols))
    
    rows = []
    for _, row in df.iterrows():
        row_str = " | ".join([str(row[c]).replace('\n', ' ') for c in cols])
        rows.append(row_str)
        
    return f"| {headers} |\n| {separator} |\n" + "\n".join([f"| {r} |" for r in rows])


# 7. FastHTML Endpoint Routes

# Login View GET
@rt('/login', methods=['GET'])
def login_page(error_msg: str = "", registered: str = ""):
    success_banner = ""
    if registered == "1":
        success_banner = Div("Account created successfully! Please log in below.", cls="bg-emerald-950/60 border border-emerald-800 text-emerald-300 px-4 py-2.5 rounded-lg text-xs font-semibold mb-4 text-center")
    
    card = Div(
        Div(
            briefcase_svg(),
            H1("Job Tracker Login", cls="text-xl font-black text-white tracking-tight ml-2"),
            cls="flex items-center justify-center mb-6"
        ),
        (success_banner if success_banner else P("Enter your credentials to access your dashboard.", cls="text-slate-400 text-xs text-center mb-6 leading-relaxed")),
        Form(
            Div(
                Label("Username", cls="block text-xs font-semibold text-slate-400 uppercase mb-1"),
                Input(type="text", name="username", required=True, placeholder="e.g. saurabh",
                      cls="w-full bg-slate-955 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white placeholder-slate-650 focus:outline-none focus:border-blue-500 transition-colors"),
                cls="mb-4"
            ),
            Div(
                Label("Password", cls="block text-xs font-semibold text-slate-400 uppercase mb-1"),
                Div(
                    Input(type="password", name="password", id="login-pwd", required=True, placeholder="••••••••",
                          cls="w-full bg-slate-955 border border-slate-800 rounded-lg pl-3 pr-10 py-2 text-sm text-white placeholder-slate-655 focus:outline-none focus:border-blue-500 transition-colors"),
                    Button(
                        SafeHtml(eye_on_svg()),
                        id="login-eye-pwd",
                        type="button",
                        onclick="togglePassword('login-pwd', 'login-eye-pwd')",
                        cls="absolute right-3 top-2.5 text-slate-455 hover:text-white transition-colors"
                    ),
                    cls="relative w-full"
                ),
                cls="mb-6"
            ),
            (
                Div(error_msg, cls="text-rose-450 text-xs font-semibold mb-4 text-center") if error_msg else ""
            ),
            Button("Sign In", type="submit",
                   cls="w-full py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-lg text-sm font-bold transition-all shadow-md hover:shadow-blue-600/20 mb-4"),
            P(
                Span("Don't have an account? ", cls="text-slate-450"),
                A("Sign Up", href="/signup", cls="text-blue-400 hover:text-blue-300 font-semibold underline"),
                cls="text-xs text-center"
            ),
            action="/login",
            method="post"
        ),
        cls="bg-slate-900/65 border border-slate-800/85 backdrop-blur-md rounded-2xl p-8 shadow-2xl max-w-sm w-full mx-4"
    )
    
    eye_script = Script(f"""
        const eyeOnSvg = `{eye_on_svg()}`;
        const eyeOffSvg = `{eye_off_svg()}`;
        function togglePassword(inputId, eyeId) {{
            var input = document.getElementById(inputId);
            var eye = document.getElementById(eyeId);
            if (input.type === 'password') {{
                input.type = 'text';
                eye.innerHTML = eyeOffSvg;
            }} else {{
                input.type = 'password';
                eye.innerHTML = eyeOnSvg;
            }}
        }}
    """)
    
    return Title("Job Tracker - Login"), Body(
        Div(card, cls="min-h-screen bg-slate-950 flex items-center justify-center"),
        eye_script,
        cls="bg-slate-955 text-slate-100"
    )

# Signup View GET
@rt('/signup', methods=['GET'])
def signup_page(error_msg: str = ""):
    card = Div(
        Div(
            briefcase_svg(),
            H1("Create Account", cls="text-xl font-black text-white tracking-tight ml-2"),
            cls="flex items-center justify-center mb-6"
        ),
        P("Fill in the fields below to register a new account.",
          cls="text-slate-400 text-xs text-center mb-6 leading-relaxed"),
        Form(
            Div(
                Label("Username *", cls="block text-xs font-semibold text-slate-400 uppercase mb-1"),
                Input(type="text", name="username", required=True, placeholder="e.g. saurabh",
                      cls="w-full bg-slate-955 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white placeholder-slate-650 focus:outline-none focus:border-blue-500 transition-colors"),
                cls="mb-4"
            ),
            Div(
                Label("Password *", cls="block text-xs font-semibold text-slate-400 uppercase mb-1"),
                Div(
                    Input(type="password", name="password", id="signup-pwd", required=True, placeholder="••••••••",
                          cls="w-full bg-slate-955 border border-slate-800 rounded-lg pl-3 pr-10 py-2 text-sm text-white placeholder-slate-650 focus:outline-none focus:border-blue-500 transition-colors"),
                    Button(
                        SafeHtml(eye_on_svg()),
                        id="signup-eye-pwd",
                        type="button",
                        onclick="togglePassword('signup-pwd', 'signup-eye-pwd')",
                        cls="absolute right-3 top-2.5 text-slate-450 hover:text-white transition-colors"
                    ),
                    cls="relative w-full"
                ),
                cls="mb-4"
            ),
            Div(
                Label("Confirm Password *", cls="block text-xs font-semibold text-slate-400 uppercase mb-1"),
                Div(
                    Input(type="password", name="confirm_password", id="signup-confirm-pwd", required=True, placeholder="••••••••",
                          cls="w-full bg-slate-955 border border-slate-800 rounded-lg pl-3 pr-10 py-2 text-sm text-white placeholder-slate-650 focus:outline-none focus:border-blue-500 transition-colors"),
                    Button(
                        SafeHtml(eye_on_svg()),
                        id="signup-eye-confirm",
                        type="button",
                        onclick="togglePassword('signup-confirm-pwd', 'signup-eye-confirm')",
                        cls="absolute right-3 top-2.5 text-slate-450 hover:text-white transition-colors"
                    ),
                    cls="relative w-full"
                ),
                cls="mb-6"
            ),
            (
                Div(error_msg, cls="text-rose-450 text-xs font-semibold mb-4 text-center") if error_msg else ""
            ),
            Button("Register Account", type="submit",
                   cls="w-full py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-lg text-sm font-bold transition-all shadow-md hover:shadow-blue-600/20 mb-4"),
            P(
                Span("Already have an account? ", cls="text-slate-450"),
                A("Log in", href="/login", cls="text-blue-400 hover:text-blue-300 font-semibold underline"),
                cls="text-xs text-center"
            ),
            action="/signup",
            method="post"
        ),
        cls="bg-slate-900/65 border border-slate-800/85 backdrop-blur-md rounded-2xl p-8 shadow-2xl max-w-sm w-full mx-4"
    )
    
    eye_script = Script(f"""
        const eyeOnSvg = `{eye_on_svg()}`;
        const eyeOffSvg = `{eye_off_svg()}`;
        function togglePassword(inputId, eyeId) {{
            var input = document.getElementById(inputId);
            var eye = document.getElementById(eyeId);
            if (input.type === 'password') {{
                input.type = 'text';
                eye.innerHTML = eyeOffSvg;
            }} else {{
                input.type = 'password';
                eye.innerHTML = eyeOnSvg;
            }}
        }}
    """)
    
    return Title("Job Tracker - Sign Up"), Body(
        Div(card, cls="min-h-screen bg-slate-950 flex items-center justify-center"),
        eye_script,
        cls="bg-slate-950 text-slate-100"
    )

# Signup View POST
@rt('/signup', methods=['POST'])
def handle_signup(username: str, password: str, confirm_password: str):
    username = username.strip()
    if not username or not password or not confirm_password:
        return signup_page("All fields are required.")
    
    if password != confirm_password:
        return signup_page("Passwords do not match.")
        
    # Check if username exists
    existing_users = list(users.rows_where("username = ?", [username]))
    if existing_users:
        return signup_page("Username already taken. Please choose another.")
        
    # Register user
    pwd_hash = hash_password(password)
    new_user = User(username=username, password=pwd_hash)
    users.insert(new_user)
    
    # Get ID
    user = list(users.rows_where("username = ?", [username]))[0]
    user_id = user['id']
    
    # Seed mock data if first user
    user_count = users.count
    if user_count == 1:
        seed_jobs_for_user(user_id)
        
    # Redirect to login with success parameter
    return RedirectResponse('/login?registered=1', status_code=303)

# Login View POST
@rt('/login', methods=['POST'])
def handle_login(username: str, password: str, sess):
    username = username.strip()
    if not username or not password:
        return login_page("Username and password are required.")
    
    # Check if user exists
    existing_users = list(users.rows_where("username = ?", [username]))
    if not existing_users:
        # Give explicit message that user doesn't exist and link to signup
        return login_page("User does not exist. Click on Sign Up below to create a new user.")
    else:
        user = existing_users[0]
        pwd_hash = hash_password(password)
        if user['password'] == pwd_hash:
            # Login successful
            sess['auth'] = user['id']
            sess['username'] = user['username']
            return RedirectResponse('/', status_code=303)
        else:
            return login_page("Incorrect password. Please enter the correct password.")

# Logout View GET
@rt('/logout', methods=['GET'])
def handle_logout(sess):
    sess.clear()
    return RedirectResponse('/login', status_code=303)

# Protected Main View (Root / Dashboard)
@rt('/', methods=['GET'])
def dashboard_page(sess):
    user_id = sess.get('auth')
    username = sess.get('username', 'User')
    
    content = main_layout(user_id, username)
    
    modal = Dialog(
        Div(id="modal-content"),
        id="job-modal",
        cls="modal max-w-lg w-full bg-slate-900 text-slate-100 rounded-2xl border border-slate-800 p-6 shadow-2xl backdrop:bg-slate-950/80 backdrop:backdrop-blur-sm focus:outline-none"
    )
    toast_container = Div(id="toast-container", cls="fixed bottom-5 right-5 z-50 flex flex-col gap-2")
    
    # SortableJS Drag & Drop Initialization script
    sortable_script = Script("""
        function initSortable() {
            var columns = document.querySelectorAll(".kanban-dropzone");
            columns.forEach(function(col) {
                if (!col.classList.contains("sortable-active")) {
                    col.classList.add("sortable-active");
                    new Sortable(col, {
                        group: 'kanban',
                        animation: 150,
                        ghostClass: 'sortable-ghost',
                        chosenClass: 'sortable-chosen',
                        onEnd: function (evt) {
                            let cardId = evt.item.getAttribute("data-id");
                            let targetStatus = evt.to.getAttribute("data-status");
                            htmx.ajax('POST', '/job/' + cardId + '/status', {
                                values: { status: targetStatus },
                                target: '#toast-container',
                                swap: 'innerHTML'
                            });
                        }
                    });
                }
            });
        }
        htmx.onLoad(function(content) {
            initSortable();
        });
    """)
    
    return Title("Job Tracker"), Body(
        content,
        modal,
        toast_container,
        sortable_script,
        cls="bg-slate-955 min-h-screen text-slate-100"
    )

# Search handler
@rt('/search', methods=['GET'])
def search_jobs(sess, q: str = ""):
    user_id = sess.get('auth')
    return kanban_board(user_id, q)

# Show Add Job form
@rt('/job/new', methods=['GET'])
def new_job_form():
    form = job_form()
    script = Script("document.getElementById('job-modal').showModal();")
    return Div(form, script)

# Add Job submission
@rt('/job/new', methods=['POST'])
def add_job(sess, company: str, title: str, status: str, date_applied: str = "", url: str = "", notes: str = ""):
    try:
        user_id = sess.get('auth')
        new_job = Job(
            user_id=user_id,
            company=company,
            title=title,
            status=status,
            date_applied=date_applied,
            url=url,
            notes=notes
        )
        jobs.insert(new_job)
        
        toast = toast_notification(f"Saved application for {company}", "success")
        close_script = Script("document.getElementById('job-modal').close();")
        
        # Swap updated dropzone and dashboard metrics for this user
        dropzone = render_dropzone_content(user_id, status)
        dropzone.attrs["hx-swap-oob"] = "true"
        
        # OOB updates for counts
        count_swaps = []
        statuses = ["Wishlist", "Applied", "Interviewing", "Offer", "Rejected"]
        for s in statuses:
            count = jobs.count_where("user_id = ? AND status = ?", [user_id, s])
            count_swaps.append(
                Span(str(count), id=f"count-{s}", hx_swap_oob="true", cls=get_count_badge_class(s))
            )
            
        analytics = get_analytics_view(user_id)
        analytics.attrs["hx-swap-oob"] = "true"
        
        return Div(
            toast,
            dropzone,
            *count_swaps,
            analytics,
            close_script
        )
    except Exception as e:
        return toast_notification(f"Error adding job: {str(e)}", "error")

# Show Edit form
@rt('/job/{id}/edit', methods=['GET'])
def edit_job_form(sess, id: int):
    try:
        user_id = sess.get('auth')
        job = jobs[id]
        if job.user_id != user_id:
            return toast_notification("Unauthorized: Attempt to access another user's application details.", "error")
            
        form = job_form(job)
        script = Script("document.getElementById('job-modal').showModal();")
        return Div(form, script)
    except Exception as e:
        return toast_notification(f"Error loading application details: {str(e)}", "error")

# Edit Job submission
@rt('/job/{id}/edit', methods=['POST'])
def edit_job(sess, id: int, company: str, title: str, status: str, date_applied: str = "", url: str = "", notes: str = ""):
    try:
        user_id = sess.get('auth')
        job = jobs[id]
        if job.user_id != user_id:
            return toast_notification("Unauthorized action.", "error")
            
        old_status = job.status
        
        job.company = company
        job.title = title
        job.status = status
        job.date_applied = date_applied
        job.url = url
        job.notes = notes
        
        jobs.update(job)
        
        toast = toast_notification(f"Updated application for {company}", "success")
        close_script = Script("document.getElementById('job-modal').close();")
        
        swaps = [toast, close_script]
        
        # Status change triggers multi-column re-renders, otherwise just re-renders single target column
        if old_status != status:
            old_dropzone = render_dropzone_content(user_id, old_status)
            old_dropzone.attrs["hx-swap-oob"] = "true"
            swaps.append(old_dropzone)
            
            new_dropzone = render_dropzone_content(user_id, status)
            new_dropzone.attrs["hx-swap-oob"] = "true"
            swaps.append(new_dropzone)
        else:
            dropzone = render_dropzone_content(user_id, status)
            dropzone.attrs["hx-swap-oob"] = "true"
            swaps.append(dropzone)
            
        # OOB updates for counts
        statuses = ["Wishlist", "Applied", "Interviewing", "Offer", "Rejected"]
        for s in statuses:
            count = jobs.count_where("user_id = ? AND status = ?", [user_id, s])
            swaps.append(
                Span(str(count), id=f"count-{s}", hx_swap_oob="true", cls=get_count_badge_class(s))
            )
            
        analytics = get_analytics_view(user_id)
        analytics.attrs["hx-swap-oob"] = "true"
        swaps.append(analytics)
        
        return Div(*swaps)
    except Exception as e:
        return toast_notification(f"Error updating application: {str(e)}", "error")

# Delete Job application
@rt('/job/{id}', methods=['DELETE'])
def delete_job(sess, id: int):
    try:
        user_id = sess.get('auth')
        job = jobs[id]
        if job.user_id != user_id:
            return toast_notification("Unauthorized action.", "error")
            
        status = job.status
        company = job.company
        
        jobs.delete(id)
        
        toast = toast_notification(f"Removed application for {company}", "success")
        
        # Re-render status column dropzone
        dropzone = render_dropzone_content(user_id, status)
        dropzone.attrs["hx-swap-oob"] = "true"
        
        # Count updates
        count_swaps = []
        statuses = ["Wishlist", "Applied", "Interviewing", "Offer", "Rejected"]
        for s in statuses:
            count = jobs.count_where("user_id = ? AND status = ?", [user_id, s])
            count_swaps.append(
                Span(str(count), id=f"count-{s}", hx_swap_oob="true", cls=get_count_badge_class(s))
            )
            
        analytics = get_analytics_view(user_id)
        analytics.attrs["hx-swap-oob"] = "true"
        
        return Div(
            toast,
            dropzone,
            *count_swaps,
            analytics
        )
    except Exception as e:
        return toast_notification(f"Error deleting job: {str(e)}", "error")

# Drag-and-drop / Status changes
@rt('/job/{id}/status', methods=['POST'])
def update_job_status(sess, id: int, status: str):
    try:
        user_id = sess.get('auth')
        job = jobs[id]
        if job.user_id != user_id:
            return toast_notification("Unauthorized action.", "error")
            
        job.status = status
        jobs.update(job)
        
        toast = toast_notification(f"Moved {job.company} to {status}", "success")
        
        # Return updated counts
        count_swaps = []
        statuses = ["Wishlist", "Applied", "Interviewing", "Offer", "Rejected"]
        for s in statuses:
            count = jobs.count_where("user_id = ? AND status = ?", [user_id, s])
            count_swaps.append(
                Span(str(count), id=f"count-{s}", hx_swap_oob="true", cls=get_count_badge_class(s))
            )
            
        analytics = get_analytics_view(user_id)
        analytics.attrs["hx-swap-oob"] = "true"
        
        return Div(
            toast,
            *count_swaps,
            analytics
        )
    except Exception as e:
        return toast_notification(f"Error moving job: {str(e)}", "error")


# 8. Data Export Router Handles (scoped to User)

# Download CSV Export
@rt('/export/csv', methods=['GET'])
def export_csv(sess):
    try:
        user_id = sess.get('auth')
        rows = list(jobs.rows_where("user_id = ?", [user_id]))
        if not rows:
            return Response("No job data to export.", status_code=400)
        
        df = pd.DataFrame(rows)
        # Order columns for CSV output
        df = df[['id', 'company', 'title', 'status', 'date_applied', 'url', 'notes']]
        csv_content = df.to_csv(index=False)
        
        return Response(
            csv_content,
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=job_applications.csv"}
        )
    except Exception as e:
        return Response(f"CSV Export Error: {str(e)}", status_code=500)

# Download Markdown Summary
@rt('/export/markdown', methods=['GET'])
def export_markdown(sess):
    try:
        user_id = sess.get('auth')
        rows = list(jobs.rows_where("user_id = ?", [user_id]))
        if not rows:
            return Response("No job data to export.", status_code=400)
        
        df = pd.DataFrame(rows)
        df = df[['company', 'title', 'status', 'date_applied', 'url', 'notes']]
        md_table = df_to_markdown(df)
        
        date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        report = f"# Job Applications Report\nGenerated: {date_str}\n\n{md_table}"
        
        return Response(
            report,
            media_type="text/markdown",
            headers={"Content-Disposition": "attachment; filename=job_applications_report.md"}
        )
    except Exception as e:
        return Response(f"Markdown Export Error: {str(e)}", status_code=500)


# 9. Serve Application Local Server
if __name__ == '__main__':
    serve(host='localhost', port=5001)
