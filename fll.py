from flask import Flask, render_template, request
import requests
import json


app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def hello_world():
    if request.method == "POST":
        text = request.form['search']
        url = "https://stablediffusionapi.com/api/v3/text2img/"

        payload = json.dumps({
        "key": "your_api_key",
        "prompt": f"{text}",
        "negative_prompt": None,
        "width": "512",
        "height": "512",
        "samples": "1",
        "num_inference_steps": "20",
        "seed": None,
        "guidance_scale": 7.5,
        "safety_checker": "yes",
        "multi_lingual": "no",
        "panorama": "no",
        "self_attention": "no",
        "upscale": "no",
        "embeddings_model": None,
        "webhook": None,
        "track_id": None
        })

        headers = {
        'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        print(type(response.text))
        print(response.text)

        response = json.loads(response.text)

        if response['status'] == "error" or response['status'] == "processing":
            img = 'static/eerr.jpg'

        else:
            img = response['output'][0]
        # print(img)

        return render_template("main.html", img=img)
    
    return render_template("main.html", img="static/eerr.jpg")


app.run(debug=True)