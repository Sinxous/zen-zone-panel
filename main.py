from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import urllib.parse

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Access log list
access_logs = ["Morgan", "Sam"]

@app.get("/")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    # Default login
    if username == "admin" and password == "password123":
        response = RedirectResponse("/name-input", status_code=302)
        response.set_cookie("user", username)
        return response
    return templates.TemplateResponse("login.html", {"request": request, "error": True})

@app.get("/name-input")
def name_input(request: Request):
    return templates.TemplateResponse("name_input.html", {"request": request})

@app.post("/set-name")
def set_name(request: Request, display_name: str = Form(...)):
    # Encode the name for cookie (fixes Unicode crash on Render)
    safe_name = urllib.parse.quote(display_name)

    response = RedirectResponse("/dashboard", status_code=302)
    response.set_cookie("display_name", safe_name)

    # Add the REAL name to access logs
    access_logs.append(display_name)

    return response

@app.get("/dashboard")
def dashboard(request: Request):
    user = request.cookies.get("user")

    # Decode the encoded cookie name
    raw_name = request.cookies.get("display_name", "")
    display_name = urllib.parse.unquote(raw_name)

    if not user:
        return RedirectResponse("/")

    members = 17
    member_goal = 100
    member_percent = int(members / member_goal * 100)

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "display_name": display_name,
            "founder": "Morgan",
            "cofounder": "Sam",
            "members": members,
            "bots": 5,
            "member_goal": member_goal,
            "member_percent": member_percent,
            "access_logs": access_logs,
        }
    )
