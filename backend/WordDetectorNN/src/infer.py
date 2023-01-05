import torch
from path import Path
import cv2
import numpy as np

from .dataloader import DataLoaderImgFile
from .eval import evaluate
from .net import WordDetectorNet

def word_extractor( src, dest, device = 'cpu' ):
    
    net = WordDetectorNet()
    net.load_state_dict(torch.load('./WordDetectorNN/model/weights', map_location=device))

    net.eval()
    net.to(device)
    loader = DataLoaderImgFile(Path(src), net.input_size,device)
    res = evaluate(net, loader, max_aabbs=1000)

    for i, (img, aabbs) in enumerate(zip(res.batch_imgs, res.batch_aabbs)):
        f = loader.get_scale_factor(i)
        aabbs = order_aabbs(aabbs)
        aabbs = [aabb.scale(1 / f, 1 / f) for aabb in aabbs]
        img = loader.get_original_img(i)       
        crop_image(img, aabbs, dest, 5)

def crop_image(img, aabbs, dest, margin=5):
    word_count = 0

    for aabb in aabbs:
        word_count += 1

        xmin = int(aabb.xmin)-margin
        xmax = int(aabb.xmax)+margin
        ymin = int(aabb.ymin)-margin
        ymax = int(aabb.ymax)+margin
        cropped_image = img[ymin:ymax,xmin:xmax]
        if(not np.any(cropped_image)):
            cropped_image = img[int(aabb.ymin):int(aabb.ymax),int(aabb.xmin):int(aabb.xmax)]
        # https://stackoverflow.com/questions/19239381/pyplot-imsave-saves-image-correctly-but-cv2-imwrite-saved-the-same-image-as
        #cropped_image = cv2.convertScaleAbs(cropped_image, alpha=(255.0))
        cropped_image = cv2.normalize(cropped_image, dst=None, alpha=0, beta=255,norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        cv2.imwrite(f'{dest}/file{word_count:03d}.png', cropped_image)

def order_aabbs(aabbs):
    new_aabbs = []
    words_middle_point = {}
    word_height_sum = 0
    for index, aabb in enumerate(aabbs):
        ymin = aabb.ymin
        ymax = aabb.ymax
        word_height_sum += ymax-ymin
        middle_point = (ymax-ymin)/2+ymin
        words_middle_point[middle_point] = aabb
    average_word_height = word_height_sum / (index+1)
    clusters = cluster_words_in_line(words_middle_point, average_word_height/2)
    new_aabbs = order_aabbs_from_clusters(clusters)
    return new_aabbs

def cluster_words_in_line(words, average_word_height):
    clusters = []
    eps = average_word_height
    points_sorted = sorted(words.items())
    curr_point = points_sorted[0]
    curr_cluster = [curr_point]
    for point in points_sorted[1:]:
        if point[0] <= curr_point[0] + eps:
            curr_cluster.append(point)
        else:
            clusters.append(curr_cluster)
            curr_cluster = [point]
        curr_point = point
    clusters.append(curr_cluster)
    return clusters

def order_aabbs_from_clusters(clusters):
    global_ordered_words = []
    for cluster in clusters:
        words_leftmost_point = {}
        for word in cluster:
            xmin = word[1].xmin
            words_leftmost_point[xmin] = word[1]
        words_sorted = sorted(words_leftmost_point.items())
        for sorted_word in words_sorted:
            global_ordered_words.append(sorted_word[1])
    return global_ordered_words