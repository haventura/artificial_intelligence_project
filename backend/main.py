from typing import Union
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile
import time

app = FastAPI()

origins = [
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/images/{image_id}")
def read_image(image_id: int):
    return {"image_id": image_id}

@app.post("/uploadfile/")
async def create_file(file: bytes = File()):
    ts = time.strftime("%Y%m%d-%H%M%S")
    f = open(f'{ts}.jpg', 'wb')
    f.write(file)
    f.close()
    return {"file_size": len(file)}

# @app.post("/uploadfile/")
# async def create_upload_file(file: UploadFile):
#     return {"filename": file.filename}