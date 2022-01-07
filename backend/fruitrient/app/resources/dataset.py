# Author: Ruthger

import json
import logging
import falcon
from falcon.asgi import Request, Response

from .common import collect_form
from ..models import DataSetModelExt

logger = logging.getLogger(__name__)

class DataSetResource:
    # Route to upload a new dataset expects a multipart form
    # each key with the "image" prefix is interpreted as an image
    # and "labels" is interpreted as an array of labels for all images
    async def on_post(self, req: Request, resp: Response) -> None:
        resp.status = falcon.HTTP_404

        data = await collect_form(await req.media)
        
        # Zip the images with their respective labels, it is considered user error if sizes mismatch
        dataset = zip((kv[1].resize((255,255)) for kv in data.items() if kv[0].startswith("image")), data["labels"])

        DataSetModelExt.push(data["name"], dataset)

        resp.status = falcon.HTTP_200
    
    # Getter for all resources, doesn't actually return the dataset, just meta data such as image_count and name
    async def on_get(self, _: Request, resp: Response) -> None:
        resp.text = json.dumps([{ "id": dataset.id, "name": dataset.name, "image_count": len(dataset.data) } for dataset in DataSetModelExt.iter()])
        resp.status = falcon.HTTP_200
    
    # TODO: a way to remove datasets