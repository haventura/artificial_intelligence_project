from typing import Union
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile
import time
import json
from SimpleHTR.src.inference import infer
from SimpleHTR.src.model import Model
import dataclasses

class FilePaths:
    """Filenames and paths to data."""
    fn_output = 'output/output.json'
    fn_char_list = 'model/charList.txt'

@dataclasses.dataclass
class TextData:
    color: str
    content: str

@dataclasses.dataclass
class ResponseData:
    img_name: str
    img_url: str
    text_data: list[TextData]

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

@app.on_event("startup")
async def startup_event():
    with open(FilePaths.fn_char_list) as f:
        global model
        model = Model(list(f.read()))

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/images/{image_id}")
def read_image(image_id: int):
    return {"image_id": image_id}

@app.post("/uploadfile/")
async def create_file(file: bytes = File()):
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f'{timestamp}.png'
    f = open(f'data/{filename}', 'wb')
    f.write(file)
    f.close()

    recognized, probability = infer(model, f'data/{filename}')
    text_data = [TextData("#ff00ff",recognized), TextData("#ff00ff",recognized)]
    response_data = ResponseData("nom de l'image", "une url", text_data)
    with open(FilePaths.fn_output, 'w') as f:
        json.dump(dataclasses.asdict(response_data),f)
    return response_data