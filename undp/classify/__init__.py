import logging
import os

import azure.functions as func
from fastai.vision import *
import requests

from .notification import *

IS_DEBUG = False
CONN_STRING = '<ConnectionString>'
HUB_NAME = '<HubName>'

def main(req: func.HttpRequest) -> func.HttpResponse:
    path = Path.cwd()
    learn = load_learner(path)
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        image_url = req.params.get('name')
        logging.info('Image URL received: ' + image_url)
        r = requests.get(image_url)

        if r.status_code == 200:
            temp_image_name = "temp.jpg"        
            with open(temp_image_name, 'wb') as f:
                f.write(r.content)
        else:
            return func.HttpResponse(f"Image download failed, url: {image_url}")

        img = open_image(temp_image_name)
        pred_class, pred_idx, outputs = learn.predict(img)
        confidence = outputs[pred_idx].item()

        # initialize notification hub
        hub = NotificationHub(CONN_STRING, HUB_NAME, IS_DEBUG)

        gcm_payload = {
            'data':
                {
                    'msg': f'{pred_class} detected, confidence: {confidence:.3f}'
                }
        }
        hub.send_gcm_notification(gcm_payload)

        return func.HttpResponse(f"image_url: {image_url}, pred_class: {pred_class}, confidence: {confidence}")
    else:
        return func.HttpResponse(
             "Please pass a name on the query string or in the request body",
             status_code=400
        )
