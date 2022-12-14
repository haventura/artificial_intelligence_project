import argparse

import torch
from path import Path

from .dataloader import DataLoaderImgFile
from .eval import evaluate
from .net import WordDetectorNet
from .visualization import crop_image

def word_extractor( src, dest, device = 'cpu' ):
    
    net = WordDetectorNet()
    net.load_state_dict(torch.load('./WordDetectorNN/model/weights', map_location=device))

    net.eval()
    net.to(device)
    loader = DataLoaderImgFile(Path(src), net.input_size,device)
    res = evaluate(net, loader, max_aabbs=1000)

    for i, (img, aabbs) in enumerate(zip(res.batch_imgs, res.batch_aabbs)):
        f = loader.get_scale_factor(i)
        aabbs = [aabb.scale(1 / f, 1 / f) for aabb in aabbs]
        img = loader.get_original_img(i)
        
        crop_image(img, aabbs, dest, 3)