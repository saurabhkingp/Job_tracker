from fasthtml.common import *
from starlette.responses import Response

# Session Authentication Middleware & Beforeware Setup
login_redir = RedirectResponse('/login', status_code=303)

def before_auth(req, sess):
    auth = req.scope['auth'] = sess.get('auth', None)
    path = req.scope['path']
    # Allow login, signup, logout, static files, and favicon to bypass authentication
    if not auth and path not in ('/login', '/signup', '/logout') and not path.startswith('/static') and not path.startswith('/data'):
        return login_redir

bware = Beforeware(before_auth, skip=[r'/login', r'/signup', r'/logout', r'/static/.*', r'/data/.*', r'/favicon\.ico'])

# Initialize FastHTML App with Beforeware and Session configuration
import os
session_secret = os.environ.get('FASTHTML_SESSKEY', 'fallback-session-key-654321')

app, rt = fast_app(
    pico=False,
    before=bware,
    secret_key=session_secret,
    hdrs=(
        # Global Favicon
        Link(rel="icon", type="image/png", href="/data/logo.png"),
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
