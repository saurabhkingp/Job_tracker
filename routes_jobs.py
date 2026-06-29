from fasthtml.common import *
from app import rt
from database import jobs, Job
from components import job_form, toast_notification, render_dropzone_content, get_count_badge_class, get_analytics_view

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
