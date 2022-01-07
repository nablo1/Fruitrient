
import logging
from typing import Optional, Tuple
import random
from PIL.Image import Image
import numpy as np
from keras.models import load_model
import h5py
from keras.preprocessing.image import img_to_array
import io

logger = logging.getLogger(__name__)

class PredictionRes:
    name: str
    fresh: bool

    def __init__(self, name: str, fresh: float) -> None:
        self.name = name
        self.fresh = fresh

def extract_label_components(name: str) -> Tuple[str, bool]:
    rotten = True
    if name.startswith("fresh"):
        fruit_name = name.split("fresh")[-1]
        rotten = False

    if name.startswith("rotten"):
        fruit_name = name.split("rotten")[-1]
    
    return (fruit_name, not rotten)

class Classifier:
    labels = {}
    image_type: str
    image_x: int
    image_y: int

    def __init__(self, labels, image_type, image_x, image_y) -> None:
        self.labels = labels
        self.image_type = image_type
        self.image_x = image_x
        self.image_y = image_y

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
        
       
        fruit_name, fresh = extract_label_components(fruit_name)

        return PredictionRes(fruit_name, fresh)

    def _predict(self, _: Image) -> Optional[int]:
        logger.info("BASE CLASSIFIER")
        assert False

    def retrain(self, images: list[Tuple[str, Image]]):

        labels_swap = {}
        for k,v in self.labels.items():
            labels_swap[v] = k

        mapped = [(labels_swap[image[0]], image[1]) for image in images]

        return self._retrain(mapped)

    def _retrain(self, images: list[Tuple[int, Image]]) -> None:
        logger.info("BASE CLASSIFIER RETRAIN")
        assert False

class RandomClassifier(Classifier):

    def __init__(self, labels) -> None:
        super().__init__(labels, "L", 0, 0)

    def _predict(self, _: Image) -> Optional[int]:
        logger.info("RANDOM CLASSIFIER")
        return random.randrange(0, len(self.labels))

class KerasClassifier(Classifier):
    model_bytes: bytes


    def _load_model(self):
        with h5py.File(io.BytesIO(self.model_bytes)) as h5:
            return load_model(h5)

    def __init__(self, h5: bytes, labels, image_type, image_x, image_y) -> None:
        super().__init__(labels, image_type, image_x, image_y)
        self.model_bytes = h5
        self._load_model()

    def _fix_image(self, img: Image) -> Image:
        return img.resize((self.image_x, self.image_y)).convert(self.image_type)

    def _predict(self, image: Image) -> Optional[int]:
        logger.info("KERAS CLASSIFIER")
        model = self._load_model()
        
        image = self._fix_image(image)
        img_data = np.array([img_to_array(image)])

        try:
            predictions = np.argmax(model.predict(img_data), axis=1)
        except Exception as e:
            logger.info("KERAS ERROR OOPS")
            logger.info(e)
            return None
        
        return int(predictions[0])
    
    def _retrain(self, images: list[Tuple[int, Image]]) -> Optional[Classifier]:
        logger.info("KERAS CLASSIFIER RETRAIN")
        try:
            model = self._load_model()
            
            X_train = np.asarray([img_to_array(self._fix_image(image[1])) for image in images])
            Y_train = np.asarray([image[0] for image in images])

            logger.info(X_train.shape)
            logger.info(Y_train.shape)

            model.fit(X_train, Y_train, epochs=5)

            
            h5bytes = io.BytesIO(bytearray())
            with h5py.File(h5bytes, mode='w') as h5:
                model.save(h5)

            return KerasClassifier(h5bytes.getvalue(), self.labels, self.image_type, self.image_x, self.image_y)
        except Exception as e:
            logger.info(e)

            return None

class SciKitClassifier(Classifier):
    model = None

    def __init__(self, model, labels, image_type, image_x, image_y) -> None:
        super().__init__(labels, image_type, image_x, image_y)
        self.model = model

    def _predict(self, image: Image) -> Optional[int]:
        logger.info("SCIKIT CLASSIFIER")

        image = image.resize((self.image_x, self.image_y)).convert(self.image_type)
        img_data = np.asarray(image.getdata(), dtype=np.int32).flatten()

        return int(self.model.predict([img_data])[0])

    def _retrain(self, _: list[Tuple[int, Image]]) -> None:
        assert False, "SCIKIT RETRAIN IS NOT IMPLEMENTED YET"