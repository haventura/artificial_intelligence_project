import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import pandas as pd
import numpy as np
import requests
import io

class fragile(object):
    class Break(Exception):
      """Break out of the with statement"""

    def __init__(self, value):
        self.value = value

    def __enter__(self):
        return self.value.__enter__()

    def __exit__(self, etype, value, traceback):
        error = self.value.__exit__(etype, value, traceback)
        if etype == self.Break:
            return True
        return error

def main():
    st.set_page_config(page_title="Text Recognition", page_icon="✏️", layout="wide")
    st.title("✒️ Handwritten Text Recognition")

    col1, col2, col3 = st.columns([1,2,1])
    # image_placeholder = col2.empty()
    COLORS = [
        "#53bfc5",
        "#2b58b1",
        "#61c648",
        "#ffe86a",
        "#de4d8b",
        "#f68d8a"
    ]

    if "color_index" not in st.session_state:
        st.session_state["color_index"] = 0
    print(st.session_state["color_index"])
    if "transcript" not in st.session_state:
        st.session_state["transcript"] = []

    with col1:
        st.header("📜 Input File")
        uploaded_file = st.file_uploader("Drop a file containing handwritten text here:",type=["png", "jpg", "pdf"], accept_multiple_files=False)
    
    with fragile(col2):
        if uploaded_file is None:
            raise fragile.Break
        background_image = Image.open(uploaded_file) 
        width, height, ratio = scaleImage(background_image,500)
        canvas_result = st_canvas(
            fill_color = "rgba(0, 0, 0, 0.0)",
            stroke_color = COLORS[st.session_state["color_index"]-1],
            stroke_width = 2,
            background_image = background_image,
            width = width,
            height = height,
            drawing_mode = "rect",
            key = "canvas",
            display_toolbar = False,
        )

    with fragile(col3):
        st.header("🖨️ Transcripts")
        if uploaded_file is None:
            raise fragile.Break
        if canvas_result.json_data is None:
            
            raise fragile.Break
        df = pd.json_normalize(canvas_result.json_data["objects"])
       
        if len(df) == 0:
            st.session_state["color_index"] += 1
            raise fragile.Break
        crop_result = canvas_result.json_data["objects"][-1]
        left = crop_result["left"] * (1/ratio)
        top = crop_result["top"] * (1/ratio)
        right = left + crop_result["width"] * (1/ratio)
        bottom = top + crop_result["height"] * (1/ratio)             
        cropped_image = background_image.crop((left, top, right, bottom))
        img_byte_arr = io.BytesIO()
        cropped_image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()     
        response = requests.post('http://localhost:8000/uploadfile/', files = {'file': img_byte_arr})
        transcript = response.json()["content"]
        st.session_state["transcript"].append((COLORS[st.session_state["color_index"]-2], transcript))
        for value in st.session_state["transcript"]:
            st.write('<p style="color:' + value[0] + ';">' + value[1] + '</p>', unsafe_allow_html=True)
        st.session_state["color_index"] += 1
        if(st.session_state["color_index"] >= len(COLORS)):
            st.session_state["color_index"] = 0
        
    st.write('<style>div.block-container{padding-top:1.2rem;}</style>', unsafe_allow_html=True)
    hide_footer_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
    st.markdown(hide_footer_style, unsafe_allow_html=True) 
    st.caption("Made with Tensorflow and Streamlit by Andrea Ventura, Dawid Krasowski, Bartlomiej Drewnowski. <a href=https://github.com/haventura/artificial_intelligence_project>GitHub project</a>", unsafe_allow_html=True)

def scaleImage(image, size):
    if image.width >= image.height:
        width = size
        ratio = width / image.width
        height = int(image.height * ratio)
        return width, height, ratio
    else:
        height = size
        ratio = height / image.height
        width = int(image.width * ratio)
        return width, height, ratio

if __name__ == '__main__':
    main()