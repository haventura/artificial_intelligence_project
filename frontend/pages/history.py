import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import pandas as pd
import numpy as np
import requests
import io
import dataclasses

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
    image: Image
    transcripts: list[str]

def main():
    st.set_page_config(page_title="Text Recognition", page_icon="✏️", layout="wide")
    st.title("✒️ Handwritten Text Recognition")
   
    st.write('<style>div.block-container{padding-top:1.2rem;}</style>', unsafe_allow_html=True)
    hide_footer_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """ 
    st.markdown(hide_footer_style, unsafe_allow_html=True) 
    st.caption("Made with Tensorflow and Streamlit by Andrea Ventura, Dawid Krasowski, Bartlomiej Drewnowski. <a href=https://github.com/haventura/artificial_intelligence_project>GitHub project</a>", unsafe_allow_html=True)

#def selectFileFromHistory(entry: HistoryEntry):

if __name__ == '__main__':
    main()