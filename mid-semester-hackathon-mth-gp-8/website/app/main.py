from fastapi import APIRouter, FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .library.helpers import openfile

app = FastAPI()


templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    data = openfile("home.md")
    return templates.TemplateResponse(
        "page.html", {"request": request, "data": data}
    )


@app.get("/form1", response_class=HTMLResponse)
def form_post1(request: Request, user_text: str = Form(...)):
	print(user_text)
	#return templates.TemplateResponse("twoforms.html", context={"request":request, "result": result, "yournum": number})


@app.get("/page/{page_name}", response_class=HTMLResponse)
async def show_page(request: Request, page_name: str):
    data = openfile(page_name + ".md")
    return templates.TemplateResponse(
        "page.html", {"request": request, "data": data}
    )
