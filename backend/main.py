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
    text_data: 'list[TextData]'

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

    #create subfolder in data/ with timestamp as name
    #this folder will contain the main uploaded image file and all subwords image files
    dirname = os.path.dirname(__file__)
    main_image_folder_path = os.path.join(dirname, f'data/{timestamp}')
    sub_images_folder_path = os.path.join(dirname, f'data/{timestamp}/sub_images')
    os.mkdir(main_image_folder_path)
    os.mkdir(sub_images_folder_path)

    filename = f'{timestamp}.png'
    f = open(f'data/{filename}', 'wb')
    f.write(file)
    f.close()

    # Call Dawid's word detector function, passing the main image file
    word_count = word_extractor(f"data/{timestamp}", f"data/{timestamp}/sub_images")
    # Dawid will make sure that each subimage is labelled orderly
    # Then loop over each sub_image, transcribe them one by one and append each word to a list.

    # list[dawidReturnedColor], list[paragraphFolderName]
    # or a list of dictionnaries?
    # a 2-D array of colors and associated folder (will only contain 1 entry for a start)
    # dico = {colors: [color 1, color 2, color 3], folders: [paragraphfolder1, paragraphfolder2, paragraphfolder3]}

    # text_data = []
    # For i in len(dico[folders]):
    # 
    #   color = dico[colors][i]
    #   For each image in dico[folders][i]:
    #   recognized, probability = infer(model, f'data/{timestamp}/{subfolder}/{image}')
    #   data = TextData(color, recognized)
    #   text_data.append(data)
    #   
    # response_data = ResponseData("nom de l'image", "une url", text_data)
    text = ""
    for filename in os.listdir(sub_images_folder_path):
        recognized, probability = infer(model, f'{sub_images_folder_path}/{filename}')
        text += (recognized + " ")

    text_data = [TextData("#ff00ff",text), TextData("#ff00ff",text)]
    response_data = ResponseData("nom de l'image", "une url", text_data)
    #with open(FilePaths.fn_output, 'w') as f:
    #    json.dump(dataclasses.asdict(response_data),f)
    return response_data