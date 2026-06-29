from fasthtml.common import *
import pandas as pd
import datetime
from database import jobs

# Safe HTML Helper
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
                Span(job.company, cls="text-xs font-bold uppercase tracking-wider text-slate-400"),
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
                    cls="text-xs text-slate-300 bg-slate-900/45 p-2 rounded border border-slate-800/60 mt-3 line-clamp-2"
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
                      cls="w-full bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white placeholder-slate-600 focus:outline-none focus:border-blue-500 transition-colors"),
                cls="mb-4"
            ),
            
            Div(
                Label("Job Title *", cls="block text-xs font-semibold text-slate-400 uppercase mb-1"),
                Input(type="text", name="title", value=title_val, required=True, placeholder="e.g. Software Engineer",
                      cls="w-full bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white placeholder-slate-600 focus:outline-none focus:border-blue-500 transition-colors"),
                cls="mb-4"
            ),
            
            Div(
                Div(
                    Label("Status", cls="block text-xs font-semibold text-slate-400 uppercase mb-1"),
                    Select(*options, name="status",
                           cls="w-full bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-blue-500 transition-colors"),
                ),
                Div(
                    Label("Date Applied", cls="block text-xs font-semibold text-slate-400 uppercase mb-1"),
                    Input(type="date", name="date_applied", value=date_val,
                          cls="w-full bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-blue-500 transition-colors"),
                ),
                cls="grid grid-cols-2 gap-4 mb-4"
            ),
            
            Div(
                Label("Listing URL", cls="block text-xs font-semibold text-slate-400 uppercase mb-1"),
                Input(type="url", name="url", value=url_val, placeholder="https://careers.google.com/...",
                      cls="w-full bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white placeholder-slate-600 focus:outline-none focus:border-blue-500 transition-colors"),
                cls="mb-4"
            ),
            
            Div(
                Label("Notes", cls="block text-xs font-semibold text-slate-400 uppercase mb-1"),
                Textarea(notes_val, name="notes", rows=3, placeholder="Requirements, salary, interview stages...",
                         cls="w-full bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white placeholder-slate-600 focus:outline-none focus:border-blue-500 transition-colors"),
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
                            Span(f"Welcome, {username.title()}", cls="text-sm font-medium text-slate-350 mr-4"),
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
                          cls="w-full bg-slate-900 border border-slate-800 rounded-xl pl-10 pr-4 py-2 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-slate-700 transition-colors"),
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
