import pickle
from typing import Optional

from fastapi import APIRouter, FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from ..library.helpers import text_cleaning

router = APIRouter()
templates = Jinja2Templates(directory="templates/")

@router.get("/form1", response_class=HTMLResponse)
def flagg_text(request: Request, query: Optional[str] = None):
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
	return templates.TemplateResponse("result.html", context={"request":request, "result": result[output], "yourtext":query})

