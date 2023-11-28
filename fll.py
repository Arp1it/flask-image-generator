from flask import Flask, render_template, request
import requests
import json
from openai import OpenAI


app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def hello_world():
    if request.method == "POST":
        text = request.form['search']
        url = "https://stablediffusionapi.com/api/v4/dreambooth/"

        client = OpenAI(organization="you_stable_diffusion_org_id_here", api_key="you_stable_diffusion_api_key_here")

        completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are creating a single word of full sentences"},
            {"role": "user", "content": text}
        ]
        )

        print(completion.choices[0].message.content)
        text = completion.choices[0].message.content

        payload = json.dumps({
        "key": "you_stable_diffusion_api_key_here",
        "model_id": "midjourney",
        "prompt": text,
        "width": "512",
        "height": "512",
        "samples": "1",
        "num_inference_steps": "30",
        "safety_checker": "no",
        "enhance_prompt": "yes",
        "seed": None,
        "guidance_scale": 7.5,
        "multi_lingual": "no",
        "panorama": "no",
        "self_attention": "no",
        "upscale": "no",
        "embeddings_model": None,
        "lora_model": None,
        "tomesd": "yes",
        "use_karras_sigmas": "yes",
        "vae": None,
        "lora_strength": None,
        "scheduler": "UniPCMultistepScheduler",
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