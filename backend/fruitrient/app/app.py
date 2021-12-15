import logging
import pickle
from falcon.asgi import App
from falcon import CORSMiddleware
from peewee import SqliteDatabase
from .models import ClassifierModel, TrackedClassifier, bind
from dotenv import load_dotenv
import os

from .classification import RandomClassifier
from .handlers import ActiveClassifierResource, AdminActions, ClassifierResource, NutritionResource, PredictionResource, UserActions

logger = logging.getLogger(__name__)


def create_app() -> App:
    load_dotenv()

    db = SqliteDatabase("testing.db")
    assert db.connect(True)

    bind(db)

    try:
        nice = ClassifierModel.get()
    except Exception:
        logger.info("No classifier found, creating a dummy!")
        nice = ClassifierModel(
            name = "Default - Random",
            model_bytes = pickle.dumps(RandomClassifier()),
            performance = 0
        )
        nice.save()

        ClassifierModel(
            name = "Default - Random 2",
            model_bytes = pickle.dumps(RandomClassifier()),
            performance = 0
        ).save()

        ClassifierModel(
            name = "Default - Random 3",
            model_bytes = pickle.dumps(RandomClassifier()),
            performance = 0
        ).save()

    if nice == None:
        assert False

    classifier = TrackedClassifier()

    app = App(middleware=[CORSMiddleware()])

    # Actions
    user = UserActions(classifier)
    app.add_route('/user/classify', user)

    # TODO:
    admin = AdminActions(classifier)
    app.add_route('/admin/check_perf/{classifier_id}', admin, suffix='check_perf')

    # Resources
    passive = ClassifierResource()
    app.add_route('/classifiers', passive)
    app.add_route('/classifiers/{id}', passive, suffix='single')

    active = ActiveClassifierResource()
    app.add_route('/active_classifiers', active)
    app.add_route('/active_classifiers/{id}', active, suffix='single')

    pred = PredictionResource()
    app.add_route('/predictions', pred)
    app.add_route('/predictions/{id}/image', pred, suffix="image")

    # TODO: by id?

    key =  os.getenv("SPOONACULAR_API_KEY", "")
    if key == "":
        logger.info("No proper spoonacular api key found, expect failure!")
    nutrition = NutritionResource(key)
    app.add_route('/nutrition_facts/{ingredient}', nutrition, suffix='nutrition')
    app.add_route('/recipes/{ingredient}', nutrition, suffix='recipes')


    return app
