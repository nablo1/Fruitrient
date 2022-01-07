import io
import logging
import PIL
from PIL.Image import Image

from ..models import ClassifierHistoryModel, ClassifierModel, PredictionModel
from ..classification import Classifier, extract_label_components

logger = logging.getLogger(__name__)


def classifier_to_dict(c: ClassifierModel):
    return { 
        "id": c.id,
        "name": c.name,
        "performance": int(c.performance),
        "creation_date": str(c.creation_date),
        "generation": c.generation
    }

def active_classifier_to_dict(h: ClassifierHistoryModel):
    return {
        "id": h.id,
        "selected_date": str(h.selected_date),
        "classifier": classifier_to_dict(h.classifier)
    }

def prediction_to_dict(p: PredictionModel):
    return {
        "id": getattr(p, 'id', None),
        "name": p.name,
        "fresh": p.fresh,
    }


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

def check_perf(classifier: Classifier, data: list[tuple[Image, str]]):

    result = map(lambda xy: (classifier.classify(xy[0]), xy[1]), data)

    total_correct = 0
    acc = []
    for res, correct_label in result:
        (name, fresh) = extract_label_components(correct_label)
        logger.info(f"label: {correct_label} name: {name} fresh: {fresh}")
        iscorrect = (res != None) and (res.name == name) and (res.fresh == fresh)
        logger.info(f"res.name  {res.name} res.fresh {res.fresh}")

        acc.append({
            "result": prediction_to_dict(res),
            "is_correct": iscorrect,
            "expected_name": name,
            "expected_fresh": fresh
        })
        total_correct += int(iscorrect)
    
    logger.info(f"we got many results: {len(acc)}")
    total_incorrect = len(acc) - total_correct

    return {"results": acc, "total_correct": total_correct, "total_incorrect": total_incorrect}
