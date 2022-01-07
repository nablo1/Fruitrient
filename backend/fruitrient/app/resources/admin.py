# Author: Ruthger

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

# Administrative actions such as checking performance of a classifier or retraining one
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

    # Takes a classifier and 2 datasets for train and test, then retrains it and adds it as a new version to the database
    async def on_put_retrain(self, req: Request, resp: Response, classifier_id: int) -> None:
        resp.status = falcon.HTTP_404
        media = await req.media

        # Get the classifier
        model = ClassifierModelExt.get(classifier_id)
        if model == None:
            return

        dataset_id = media["dataset_id"]
        dataset_verify_id = media["dataset_verify_id"]

        # Get the training dataset
        dataset = DataSetModelExt.get(dataset_id)

        if dataset == None:
            return

        logger.info("starting retrain!")

        # load up the classifier and call retrain on it
        modelcl: Classifier = pickle.loads(model.model_bytes)
        new_model: Classifier = modelcl.retrain(((data.label, Image.open(io.BytesIO(data.image))) for data in dataset.data))

        # check if the new model is None which mean failure
        if new_model == None:
            logger.info("FAILED TO RETRAIN")
            return

        # Get the testing dataset
        dataset_verify = DataSetModelExt.get(dataset_verify_id)

        if dataset_verify == None:
            return
        
        # Test the accuracy
        accuracy = test_accuracy_with_dataset(new_model, dataset_verify.data)

        # if the accuracy is lower than the original model then fail the retraining
        if accuracy * 100 < model.performance:
            logger.info("retrain did not improve accuracy!")
            # TODO: fail
        
        # Save the new classifier with the same metadata except with a version increase
        ClassifierModel(
            name = model.name,
            performance = accuracy * 100,
            model_bytes = pickle.dumps(new_model),
            generation = model.generation + 1 # increase version
        ).save()

        resp.status = falcon.HTTP_200
