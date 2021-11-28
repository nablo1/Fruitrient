import falcon
from falcon import Request, Response
import logging

logger = logging.getLogger(__name__)


class Basic:
    async def on_get(self, req: Request, resp: Response):
        body = await req.stream.read()

        logger.info(f"params: {req.params} body: {body}")

        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_HTML

        # Just ping back the body
        resp.text = body
