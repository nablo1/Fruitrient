# Author: Ruthger

import logging
import falcon
from falcon.asgi import Request, Response
import json
import io
from PIL import Image

from .common import prediction_to_dict
from ..app import TrackedClassifier

logger = logging.getLogger(__name__)

class UserActions:
    classifier: TrackedClassifier

    def __init__(self, classifier: TrackedClassifier) -> None:
        self.classifier = classifier

    # Expects an image body, can be any image type as long as its supported by the Pillow library
    async def on_put(self, req: Request, resp: Response) -> None:
        image = Image.open(io.BytesIO(await req.stream.readall()))

        # delegate classification to the TrackedClassifier
        res = self.classifier.classify(image)
        
        if res == None:
            resp.status = falcon.HTTP_400
            resp.text = "Classification failed!"
            logger.info("Classification failed!" + str(res))
            return

        # convert the result to a dictionary
        ret = prediction_to_dict(res)

        resp.text = json.dumps(ret)
        resp.status = falcon.HTTP_200
