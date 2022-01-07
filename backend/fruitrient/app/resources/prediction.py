# Author: Ruthger

import falcon
from falcon.asgi import Request, Response
import json

from .common import prediction_to_dict
from ..models import PredictionModelExt

# Simple resource to give access to predictions
class PredictionResource:
    async def on_get(self, _: Request, resp: Response) -> None:
        ret = list(map(prediction_to_dict, PredictionModelExt.iter()))

        resp.text = json.dumps(ret)
        resp.status = falcon.HTTP_200
    
    # Since serving images are a bit special we have a seperate route for them for the client to use as image source
    async def on_get_image(self, _: Request, resp: Response, id) -> None:
        image = PredictionModelExt.get(id)
        if image == None:
            resp.status = falcon.HTTP_404
            return
        
        resp.data = image.image
        resp.status = falcon.HTTP_202
