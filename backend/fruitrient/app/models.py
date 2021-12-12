import datetime
import io
import logging
import pickle
from typing import Optional
from peewee import BooleanField, Model, BlobField, DateTimeField, FloatField, AutoField, IntegerField, CharField, ForeignKeyField, Database


from .classification import Classifier, Image, PredictionRes 

logger = logging.getLogger(__name__)

class ClassifierModel(Model):
    id = AutoField()
    name = CharField()
    creation_date = DateTimeField(default=datetime.datetime.now)
    model_bytes = BlobField()
    performance = FloatField()

class ClassifierModelExt:
    def get(idx: int) -> Optional[ClassifierModel]:
        try:
            return ClassifierModel.get_by_id(idx)
        except:
            return None
    
    def erase(idx: int) -> bool:
        try:
            ClassifierModel.delete_by_id(idx)
            return True
        except:
            return False

    def iter():
        return ClassifierModel \
                .select(ClassifierModel) \
                .order_by(ClassifierModel.id.desc())

class PredictionModel(Model):
    id = AutoField()
    predicted_by = ForeignKeyField(ClassifierModel, backref='predictions')
    image = BlobField()
    name = CharField()
    type = IntegerField()
    fresh = BooleanField()

class PredictionModelExt:
    def iter():
        return PredictionModel \
                .select(PredictionModel) \
                .order_by(PredictionModel.id)
    
    def get(idx: int) -> Optional[PredictionModel]:
        try:
            return PredictionModel.get_by_id(idx)
        except:
            return None

class ClassifierHistoryModel(Model):
    id = AutoField()
    classifier = ForeignKeyField(ClassifierModel)
    selected_date = DateTimeField(default=datetime.datetime.now)

class ClassifierHistoryModelExt:
    def get(idx: int) -> Optional[ClassifierHistoryModel]:
        try:
            return ClassifierHistoryModel \
                        .select(ClassifierHistoryModel) \
                        .order_by(ClassifierHistoryModel.id.asc() if idx > 0 else ClassifierHistoryModel.id.desc()) \
                        .offset(abs(idx)) \
                        .limit(1) \
                        .get_or_none()
        except Exception as e:
            logger.info(e)
            return None

    def push(classifier_id: int) -> Optional[ClassifierHistoryModel]:
        front = ClassifierHistoryModelExt.get(-1)
        if front != None and front.classifier.id == classifier_id:
            logger.info("WTF")
            return front
        elif ClassifierModelExt.get(classifier_id) != None:
            ret = ClassifierHistoryModel(classifier = classifier_id)
            ret.save()
            logger.info("WTF2")

            return ret
        else:
            logger.info("WTF4")

    
    def iter():
        return ClassifierHistoryModel \
                    .select(ClassifierHistoryModel) \
                    .order_by(ClassifierHistoryModel.id.desc())


def bind(db: Database):
    models = [
        ClassifierModel,
        PredictionModel,
        ClassifierHistoryModel
    ]
    db.bind(models)
    db.create_tables(models)


class TrackedClassifier(Classifier):

    def classify(self, image: Image) -> Optional[PredictionRes]:

        # We're effectively polling the active classifier,
        # since we don't own the backing storage it's considered volatile.
        classifier = ClassifierHistoryModelExt.get(-1)


        if classifier == None:
            return None

        # TODO: somehow cache this?
        cl = pickle.loads(classifier.classifier.model_bytes)
        res = cl.classify(image)

        if res == None:
            return None
        
        try:
            image_bytes = io.BytesIO()
            image.save(image_bytes, format='png')
            image_bytes.seek(0)
            PredictionModel(
                predicted_by = classifier.classifier.id,
                image = image_bytes.read(),
                name = res.name,
                type = res.type,
                fresh = res.fresh,
            ).save()
        except Exception as e:
            logger.info("Failed to save prediction! " + str(e))
            return None
        
        return res
