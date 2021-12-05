import falcon
from falcon.asgi import Request, Response
import logging
import json
import pickle

from .app import TrackedClassifier
from .models import ClassifierHistoryModel, ClassifierHistoryModelExt, ClassifierModel, ClassifierModelExt, PredictionModel, PredictionModelExt

from .classification import Classifier

logger = logging.getLogger(__name__)

def classifier_to_dict(c: ClassifierModel):
    return { 
        "id": c.id,
        "name": c.name,
        "performance": c.performance,
        "creation_date": str(c.creation_date)
    }

def active_classifier_to_dict(h: ClassifierHistoryModel):
    return {
        "id": h.id,
        "selected_date": str(h.selected_date),
        "classifier": classifier_to_dict(h.classifier)
    }

def prediction_to_dict(p: PredictionModel):
    return {
        "fruit": {
            "name": p.fruit_name,
            "type": p.fruit_type,
            "certainty": p.fruit_certainty
        },
        "quality": {
            "quality": p.quality,
            "certainty": p.quality_certainty
        }
    }


class UserActions:
    classifier: Classifier

    def __init__(self, classifier: Classifier) -> None:
        self.classifier = classifier

    async def on_put(self, req: Request, resp: Response) -> None:
        image = await req.stream.readall()

        res = self.classifier.classify(image)
        
        if res == None:
            resp.status = falcon.HTTP_400
            resp.text = "Classification failed!"
            return

        fruit, quality = res

        ret = \
            {
                "fruit": {
                    "name": fruit.name,
                    "type": fruit.type,
                    "certainty": fruit.certainty
                },
                "quality": {
                    "quality": quality.quality,
                    "certainty": quality.certainty
                }
            }

        resp.text = json.dumps(ret)
        resp.status = falcon.HTTP_200


class AdminActions:
    classifier: TrackedClassifier

    def __init__(self, classifier: TrackedClassifier) -> None:
        self.classifier = classifier

    # TODO: implement stuff

class ActiveClassifierResource:
    
    async def on_post(self, req: Request, resp: Response) -> None:
        resp.status = falcon.HTTP_400

        media = await req.get_media()

        logger.info(media)
        
        if not "id" in media:
            return

        id = int((media)["id"])
        
        if ClassifierHistoryModelExt.push(id) != None:
            resp.status = falcon.HTTP_200

    async def on_get_single(self, _: Request, resp: Response, id) -> None:
        ret = ClassifierHistoryModelExt.get(int(id))
        if ret != None:
            resp.text = json.dumps(active_classifier_to_dict(ret))
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_400


    async def on_get(self, _: Request, resp: Response) -> None:

        resp.text = \
            json.dumps(list(map(active_classifier_to_dict, ClassifierHistoryModelExt.iter())))
        
        resp.status = falcon.HTTP_200

class ClassifierResource:
    
    async def on_post(self, req: Request, resp: Response) -> None:
        jsn = req.get_media()
        bits = bytes(jsn["bits"])

        pickle.loads(bits)
        
        ClassifierModel(
            name = jsn["name"],
            performance = jsn["performance"],
            model_bytes = bits
        ).save()

        resp.status = falcon.HTTP_200

    async def on_delete(self, _: Request, resp: Response, id) -> None:
        resp.status = falcon.HTTP_200 if ClassifierModelExt.erase(int(id)) else falcon.HTTP_400
            
    async def on_get(self, _: Request, resp: Response) -> None:
        resp.text = json.dumps(list(map(classifier_to_dict, ClassifierModelExt.iter())))
        resp.status = falcon.HTTP_200
    
    async def on_get_single(self, _: Request, resp: Response, id) -> None:
        ret = ClassifierModelExt.get(int(id))
        if ret != None:
            resp.text = json.dumps(classifier_to_dict(ret))
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_400


class PredictionResource:
    async def on_get(self, _: Request, resp: Response) -> None:
        ret = list(map(prediction_to_dict, PredictionModelExt.iter()))

        resp.text = json.dumps(ret)
        resp.status = falcon.HTTP_200

