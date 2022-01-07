import logging
from PIL import Image
import falcon
from falcon.asgi import Request, Response
import json
import io
import pickle

from ..classification import Classifier

from .classifier import test_accuracy_with_dataset

from .common import check_perf

from ..models import ClassifierModel, ClassifierModelExt, DataSetModelExt

logger = logging.getLogger(__name__)

class AdminActions:
   
    async def on_put_check_perf(self, req: Request, resp: Response, classifier_id: int) -> None:
        resp.status = 404
        classifier = ClassifierModelExt.get(int(classifier_id))
        classifier = pickle.loads(classifier.model_bytes)
        
        if classifier == None:
            return

        data = await req.media
        dataset = DataSetModelExt.get(data["dataset_id"])

        logger.info(len(dataset.data))
        
        res = check_perf(classifier, ((Image.open(io.BytesIO(data.image)), data.label) for data in dataset.data))

        resp.status = falcon.HTTP_200
        resp.text = json.dumps(res)

    async def on_put_retrain(self, req: Request, resp: Response, classifier_id: int) -> None:
        resp.status = falcon.HTTP_404
        media = await req.media

        model = ClassifierModelExt.get(classifier_id)
        if model == None:
            return

        dataset_id = media["dataset_id"]
        dataset_verify_id = media["dataset_verify_id"]

        dataset = DataSetModelExt.get(dataset_id)

        if dataset == None:
            return

        logger.info("starting retrain!")

        modelcl: Classifier = pickle.loads(model.model_bytes)
        new_model: Classifier = modelcl.retrain(((data.label, Image.open(io.BytesIO(data.image))) for data in dataset.data))

        if new_model == None:
            logger.info("FAILED TO RETRAIN")
            return

        dataset_verify = DataSetModelExt.get(dataset_verify_id)

        if dataset_verify == None:
            return
        
        accuracy = test_accuracy_with_dataset(new_model, dataset_verify.data)

        if accuracy * 100 < model.performance:
            logger.info("retrain did not improve accuracy!")
            # TODO: fail
        
        ClassifierModel(
            name = model.name,
            performance = accuracy * 100,
            model_bytes = pickle.dumps(new_model),
            generation = model.generation + 1
        ).save()

        resp.status = falcon.HTTP_200
