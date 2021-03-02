from fastapi import FastAPI, Request, Response
import clip
import torch
import json

from utils.search import text_search
from utils.indexer import index_one_image, index_many_images, get_img_features
from body_models import Image, ImageBatch
import faiss
import pandas as pd

app = FastAPI()
faiss_index = faiss.read_index("features/image_index")
files = pd.read_csv("features/files.csv")


@app.post("/encode/image", summary="Index one image")
async def encode_image(data: Image):
    print(data)
    img_name = data.name
    data = data.base64img.encode('ascii')
    index_one_image(data, img_name, model, preprocess, device)
    return Response("Successful", status_code=200)


@app.post("/encode/images", summary="Index multiple images at once")
async def encode_images(data: ImageBatch):
    image_base64_list = data.img_list
    image_names = data.img_names
    index_many_images(image_base64_list, image_names, model, preprocess, device)
    return Response("Successful", status_code=200)


@app.post("/text/search", summary="Perform a search using string input")
async def search_by_text(request: Request):
    data = json.loads(await request.body())
    text_input = data['text']
    tokens = clip.tokenize([text_input]).to(device)
    with torch.no_grad():
        text_features = model.encode_text(tokens)
    text_features /= text_features.norm(dim=-1, keepdim=True)
    sorted_ids = text_search(text_features)
    results = files['photo_path'].iloc[sorted_ids].values.tolist()
    answer = {
        "results": results
    }
    return Response(json.dumps(answer), status_code=200)


@app.post("/image/search", summary="Perform a search using base64 image input")
async def search_by_image(request: Request):
    data = json.loads(await request.body())
    image_base64 = data['base64img'].encode('ascii')
    image_features = get_img_features(image_base64, model, preprocess, device).cpu().numpy()
    image_features = image_features.astype("float32")
    _, ids = faiss_index.search(image_features, k=50)
    results = files['photo_path'].iloc[ids[0]].values.tolist()
    answer = {
        "results": results
    }
    return Response(json.dumps(answer), status_code=200)

device = "cuda:0" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32")
model.to(device)
