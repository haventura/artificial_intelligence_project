# Artificial Intelligence project

A short resume of the project

![Streamlit frontend](/images/streamlit_app.png)

## Installation

### With Docker

1. From the root folder, run `docker compose up`. This command will start building the images for the frontend and backend services. After building them, it will also create the related containers and start them.
1.  Once started, the streamlit application will be available at the following address: http://localhost:8501.

### Without Docker

1. You'll first have to install the python packages for the frontend and backend services, running `pip install -r requirements.txt` from within these two folders.
1. Once the packages are installed, you can start the backend service from within the `backend` folder using `python -m uvicorn main:app --reload`.
1. After the backend has succesfully started, the frontend can be started using `streamlit run main.py` from the `frontend` folder.
1. The streamlit application will be available at the following address: http://localhost:8501.

## Usage

The first step in using our app is to upload a `png`, `jpg` or `pdf` file to the file uploader located on the sidebar of the application (for `pdf`, only the first page will be rendered). After uploading a file, it will be rendered on your screen and you'll be able to freely draw rectangles encasing words, lines and paragraphs of text, or the whole file.

After ecompasing text within a rectangle, the Streamlit app sends a request to the backend service that transcribe the content of that rectangles and returns the formatted text. That text is displayed on the right-hand side of the aplication and is colored according to the color of the rectangle used to select that text. Several transcriptions can be made on the same image by drawing multiple rectangles; each results will be added under the previous ones.

After transcribing the desired text, a Download button enables the user to export the formatted text and download it as a text file, with each line in the file beeing the output of one transcription. The user can then upload another file and start a new transcription.

The application also feature a History tab, acessible from the sidebar, from which the user can see previously transcribed files and their formatted textual content.

## Architecture

![Steps](/images/steps.png)

The frontend application was created using the [Streamlit](https://streamlit.io/) framework, with a custom [drawable canvas](https://github.com/andfanilo/streamlit-drawable-canvas) component.

The transcription of an input image, selected as a rectangle by the user, is done in two steps:

1. First, the backend uses PyTorch to extract words from the input image, by dividing it in images of single words. These words are also ordered based on their coordinates on the original image. 
1. Then, Tensorflow is used to infer the content of each sub-image, concatenating each word as a single text and returning that transcribed text. 

Since the app is used only for inferance, and in order to reduce the backend image size, gpu support is not enabled; all inferance tasks are computed using the cpu.

### Word extraction from input image

The model used was developped by Harald Scheidl and is trained on the IAM dataset. It generates rectangular bounding boxes containing words from the original image. The coordinate of these bounding boxes are then used to extract those words into sub-images that are then fed one by one to the word transcription model.

A detailled description of the model can be found [here](https://githubharald.github.io/word_detector.html).

### Word transcription

The model used is a stripped down version of the model described by Harald Scheidl in his [Visual Computing Diploma thesis](https://repositum.tuwien.at/handle/20.500.12708/5409), called "SimpleHTR". Made using a neural network, this model consist of 5 convolutional NN layers, 2 recurrent NN layers using the popular Long Short-Term Memory implementation, and a a final Connectionist Temporal Classification (CTC) loss and decoding layer. 

This model is also trained on the IAM dataset, it takes as input an image of a single word of any size, resize it to fit the input RNN layer (adding blank space if necessary) and output the transcribed word as text.

The stripped down model is described in great details in this [Medium article](https://towardsdatascience.com/build-a-handwritten-text-recognition-system-using-tensorflow-2326a3487cd5).

### Reordering a multiline transcript

Each sub-image, containing a single word, that is extracted from the main image is associated with its coordinates within that image. Reordering the output words is done in two steps: First, the words are ordered based on their y coordinates, their vertical position on the original image. This ordered list is then clustered to group words in lines isolated from one another. Afterward, within each line, each words are ordered from left to right according to their x coordinate in the image. The lines are then concatenated and the result is an ordered text, from left to right and top to bottom.

## References

* [Harald Scheidl - Handwritten Text Recognition.](https://github.com/githubharald/SimpleHTR)
* [Harald Scheidl - Handwritten Word Detector.](https://github.com/githubharald/WordDetectorNN)
* [Streamlit - A faster way to build and share data apps.](https://streamlit.io/)
* [Streamlit Drawable Canvas.](https://github.com/andfanilo/streamlit-drawable-canvas)
* [TensorFlow - Create production-grade machine learning models.](https://www.tensorflow.org/)
* [PyTorch - An open source machine learning framework.](https://pytorch.org/)
* [IAM Handwriting Database](https://fki.tic.heia-fr.ch/databases/iam-handwriting-database)