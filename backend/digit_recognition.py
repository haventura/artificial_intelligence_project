# Imports PIL module 
from keras.models import load_model
from PIL import ImageGrab, Image
import numpy as np
from keras.utils import np_utils
from keras.datasets import mnist
import cv2
import tensorflow as tf

def normalize_images(images):
    '''
    Channel-wise normalization of the input images: subtracted by mean and divided by std
    Args:
        images: 3-D array
    Returns:
        normalized images: 2-D array
    '''
    H, W = 28, 28
    images = np.reshape(images, (-1, H * W))
    numerator = images - np.expand_dims(np.mean(images, 1), 1)
    denominator = np.expand_dims(np.std(images, 1), 1)
    return np.reshape(numerator / (denominator + 1e-7), (-1, H, W))

def load_image():

    img = mnist.load_data()
    img = normalize_images(img)
    img = img.reshape(-1, 28, 28, 1)

    return img

def load_mnist():
    '''
    Load mnist data sets for training, validation, and test.
    Args:
        None
    Returns:
        (x_train, y_train): (4-D array, 2-D array)
        (x_val, y_val): (4-D array, 2-D array)
        (x_test, y_test): (4-D array, 2-D array)
    '''
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    x_train = normalize_images(x_train)
    x_test = normalize_images(x_test)

    x_train = x_train.reshape(-1, 28, 28, 1)
    x_test = x_test.reshape(-1, 28, 28, 1)
    y_train = np_utils.to_categorical(y_train) # encode one-hot vector
    y_test = np_utils.to_categorical(y_test)

    num_of_test_data = 50000
    x_val = x_train[num_of_test_data:]
    y_val = y_train[num_of_test_data:]
    x_train = x_train[:num_of_test_data]
    y_train = y_train[:num_of_test_data]

    return (x_train, y_train), (x_val, y_val), (x_test, y_test)

if __name__ == "__main__":

    # (x_train, y_train), (x_val, y_val), (x_test, y_test) = load_mnist()
    
    x = cv2.imread('2.png',cv2.IMREAD_GRAYSCALE)
    # x = x_test[9]
    # print(x_test.shape)
    print(x.shape)
    # x = np.expand_dims(x, axis=0)
    x = normalize_images(x)
    print(x.shape)
    model = load_model('models/ResNet164.h5')
    
    # 

    # score = model.evaluate(x_test, y_test, verbose=1)
    # print('Test loss:', score[0])
    # print('Test accuracy:', score[1])

    print(np.argmax(model(x).numpy()))
    #print(tf.math.argmax(model(x)))