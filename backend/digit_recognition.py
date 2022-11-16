# Imports PIL module 
from keras.models import load_model
from PIL import ImageGrab, Image
import numpy as np
from keras.utils import np_utils
from keras.datasets import mnist

if __name__ == "__main__":

    (x_train, y_train), (x_test, y_test) = mnist.load_data()

    x_test = x_test.reshape(10000, 784)
    x_test = x_test.astype('float32')
    x_test /= 255
    y_test = np_utils.to_categorical(y_test, 10)

    model = load_model('models/mnist.h5')

    score = model.evaluate(x_test, y_test, verbose=1)
    print('Test loss:', score[0])
    print('Test accuracy:', score[1])