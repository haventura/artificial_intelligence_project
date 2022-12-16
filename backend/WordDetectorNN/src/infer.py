import torch
from path import Path

from .dataloader import DataLoaderImgFile
from .eval import evaluate
from .net import WordDetectorNet
from .visualization import crop_image
from .aabb import AABB

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