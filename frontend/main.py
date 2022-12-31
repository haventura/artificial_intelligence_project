import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import pandas as pd
import numpy as np
import requests
import io
import json

def main():
    st.set_page_config(page_title="Text Recognition", page_icon="🚀", layout="wide")
    st.title("Handwritten Text Recognition")

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
    if "transcript" not in st.session_state:
        st.session_state["transcript"] = []
    uploaded_image = col1.file_uploader("Text file:", type=["png", "jpg", "pdf"], accept_multiple_files=False)
    with col2:
        if(uploaded_image):
            background_image = Image.open(uploaded_image) 
            width = 500
            height = 500 
            if background_image.width >= background_image.height:
                ratio = width / background_image.width
                height = int(background_image.height * ratio)
            else:
                ratio = height / background_image.height
                width = int(background_image.width * ratio)
            canvas_result = st_canvas(
                fill_color = "rgba(0, 0, 0, 0.0)",
                stroke_color = COLORS[st.session_state["color_index"]],
                stroke_width = 2,
                background_image = background_image,
                width = width,
                height = height,
                drawing_mode = "rect",
                key = "canvas",
                display_toolbar = False,
            )
            
    with col3:
        st.header("Transcripts:")
        if uploaded_image is not None and canvas_result.json_data is not None:
            df = pd.json_normalize(canvas_result.json_data["objects"])
            if len(df) > 0:
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
                st.session_state["transcript"].append((COLORS[st.session_state["color_index"]], transcript))
                st.session_state["color_index"] += 1
                if(st.session_state["color_index"] >= len(COLORS)):
                    st.session_state["color_index"] = 0
                for value in st.session_state["transcript"]:
                    st.write('<p style="color:' + value[0] + ';">' + value[1] + '</p>', unsafe_allow_html=True)
        
    st.write('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
    hide_footer_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
    st.markdown(hide_footer_style, unsafe_allow_html=True) 
    st.caption("Made with Tensorflow and Streamlit by Andrea Ventura, Dawid Krasowski, Bartlomiej Drewnowski. <a href=https://github.com/haventura/artificial_intelligence_project>GitHub project</a>", unsafe_allow_html=True)

if __name__ == '__main__':
    main()