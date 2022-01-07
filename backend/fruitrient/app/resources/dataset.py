import json
import logging
import falcon
from falcon.asgi import Request, Response

from .common import collect_form
from ..models import DataSetModelExt

logger = logging.getLogger(__name__)

class DataSetResource:
    async def on_post(self, req: Request, resp: Response) -> None:
        resp.status = falcon.HTTP_404

        data = await collect_form(await req.media)
        
        dataset = zip((kv[1].resize((255,255)) for kv in data.items() if kv[0].startswith("image")), data["labels"])

        DataSetModelExt.push(data["name"], dataset)

        resp.status = falcon.HTTP_200
    
    async def on_get(self, _: Request, resp: Response) -> None:
        resp.text = json.dumps([{ "id": dataset.id, "name": dataset.name, "image_count": len(dataset.data) } for dataset in DataSetModelExt.iter()])
        resp.status = falcon.HTTP_200
        