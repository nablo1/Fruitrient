# Author: Ruthger

import logging
from PIL import Image
import falcon
from falcon.asgi import Request, Response
import json
import pickle
import io
import joblib

from .common import active_classifier_to_dict, classifier_to_dict, collect_form, check_perf
from ..models import ClassifierHistoryModelExt, ClassifierModel, ClassifierModelExt, DataSetModelExt, TrainDataModel
from ..classification import Classifier, KerasClassifier, SciKitClassifier

logger = logging.getLogger(__name__)

# Wrapper around check_perf but takes a list of TrainData, performs the appropriate conversion.
def test_accuracy_with_dataset(model: Classifier, dataset: list[TrainDataModel]) -> float:
    perf_res = check_perf(model, ((Image.open(io.BytesIO(data.image)), data.label) for data in dataset))
    accuracy = perf_res["total_correct"] / (perf_res["total_incorrect"] + perf_res["total_correct"])

    return accuracy

# Classifier resource, contains main functionality for detecting and constructing to appropriate Classifier implementation 
class ClassifierResource:
    
    async def on_post(self, req: Request, resp: Response) -> None:
        resp.status = 404
        media = await collect_form(await req.media)

        bits = media["model_bytes"]

        pyobj = None

        labels_swap = {}
        for k,v in media["labels"].items():
            labels_swap[v] = k
        labels = labels_swap

        # First try to load the bytes straight up
        try: pyobj = pickle.loads(bits)
        except: pass
        
        # If it doesn't work try joblib
        if pyobj == None:
            try: pyobj = joblib.load(io.BytesIO(bits))
            except: pass

        image_format: str = media["meta"]["image_format"]
        image_size_y: int = media["meta"]["image_size_y"]
        image_size_x: int = media["meta"]["image_size_x"]

        # If it still doesnt work try constructing a keras classifier as it works with H5 files
        if pyobj == None:
            try: 
                pyobj = KerasClassifier(bits, labels, image_format, image_size_x, image_size_y)
                logger.info("created new Keras Model!")
            except: pass

        # We're just going to assume the file is from SciKit if keras also failed
        if pyobj != None and not issubclass(type(pyobj), Classifier):
            logger.info("redumping SciKit Classifier")
            pyobj = SciKitClassifier(pyobj, labels)

        # If its still none then we currently dont support it :/
        if pyobj == None:
            return
        
        # As we have a classifier now we grab the dataset to assess it's performance
        dataset_id = media["meta"]["verify_dataset_id"]
        dataset = DataSetModelExt.get(dataset_id)

        if dataset == None:
            logger.info("Invalid dataset for model upload verification")
            return

        # Get the accuracy
        accuracy = test_accuracy_with_dataset(pyobj, dataset.data)

        # Save the classifier by pickling the classifier and grabbing the remaing meta data
        ClassifierModel(
            name = media["meta"]["name"],
            performance = accuracy * 100,
            model_bytes = pickle.dumps(pyobj),
            generation = 1
        ).save()

        resp.status = falcon.HTTP_200

    async def on_delete(self, _: Request, resp: Response, id) -> None:
        resp.status = falcon.HTTP_200 if ClassifierModelExt.erase(int(id)) else falcon.HTTP_400
            
    async def on_get(self, _: Request, resp: Response) -> None:
        resp.text = json.dumps(list(map(classifier_to_dict, ClassifierModelExt.iter())))
        resp.status = falcon.HTTP_200
    
    async def on_get_single(self, _: Request, resp: Response, id: int) -> None:
        ret = ClassifierModelExt.get(int(id))
        if ret != None:
            resp.text = json.dumps(classifier_to_dict(ret))
            resp.status = falcon.HTTP_200
        else:
            resp.status = falcon.HTTP_400

# Resource that gives access to the classifier history
# notable supports python like indexing and thus on_get_single with id = -1 gives the latest classifier
class ClassifierHistoryResource:
    
    # Takes model id and pushes it as the active one
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

