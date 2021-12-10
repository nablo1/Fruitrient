
import logging
from typing import Optional
import random
from PIL import Image
import numpy as np

logger = logging.getLogger(__name__)


class PredictionRes:
    name: str
    type: int
    fresh: bool

    def __init__(self, name: str, type: int, fresh: float) -> None:
        self.name = name
        self.type = type
        self.fresh = fresh

class Classifier:
    def classify(self, _: Image) -> Optional[PredictionRes]:
        logger.info("BASE CLASSIFIER")

        return None

class RandomClassifier(Classifier):

    fruits = ["Gomu Gomu No Mi", "Mera Mera no Mi", "Gura Gura no Mi",
              "Ito Ito no Mi", "Jiki Jiki no Mi", "Ope Ope no Mi"]

    def classify(self, _: Image) -> Optional[PredictionRes]:
        logger.info("RANDOM CLASSIFIER")
        fruit_type = random.randrange(0, len(self.fruits))
        some = PredictionRes(self.fruits[fruit_type], fruit_type, random.randint(0,1) == 1)
        return some

class SciKitClassifier(Classifier):
    model = None
    labels = {}

    def __init__(self, model, labels) -> None:
        self.model = model
        self.labels = labels

    def classify(self, image: Image) -> Optional[PredictionRes]:
        logger.info("SCIKIT CLASSIFIER")

        image = image.resize((28,28)).convert('L')
        img_data = np.asarray(image.getdata(), dtype=np.int32).flatten()

        res = int(self.model.predict([img_data])[0])

        try:
            fruit_name = self.labels[res]
        except:
            logger.info("Could not get the correct label")
            fruit_name = "Unknown" # Means our labels don't match
        
        rotten = False

        if fruit_name.startswith("fresh"):
            fruit_name = fruit_name.split("fresh")[-1]
            rotten = True

        if fruit_name.startswith("rotten"):
            fruit_name = fruit_name.split("rotten")[-1]

        return PredictionRes(fruit_name, res, not rotten)

