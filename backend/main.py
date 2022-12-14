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

    #create subfolder in data/ with timestamp as name
    #this folder will contain the main uploaded image file and all subwords image files
    dirname = os.path.dirname(__file__)
    main_image_folder_path = os.path.join(dirname, f'data/{timestamp}')
    sub_images_folder_path = os.path.join(dirname, f'data/{timestamp}/sub_images')
    os.mkdir(main_image_folder_path)
    os.mkdir(sub_images_folder_path)

    image_name = f'{timestamp}.jpg'
    f = open(f'data/{timestamp}/{image_name}', 'wb')
    f.write(file)
    f.close()

    aabbs = word_extractor(f"data/{timestamp}", f"data/{timestamp}/sub_images")
    
    text = ""
    transcribed_word = []
    for filename in os.listdir(sub_images_folder_path):
        print(filename)
        recognized, probability = infer(model, f'{sub_images_folder_path}/{filename}')
        #transcribed_word.append(recognized)
        text += (recognized + " ")
    """
    boxes = []
    i = 0
    for aabb in aabbs:
        point = [transcribed_word[i], [
            [aabb.xmin, aabb.ymin],
            [aabb.xmax, aabb.ymin],
            [aabb.xmax, aabb.ymax],
            [aabb.xmin, aabb.ymax]]]
        boxes.append(point)
    print(boxes)

    boxes = sorting_bounding_box(boxes)
    print(boxes)
    for point in boxes:
        text += (point + " ")
    """

    text_data = TextData(text)
    #with open(FilePaths.fn_output, 'w') as f:
    #    json.dump(dataclasses.asdict(response_data),f)
    return text_data

def sorting_bounding_box(points):
    
    points = list(map(lambda x:[x[0],x[1][0],x[1][2]],points))
    # print(points)
    points_sum = list(map(lambda x: [x[0],x[1],sum(x[1]),x[2][1]],points))
    x_y_cordinate = list(map(lambda x: x[1],points_sum))
    final_sorted_list = []
    while True:
        try:
            new_sorted_text = []
            initial_value_A  = [i for i in sorted(enumerate(points_sum), key=lambda x:x[1][2])][0]
    #         print(initial_value_A)
            threshold_value = abs(initial_value_A[1][1][1] - initial_value_A[1][3])
            threshold_value = (threshold_value/2) + 5
            del points_sum[initial_value_A[0]]
            del x_y_cordinate[initial_value_A[0]]
    #         print(threshold_value)
            A = [initial_value_A[1][1]]
            K = list(map(lambda x:[x,abs(x[1]-initial_value_A[1][1][1])],x_y_cordinate))
            K = [[count,i]for count,i in enumerate(K)]
            K = [i for i in K if i[1][1] <= threshold_value]
            sorted_K = list(map(lambda x:[x[0],x[1][0]],sorted(K,key=lambda x:x[1][1])))
            B = []
            points_index = []
            for tmp_K in sorted_K:
                points_index.append(tmp_K[0])
                B.append(tmp_K[1])
            dist = distance.cdist(A,B)[0]
            d_index = [i for i in sorted(zip(dist,points_index), key=lambda x:x[0])]
            new_sorted_text.append(initial_value_A[1][0])

            index = []
            for j in d_index:
                new_sorted_text.append(points_sum[j[1]][0])
                index.append(j[1])
            for n in sorted(index, reverse=True):
                del points_sum[n]
                del x_y_cordinate[n]
            final_sorted_list.append(new_sorted_text)
            # print(new_sorted_text)
        except Exception as e:
            print(e)
            break

    return final_sorted_list