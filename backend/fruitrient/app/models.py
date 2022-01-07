# Author: Ruthger 

import datetime
import io
import logging
import pickle
from typing import Optional
from peewee import BooleanField, IntegerField, Model, BlobField, DateTimeField, FloatField, AutoField, CharField, ForeignKeyField, Database

from .classification import Classifier, Image 

logger = logging.getLogger(__name__)

# Table for datasets, they dont store data themselves but have a backreference `data` from TrainDataModel
class DataSetModel(Model):
    id = AutoField()
    name = CharField()

# Individual labeled images, reference the dataset they belong to
class TrainDataModel(Model):
    dataset = ForeignKeyField(DataSetModel, backref="data")
    label = CharField()
    image = BlobField()

# Extension class to for common access to datasets
class DataSetModelExt:
    def push(name, images):
        new = DataSetModel(name=name)
        new.save()

        for image, label in images:
            image_bytes = io.BytesIO()
            image.save(image_bytes, format='png')
            image_bytes.seek(0)

            TrainDataModel(
                dataset = new.id,
                label=label,
                image = image_bytes.read(),
            ).save()

    def get(idx: int) -> Optional[DataSetModel]:
        try:
            return DataSetModel.get_by_id(idx)
        except:
            return None

    def iter():
        return DataSetModel \
                .select(DataSetModel) \
                .order_by(DataSetModel.id.desc())

# Describes a concrete classifier, `model_bytes` must be a pickled object deriving from `Classifier`
class ClassifierModel(Model):
    id = AutoField()
    name = CharField()
    generation = IntegerField()
    creation_date = DateTimeField(default=datetime.datetime.now)
    model_bytes = BlobField()
    performance = FloatField()

# Extension class to for common access to classifiers
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

# Stores predictions made by classifiers, each prediction backreferences the classifier they were made from
class PredictionModel(Model):
    id = AutoField()
    predicted_by = ForeignKeyField(ClassifierModel, backref='predictions')
    image = BlobField()
    name = CharField()
    fresh = BooleanField()

# Extension class to for common access to predictions
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

# Extension class to for common access to classifier history
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
            return front
        elif ClassifierModelExt.get(classifier_id) != None:
            ret = ClassifierHistoryModel(classifier = classifier_id)
            ret.save()
            return ret

    
    def iter():
        return ClassifierHistoryModel \
                    .select(ClassifierHistoryModel) \
                    .order_by(ClassifierHistoryModel.id.desc())


def bind(db: Database):
    models = [
        ClassifierModel,
        PredictionModel,
        ClassifierHistoryModel,
        DataSetModel,
        TrainDataModel
    ]
    db.bind(models)
    db.create_tables(models)

# Classifier like interface that pulls the current active classifier and stores the made prediction via PredictionModel
class TrackedClassifier:

    def classify(self, image: Image) -> Optional[PredictionModel]:

        # We're effectively polling the active classifier,
        # since we don't own the backing storage it's considered volatile.
        classifier = ClassifierHistoryModelExt.get(-1)


        if classifier == None:
            return None

        # TODO: somehow cache this?
        cl: Classifier = pickle.loads(classifier.classifier.model_bytes)
        res = cl.classify(image)

        if res == None:
            return None
        
        try:
            image_bytes = io.BytesIO()
            image.save(image_bytes, format='png')
            image_bytes.seek(0)
            ret = PredictionModel(
                predicted_by = classifier.classifier.id,
                image = image_bytes.read(),
                name = res.name,
                fresh = res.fresh,
            )
            
            ret.save()

            return ret
        except Exception as e:
            logger.info("Failed to save prediction! " + str(e))
            return None
