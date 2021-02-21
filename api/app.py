from flask import Flask, request, Response
import clip
import torch
from PIL import Image
import json
from utils.indexer import index_one_image, index_many_images

app = Flask(__name__)


@app.route("/encode/image", methods=["POST"])
def encode_image():
    data = json.loads(request.data)
    img_name = data['name']
    data = data['img'].encode('ascii')
    index_one_image(data, img_name, model, preprocess, device)
    return Response("Successful", status=200)


@app.route("/encode/images", methods=["POST"])
def encode_images():
    data = json.loads(request.data)
    image_base64_list = data['img_list']
    image_names = data['img_names']
    index_many_images(image_base64_list, image_names, model, preprocess, device)
    return Response("Successful", status=200)


@app.route("/encode/text", methods=['POST'])
def encode_text():
    data = json.loads(request.data)
    text_input = data['text']
    tokens = clip.tokenize([text_input]).to(device)
    with torch.no_grad():
        text_features = model.encode_text(tokens)
    text_features /= text_features.norm(dim=-1, keepdim=True)
    return Response("Success", status=200)


if __name__ == '__main__':
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load("ViT-B/32")
    model.to(device)
    app.run()
