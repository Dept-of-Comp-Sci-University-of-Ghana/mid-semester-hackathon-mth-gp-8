import pickle
from typing import Optional

from fastapi import APIRouter, FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates/")


# @router.get("/form1", response_class=HTMLResponse)
# def form_get(request: Request):
# 	result = "Enter your text"
# 	return templates.TemplateResponse("result.html", context={"request":request, "result": result})


@router.get("/form1", response_class=HTMLResponse)
def form_post1(request: Request, query: Optional[str] = None):
	loaded_model = pickle.load(open("../model/saved_model.pkl", 'rb'))
	out = loaded_model.predict(query)
	return templates.TemplateResponse("result.html", context={"request":request, "result": out, "yourtext": query})
