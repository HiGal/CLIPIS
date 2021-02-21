from fastapi import FastAPI, Request,Response
import clip
import torch
from PIL import Image
import json
from utils.indexer import index_one_image, index_many_images

app = FastAPI()


@app.route("/encode/image", methods=["POST"])
async def encode_image(request: Request):
    data = json.loads(await request.body())
    print(data)
    img_name = data['name']
    data = data['img'].encode('ascii')
    index_one_image(data, img_name, model, preprocess, device)
    return Response("Successful", status_code=200)


@app.route("/encode/images", methods=["POST"])
async def encode_images(request: Request):
    data = json.loads(await request.body())
    image_base64_list = data['img_list']
    image_names = data['img_names']
    index_many_images(image_base64_list, image_names, model, preprocess, device)
    return Response("Successful", status_code=200)


@app.route("/encode/text", methods=['POST'])
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
