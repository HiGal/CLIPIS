from fastapi import FastAPI, Request, Response
import clip
import torch
import json
from utils.indexer import index_one_image, index_many_images
from body_models import Image, ImageBatch

app = FastAPI()


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


@app.post("/encode/text", summary="Encode search query")
async def encode_text(request: Request):
    data = json.loads(await request.body())
    text_input = data['text']
    tokens = clip.tokenize([text_input]).to(device)
    with torch.no_grad():
        text_features = model.encode_text(tokens)
    text_features /= text_features.norm(dim=-1, keepdim=True)
    return Response("Success", status_code=200)


device = "cuda:0" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32")
model.to(device)
