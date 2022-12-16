from typing import Union
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile
import time
import json
from SimpleHTR.src.inference import infer
from SimpleHTR.src.model import Model
from WordDetectorNN.src.infer import word_extractor
import dataclasses
import os
import scipy.spatial.distance as distance

class FilePaths:
    """Filenames and paths to data."""
    fn_output = 'output/output.json'
    fn_char_list = 'SimpleHTR/model/charList.txt'

@dataclasses.dataclass
class TextData:
    content: str

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

@app.post("/uploadfile/")
async def create_file(file: bytes = File()):
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    dirname = os.path.dirname(__file__)
    main_image_folder_path = os.path.join(dirname, f'data/{timestamp}')
    sub_images_folder_path = os.path.join(dirname, f'data/{timestamp}/sub_images')
    os.mkdir(main_image_folder_path)
    os.mkdir(sub_images_folder_path)

    image_name = f'{timestamp}.jpg'
    f = open(f'data/{timestamp}/{image_name}', 'wb')
    f.write(file)
    f.close()

    word_extractor(f"data/{timestamp}", f"data/{timestamp}/sub_images")
    
    text = ""
    for filename in os.listdir(sub_images_folder_path):
        print(filename)
        recognized, probability = infer(model, f'{sub_images_folder_path}/{filename}')
        text += (recognized + " ")

    text_data = TextData(text)
    return text_data