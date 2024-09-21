from fastapi import FastAPI, File, UploadFile, Form, Request  
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from .database import init_qdrant
from .embedding import embed_document
from .compliance_checker import check_compliance
from .database import init_qdrant, store_embedding 

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
async def startup_event():
    init_qdrant()

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload")
async def upload_documents(
    request: Request,  
    policy: UploadFile = File(...),
    standard: UploadFile = File(...)
):
    policy_text = await policy.read()
    standard_text = await standard.read()
    
    policy_embedding = embed_document(policy_text)
    standard_embedding = embed_document(standard_text)
    
    # Store embeddings in Qdrant
    await store_embedding(policy_embedding, policy.filename)
    await store_embedding(standard_embedding, standard.filename)

    compliance_results = check_compliance(policy_embedding, standard_embedding)
    
    return templates.TemplateResponse("results.html", {
        "request": request,
        "results": compliance_results
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)