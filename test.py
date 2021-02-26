import requests
import base64
import json
import os

if __name__ == '__main__':
    ####################################################################################################################
    #                                         Test indexing of one image                                               #
    ####################################################################################################################
    with open("images/2.jpg", "rb") as f:
        image = f.read()
    # buffered = io.BytesIO()
    # image.save(buffered, format="JPEG")
    im = base64.b64encode(image)
    base64string = im.decode('utf-8')
    data = {
        "base64img": base64string,
        "name": "2.jpg"
    }
    data = json.dumps(data, indent=2)
    r = requests.post("http://84.201.156.50/encode/image", data=data)
    assert r.status_code == 200

    ####################################################################################################################
    #                                        Test indexing of many images                                              #
    ####################################################################################################################
    image_base64_list = []
    image_names = []
    for img_name in os.listdir("images"):
        with open(f"images/{img_name}", "rb") as f:
            image = f.read()
        im = base64.b64encode(image)
        base64string = im.decode('utf-8')
        image_names.append(img_name)
        image_base64_list.append(base64string)
    data = {
        "img_list": image_base64_list,
        "img_names": image_names
    }
    data = json.dumps(data, indent=2)
    r = requests.post("http://84.201.156.50/encode/images", data=data)
    assert r.status_code == 200

    data = {
        "text": "a blue colored star"
    }
    r = requests.post("http://84.201.156.50/encode/text", data=json.dumps(data))
    assert r.status_code == 200
