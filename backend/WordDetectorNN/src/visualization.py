import cv2
import matplotlib.pyplot as plt
import numpy as np

def visualize(img, aabbs):
    img = ((img + 0.5) * 255).astype(np.uint8)
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    for aabb in aabbs:
        aabb = aabb.enlarge_to_int_grid().as_type(int)
        cv2.rectangle(img, (aabb.xmin, aabb.ymin), (aabb.xmax, aabb.ymax), (255, 0, 255), 2)

    return img

def crop_image(img, aabbs, dest):
    plt.imshow(img, cmap='gray')
    word_count = 0

    for aabb in aabbs:
        word_count += 1

        xmin = int(aabb.xmin)
        xmax = int(aabb.xmax)
        ymin = int(aabb.ymin)
        ymax = int(aabb.ymax)

        cropped_image = img[ymin:ymax,xmin:xmax ]

        # https://stackoverflow.com/questions/19239381/pyplot-imsave-saves-image-correctly-but-cv2-imwrite-saved-the-same-image-as
        cropped_image = cv2.convertScaleAbs(cropped_image, alpha=(255.0))
        cv2.imwrite(f'{dest}/file{str(word_count)}.png', cropped_image)

    return word_count