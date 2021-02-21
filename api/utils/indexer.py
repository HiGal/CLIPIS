from PIL import Image
import io
import base64
import torch
import pymongo


def index_one_image(image_base64, image_name, model, preprocess, device='cpu'):
    img = Image.open(io.BytesIO(base64.b64decode(image_base64)))
    image = [preprocess(img).unsqueeze(0)]
    image = torch.cat(image).to(device)
    name, extension = image_name.split(".")
    with torch.no_grad():
        image_features = model.encode_image(image)
    image_features /= image_features.norm(dim=-1, keepdim=True)

    client = pymongo.MongoClient('files_db', 27017)
    db = client.image_db
    image_collection = db.image_data
    image_collection.insert_one({
        name: {
            "feature": image_features[0].cpu().numpy().tolist(),
            "extension": extension
        }
    })
    client.close()


def index_many_images(image_base64_list, image_name_list, model, preprocess, device='cpu'):
    image = [preprocess(Image.open(io.BytesIO(base64.b64decode(image_base64)))).unsqueeze(0) for image_base64 in image_base64_list]
    image = torch.cat(image).to(device)
    names_extensions = [image_name.split(".") for image_name in image_name_list]
    with torch.no_grad():
        image_features = model.encode_image(image)
    image_features /= image_features.norm(dim=-1, keepdim=True)

    candidates_to_insert = []

    for i, image_feature in enumerate(image_features):
        name, extension = names_extensions[i]
        candidates_to_insert.append({
            name:{
                "feature": image_feature.cpu().numpy().tolist(),
                "extension": extension
            }
        })
    client = pymongo.MongoClient('files_db', 27017)
    db = client.image_db
    image_collection = db.image_data
    image_collection.insert_many(candidates_to_insert)
    client.close()
