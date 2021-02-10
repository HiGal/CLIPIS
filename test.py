import requests
from PIL import Image
import base64
import json
import io

if __name__ == '__main__':
    with open("images/1.jpg", "rb") as f:
        image = f.read()
    # buffered = io.BytesIO()
    # image.save(buffered, format="JPEG")
    im = base64.b64encode(image)
    base64string = im.decode('utf-8')
    data = {
        "img": base64string
    }
    data = json.dumps(data, indent=2)
    r = requests.post("http://127.0.0.1:5000/encode/image", data=data)
    assert r.status_code == 200

    data = {
        "text": "a blue colored star"
    }
    r = requests.post("http://127.0.0.1:5000/encode/text", data=json.dumps(data))
    assert r.status_code == 200