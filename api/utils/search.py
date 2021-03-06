import clip
import numpy as np
import pandas as pd

img_features = np.load("features/features.npy")


def text_search(text_features):
    text_features = text_features.cpu().numpy()
    scores = (text_features @ img_features.T)[0]
    sorted_ids = scores.argsort()[::-1]
    return sorted_ids
