import pickle
from typing import Optional

from fastapi import APIRouter, FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .library.helpers import openfile, text_cleaning

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    data = openfile("home.md")
    return templates.TemplateResponse(
        "page.html", {"request": request, "data": data}
    )


@app.get("/page/{page_name}", response_class=HTMLResponse)
async def show_page(request: Request, page_name: str):
    data = openfile(page_name + ".md")
    return templates.TemplateResponse(
        "page.html", {"request": request, "data": data}
    )

@app.get("/form1", response_class=HTMLResponse)
def flag_text(request: Request, query: Optional[str] = None):
	"""
    A simple function that receive a query and predicts the insult potential of the content.
    :param review:
    :return: prediction
    """
	model = pickle.load(open("../model/saved_model.pkl", 'rb'))
    
    # clean the review
	cleaned_query = text_cleaning(query)
    
    # perform prediction
	prediction = model.predict([cleaned_query])
	output = int(prediction[0])

    # output dictionary
	result = {0: "Not an insult", 1: "Insult"}
    
    # show results
	data = openfile("home.md")
	return templates.TemplateResponse("page.html", context={"request":request, "data":data, "result": result[output], "OriginalUserInput":query, "UserInput":cleaned_query})

