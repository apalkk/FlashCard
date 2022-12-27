from fastapi import Form, File, UploadFile, Request, FastAPI
from typing import List
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import FileResponse
import json
import os 
from random import randint

pgN = 0

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get('/')
def main():
 return FileResponse('index.html')

@app.post("/submit")
def submit(
    Question: str = Form(...),
    Answer: str = Form(...),
    #files: List[UploadFile] = File(...) # Dead File Uploader
):
    with open('sample.json', mode='r+', encoding='utf-8') as f:
     entry = [str(Question),str(Answer)]
     data = json.load(f)
     data.append(entry)
     f.seek(0)        # <--- should reset file position to the beginning.
     json.dump(data, f, indent=4)
     return {
        "JSON Payload ": {"Question": Question,"Answer": Answer},
        }
     

@app.get("/start/{pg}")
def start(request:Request,pg:int):
    with open('sample.json', mode='r', encoding='utf-8') as rf:
     entry = json.load(rf)
     if(len(entry) <= pg):
         raise Exception("Page Number Out Of Bounds")
     return templates.TemplateResponse("card.html",{"title":entry[0][0],"request":request,"q":entry[pg][0],"a":entry[pg][1],"pg":pg})

@app.get("/next",response_class=RedirectResponse)
def change(): 
 with open('sample.json', 'r+') as f:
    data = json.load(f)
    i = int(data[0][1]) + 1
    if(len(data) <= i):
         raise Exception("Page Number Out Of Bounds")
    data[0][1] = str(i)
    f.seek(0)        # <--- should reset file position to the beginning.
    json.dump(data, f, indent=4)
    return ("http://127.0.0.1:8000/start/"+str(i))

@app.on_event("startup")
async def startup_event():
    with open('sample.json', 'r+') as f:
        data = json.load(f)
        data[0][1] = "1"
        f.seek(0)
        json.dump(data, f, indent=4)

@app.post("/delete")
def delete(id : int = Form(...)):
    with open('sample.json',mode='r+',encoding='utf-8') as q:
        load = json.load(q)
        load.pop(id)
        with open('sample.json',mode='w',encoding='utf-8') as qt:
         json.dump(load,qt)
         return {
            "Card Deleted"
         }

@app.get("/randomize",response_class=RedirectResponse)
def random():
    with open('sample.json', 'r+') as f:
        data = json.load(f)
        rand = randint(0,len(data)-1)
        return ("http://127.0.0.1:8000/start/"+str(rand))


