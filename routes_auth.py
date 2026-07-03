from fasthtml.common import *
from app import rt
from database import users, hash_password, User, seed_jobs_for_user
from components import briefcase_svg, eye_on_svg, eye_off_svg



# Login View GET
@rt('/login', methods=['GET'])
def login_page(error_msg: str = "", registered: str = ""):
    success_banner = ""
    if registered == "1":
        success_banner = Div("Account created successfully! Please log in below.", cls="bg-emerald-950/60 border border-emerald-800 text-emerald-350 px-4 py-2.5 rounded-lg text-xs font-semibold mb-4 text-center")
    
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
                      cls="w-full bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-blue-500 transition-colors"),
                cls="mb-4"
            ),
            Div(
                Label("Password", cls="block text-xs font-semibold text-slate-400 uppercase mb-1"),
                Div(
                    Input(type="password", name="password", id="login-pwd", required=True, placeholder="••••••••",
                          cls="w-full bg-slate-900 border border-slate-800 rounded-lg pl-3 pr-10 py-2 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-blue-500 transition-colors"),
                    Button(
                        NotStr(eye_on_svg()),
                        id="login-eye-pwd",
                        type="button",
                        onclick="togglePassword('login-pwd', 'login-eye-pwd')",
                        cls="absolute right-3 top-2.5 text-slate-400 hover:text-slate-200 transition-colors"
                    ),
                    cls="relative w-full"
                ),
                cls="mb-6"
            ),
            (
                Div(error_msg, cls="text-rose-455 text-xs font-semibold mb-4 text-center") if error_msg else ""
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
                      cls="w-full bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-blue-500 transition-colors"),
                cls="mb-4"
            ),
            Div(
                Label("Password *", cls="block text-xs font-semibold text-slate-400 uppercase mb-1"),
                Div(
                    Input(type="password", name="password", id="signup-pwd", required=True, placeholder="••••••••",
                          cls="w-full bg-slate-900 border border-slate-800 rounded-lg pl-3 pr-10 py-2 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-blue-500 transition-colors"),
                    Button(
                        NotStr(eye_on_svg()),
                        id="signup-eye-pwd",
                        type="button",
                        onclick="togglePassword('signup-pwd', 'signup-eye-pwd')",
                        cls="absolute right-3 top-2.5 text-slate-400 hover:text-slate-200 transition-colors"
                    ),
                    cls="relative w-full"
                ),
                cls="mb-4"
            ),
            Div(
                Label("Confirm Password *", cls="block text-xs font-semibold text-slate-400 uppercase mb-1"),
                Div(
                    Input(type="password", name="confirm_password", id="signup-confirm-pwd", required=True, placeholder="••••••••",
                          cls="w-full bg-slate-900 border border-slate-800 rounded-lg pl-3 pr-10 py-2 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-blue-500 transition-colors"),
                    Button(
                        NotStr(eye_on_svg()),
                        id="signup-eye-confirm",
                        type="button",
                        onclick="togglePassword('signup-confirm-pwd', 'signup-eye-confirm')",
                        cls="absolute right-3 top-2.5 text-slate-400 hover:text-slate-200 transition-colors"
                    ),
                    cls="relative w-full"
                ),
                cls="mb-6"
            ),
            (
                Div(error_msg, cls="text-rose-455 text-xs font-semibold mb-4 text-center") if error_msg else ""
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
