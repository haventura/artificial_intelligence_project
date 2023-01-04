import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import requests
import io
import dataclasses
import codecs
import magic
import pdf2image

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

@dataclasses.dataclass
class HistoryEntry:
    name: str
    image: Image = None
    transcripts: list[str] = dataclasses.field(default_factory=list)

def main():
    st.set_page_config(page_title="Text Recognition", page_icon="🤖", layout="wide")
    st.title("✒️ Handwritten Text Recognition")

    col1, col2 = st.columns([2,1])
    COLORS = [
        "#53bfc5",
        "#2b58b1",
        "#61c648",
        "#ffe86a",
        "#de4d8b",
        "#f68d8a",
        "#615279",
        "#a71930",
    ]

    if "color_index" not in st.session_state:
        st.session_state["color_index"] = 0
    if "transcript" not in st.session_state:
        st.session_state["transcript"] = []
    if "history" not in st.session_state:
        st.session_state["history"] = []
    if "prevent_transcript" not in st.session_state:
        st.session_state["prevent_transcript"] = False
    if "previous_upload" not in st.session_state:
        st.session_state["previous_upload"] = None
    if "image_width" not in st.session_state:
        st.session_state["image_width"] = 500

    with fragile(st.sidebar):
        st.header("📜 Input File")
        
        uploaded_file = st.file_uploader("Drop a file containing handwritten text here:",type=["png", "jpg", "pdf"], accept_multiple_files=False)
        if uploaded_file is None:
            st.session_state["image_width"] = st.slider("Image Width", 500, 1000, 500, 100)
        # st.subheader("📖 History")
        # if st.session_state["history"] == []:
        #     st.caption("Your transcripts history will appear here.")
        #     raise fragile.Break
        # for entry in st.session_state["history"]:
        #     st.button(entry.name, on_click=selectFileFromHistory, args=(entry))

    with fragile(col1):
        if uploaded_file is None:
            st.caption("Once uploaded, your file will appear here. Draw boxes on it to transcribe their content.")
            raise fragile.Break
        if uploaded_file != st.session_state["previous_upload"]:
            st.session_state["color_index"] = 0
            if st.session_state["previous_upload"] != None:
                preventNextTranscription()
            st.session_state["transcript"] = []
            st.session_state["previous_upload"] = uploaded_file
            st.session_state["history"].append(HistoryEntry(name=uploaded_file.name.split(".")[0])) 
        uploaded_file_bytes = uploaded_file.read()
        if magic.from_buffer(uploaded_file_bytes, mime=True) == 'application/pdf':
            background_image = pdf2image.convert_from_bytes(uploaded_file_bytes)[0]
        else:
            background_image = Image.open(uploaded_file) 
        width, height, ratio = scaleImage(background_image,st.session_state["image_width"])
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

    with fragile(col2):
        st.header("🖨️ Transcripts")
        if uploaded_file is None or canvas_result.json_data is None or len(canvas_result.json_data["objects"]) == 0:
            st.caption("Your transcription results will appear here. You'll be able to download the result as a text file.")
            if uploaded_file and canvas_result.json_data:
                st.session_state["color_index"] += 1
            raise fragile.Break
        if st.session_state["prevent_transcript"]:
            st.session_state["prevent_transcript"] = False
        else:
            crop_data = canvas_result.json_data["objects"][-1]     
            cropped_image = cropImage(background_image, crop_data, ratio)
            transcript = transcribeImage(cropped_image)
            st.session_state["transcript"].append((COLORS[st.session_state["color_index"]-1], transcript))
            st.session_state["history"][-1].transcripts.append(transcript)
            if canvas_result.image_data is not None:
                image_data = canvas_result.image_data
                st.session_state["history"][-1].image = Image.fromarray(image_data.astype("uint8"), mode="RGBA")          
        st.session_state["color_index"] += 1
        if(st.session_state["color_index"] >= len(COLORS)):
            st.session_state["color_index"] = 0
        output_data = ""
        for value in st.session_state["transcript"]:
            st.write('<p style="color:' + value[0] + ';">' + value[1] + '</p>', unsafe_allow_html=True)    
            output_data += (value[1] + "\n") 
        st.download_button("Download", data=codecs.encode(output_data), file_name=st.session_state["history"][-1].name + ".txt", on_click=preventNextTranscription)
        
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
    width = size
    ratio = width / image.width
    height = int(image.height * ratio)
    return width, height, ratio

def cropImage(image, crop_data, ratio):
    left = crop_data["left"] * (1/ratio)
    top = crop_data["top"] * (1/ratio)
    right = left + crop_data["width"] * (1/ratio)
    bottom = top + crop_data["height"] * (1/ratio)             
    return image.crop((left, top, right, bottom))

def transcribeImage(image):
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()     
    response = requests.post('http://backend:8000/uploadfile/', files = {'file': img_byte_arr})
    return response.json()["content"]

def preventNextTranscription():
    st.session_state["prevent_transcript"]=True


#def selectFileFromHistory(entry: HistoryEntry):


if __name__ == '__main__':
    main()