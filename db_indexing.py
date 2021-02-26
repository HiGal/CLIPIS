import clip
import numpy as np
import torch
from PIL import Image
from tqdm import tqdm
import pandas as pd
import os
import math
import glob


def create_dataframe(data_root, csv_out_path):
    data = {'filename': [], "filepath": []}
    data['filename'] = os.listdir(data_root)
    data['filepath'] = [f"{data_root}/{filename}" for filename in os.listdir(data_root)]
    df = pd.DataFrame.from_dict(data)
    df.to_csv(f"{csv_out_path}/files.csv")
    print("Done!")
    return df


def compute_clip_features(photos_batch):
    # Load all the photos from the files
    photos = [Image.open(photo_file) for photo_file in photos_batch]

    # Preprocess all photos
    photos_preprocessed = torch.stack([preprocess(photo) for photo in photos]).to(device)

    with torch.no_grad():
        # Encode the photos batch to compute the feature vectors and normalize them
        photos_features = model.encode_image(photos_preprocessed)
        photos_features /= photos_features.norm(dim=-1, keepdim=True)

    # Transfer the feature vectors back to the CPU and convert to numpy
    return photos_features.cpu().numpy()


def create_image_features(img_root_folder, features_folder, batch_size):
    photos_files = [f"{img_root_folder}/{filename}" for filename in os.listdir(img_root_folder)]
    batches = math.ceil(len(photos_files) / batch_size)
    pbar = tqdm(range(batches))
    if not os.path.exists(features_folder):
        os.makedirs(features_folder)
    for i in pbar:
        batch_filenames_path = f"{features_folder}/{i:010d}.csv"
        batch_features_path = f"{features_folder}/{i:010d}.npy"

        if not os.path.exists(batch_features_path):
            try:
                batch_files = photos_files[i * batch_size: (i + 1) * batch_size]
                batch_features = compute_clip_features(batch_files)
                np.save(batch_features_path, batch_features)

                photo_data = pd.DataFrame(batch_files, columns=["photo_path"])
                photo_data.to_csv(batch_filenames_path, index=False)
            except:
                print(f'Problem with batch {i}')


def concat_batches(features_folder):
    features_list = [np.load(features_file) for features_file in sorted(glob.glob(f"{features_folder}/*.npy"))]
    features = np.concatenate(features_list)
    np.save(f"{features_folder}/features.npy", features)

    photo_files = pd.concat([pd.read_csv(ids_file) for ids_file in sorted(glob.glob(f"{features_folder}/*.csv"))])
    photo_files.to_csv(f"{features_folder}/files.csv", index=False)


if __name__ == '__main__':
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load("ViT-B/32", device=device)

    features_folder = "features"
    root_path = "images"
    batch_size = 32
    if not os.path.exists(features_folder):
        create_image_features(root_path, features_folder, batch_size)
    concat_batches(features_folder)

    # if not os.path.exists(data_csv):
    #     df = create_dataframe(root_path, "./")
    # else:
    #     df = pd.read_csv(data_csv)
