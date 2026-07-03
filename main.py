from fasthtml.common import *
from app import app, rt
from components import main_layout, kanban_board

# Ensure all modular route handlers are loaded and registered
import routes_auth
import routes_jobs
import routes_export


# Protected Main View (Root / Dashboard)
@rt('/', methods=['GET'])
def dashboard_page(sess):
    user_id = sess.get('auth')
    username = sess.get('username', 'User')
    
    content = main_layout(user_id, username)
    
    modal = Dialog(
        Div(id="modal-content"),
        id="job-modal",
        cls="modal max-w-lg w-full bg-slate-900 text-slate-100 rounded-2xl border border-slate-800 p-6 shadow-2xl backdrop:bg-slate-955/80 backdrop:backdrop-blur-sm focus:outline-none"
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
        cls="bg-slate-950 min-h-screen text-slate-100"
    )

# Search handler
@rt('/search', methods=['GET'])
def search_jobs(sess, q: str = ""):
    user_id = sess.get('auth')
    return kanban_board(user_id, q)

# Serve Application Local Server
if __name__ == '__main__':
    serve(host='localhost', port=5001)
