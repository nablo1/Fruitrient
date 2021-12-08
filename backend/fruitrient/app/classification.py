
from typing import Optional, Tuple
import random

class FruitRes:
    name: str
    type: int
    certainty: float

    def __init__(self, name: str, type: int, certainty: float) -> None:
        self.name = name
        self.type = type
        self.certainty = certainty

class QualityRes:
    quality: float
    certainty: float

    def __init__(self, quality: float, certainty: float) -> None:
        self.quality = quality
        self.certainty = certainty


Image = bytes

class Classifier:
    def classify(self, _: Image) -> Optional[Tuple[FruitRes, QualityRes]]:
        return None

class RandomClassifier(Classifier):

    fruits = ["Gomu Gomu No Mi", "Mera Mera no Mi", "Gura Gura no Mi",
              "Ito Ito no Mi", "Jiki Jiki no Mi", "Ope Ope no Mi"]

    def classify(self, _: Image) -> Optional[Tuple[FruitRes, QualityRes]]:
        return (
            FruitRes(self.fruits[random.randrange(
                0, len(self.fruits))], 1, random.random()),
            QualityRes(random.random(), random.random())
        )

# TODO: actually implement once we have models to test
class SciKitClassifier(Classifier):
    model = None

    def __init__(self, model) -> None:
        self.model = model

    def classifiy(self, _: Image) -> Optional[Tuple[FruitRes, QualityRes]]:
        # self.model.predict(image)
        return None