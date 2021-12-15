
import logging
from typing import Optional
import random
from PIL import Image
import numpy as np
from keras.models import load_model
import h5py
from keras.preprocessing.image import img_to_array
import io

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
    labels = {}

    def __init__(self, labels) -> None:
        self.labels = labels

    def classify(self, image: Image) -> Optional[PredictionRes]:

        res = self._predict(image)

        if res == None:
            logger.info("failed to predict")
            return None

        try:
            fruit_name = self.labels[res]
        except:
            logger.info("Could not get the correct label")
            fruit_name = "Unknown" # Means our labels don't match
        
        rotten = True
        if fruit_name.startswith("fresh"):
            fruit_name = fruit_name.split("fresh")[-1]
            rotten = False

        if fruit_name.startswith("rotten"):
            fruit_name = fruit_name.split("rotten")[-1]

        return PredictionRes(fruit_name, res, not rotten)

    def _predict(self, _: Image) -> Optional[int]:
        logger.info("BASE CLASSIFIER")
        assert False

class RandomClassifier(Classifier):

    def __init__(self, labels) -> None:
        super().__init__(labels)

    def _predict(self, _: Image) -> Optional[int]:
        logger.info("RANDOM CLASSIFIER")
        return random.randrange(0, len(self.labels))

class KerasClassifier(Classifier):
    model_bytes = None

    def _load_model(self):
        with h5py.File(io.BytesIO(self.model_bytes)) as h5:
            return load_model(h5)

    def __init__(self, h5: bytes, labels) -> None:
        super().__init__(labels)
        self.model_bytes = h5
        self._load_model()

    def _predict(self, image: Image) -> Optional[int]:
        model = self._load_model()
        logger.info("KERAS CLASSIFIER")
        image = image.resize((224, 224)).convert('RGB')
        img_data = np.expand_dims(img_to_array(image), axis=0)
        
        predictions = np.argmax(model.predict(np.vstack([img_data])), axis=1)

        return int(predictions[0])

class SciKitClassifier(Classifier):
    model = None

    def __init__(self, model, labels) -> None:
        super().__init__(labels)
        self.model = model

    def _predict(self, image: Image) -> Optional[int]:
        logger.info("SCIKIT CLASSIFIER")

        image = image.resize((28,28)).convert('L')
        img_data = np.asarray(image.getdata(), dtype=np.int32).flatten()

        return int(self.model.predict([img_data])[0])

