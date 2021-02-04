import streamlit as st
import torchvision
from torchvision.datasets import CIFAR100
import os
import clip
import torch
import random
from PIL import Image
import os


@st.cache
def download_data():
    return CIFAR100(root=os.path.expanduser("~/.cache"), download=True, train=False)


if __name__ == '__main__':
    # dataset = torchvision.datasets.Places365(root=".",download=True)
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    query = st.text_input("Write your search query")
    text = clip.tokenize([query]).to(device)

    model, preprocess = clip.load("ViT-B/32")
    # cifar100 = download_data()
    orig_images = [Image.open("images/"+path) for path in os.listdir("images")]
    images = [preprocess(image).unsqueeze(0) for image in orig_images]
    images = torch.cat(images).to(device)

    with torch.no_grad():
        text_features = model.encode_text(text)
        images_features = model.encode_image(images)

    images_features /= images_features.norm(dim=-1, keepdim=True)
    text_features /= text_features.norm(dim=-1, keepdim=True)
    similarity = (100.0 * images_features @ text_features.T)
    topk = similarity.topk(k=2, dim=0)[1]
    st.text(torch.max(similarity, dim=0).values.item())
    st.image(orig_images[topk[0]], width=512)
    st.text(similarity[topk[1]].item())
    st.image(orig_images[topk[1]], width=512)
