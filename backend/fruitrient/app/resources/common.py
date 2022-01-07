# Author: Ruthger

import io
import logging
import PIL
from PIL.Image import Image

from ..models import ClassifierHistoryModel, ClassifierModel, PredictionModel
from ..classification import Classifier, extract_label_components

logger = logging.getLogger(__name__)

# Utility function to convert a classifier model to a dictionary
def classifier_to_dict(c: ClassifierModel):
    return { 
        "id": c.id,
        "name": c.name,
        "performance": int(c.performance),
        "creation_date": str(c.creation_date),
        "generation": c.generation
    }

# Utility function to convert an active classifier to a dictionary
def active_classifier_to_dict(h: ClassifierHistoryModel):
    return {
        "id": h.id,
        "selected_date": str(h.selected_date),
        "classifier": classifier_to_dict(h.classifier)
    }

# Utility function to convert a prediction to a dictionary
def prediction_to_dict(p: PredictionModel):
    return {
        "id": getattr(p, 'id', None),
        "name": p.name,
        "fresh": p.fresh,
    }

# Utility function that converts a multipart form into a dictionary
# also converts supported mime types into python types
# namely image/* is converted into PIL.Image
async def collect_form(form):
    media = {}
    async for part in form:
        if part.content_type.startswith("image"):
            media[part.name] = PIL.Image.open(io.BytesIO(await part.stream.readall()))
        elif part.content_type.startswith("application/octet-stream"):
            media[part.name] = await part.stream.readall()
        elif part.content_type.startswith("text/plain"):
            media[part.name] = (await part.stream.readall()).decode("ascii") 
        else:
            media[part.name] = await part.media
    return media

# Takes labeled images and a classifier
# classifies each image and bundles the expected value with it
# useful for accuracy checks
def check_perf(classifier: Classifier, data: list[tuple[Image, str]]):
    # classify each image (lazily)
    result = map(lambda xy: (classifier.classify(xy[0]), xy[1]), data)
    logger.info(classifier.labels)
    total_correct = 0
    acc = []

    # iterate over the results, then check if the classified answer is equal to the expect answer
    for res, correct_label in result:
        # as labels are strings we need to extract the components first
        (name, fresh) = extract_label_components(correct_label)
        iscorrect = (res != None) and (res.name == name) and (res.fresh == fresh)

        acc.append({
            "result": prediction_to_dict(res),
            "is_correct": iscorrect,
            "expected_name": name,
            "expected_fresh": fresh
        })
        total_correct += int(iscorrect)
    
    total_incorrect = len(acc) - total_correct

    return {"results": acc, "total_correct": total_correct, "total_incorrect": total_incorrect}
