import logging
import pickle
import falcon
from falcon.media.base import BaseHandler
from falcon.asgi import App
from falcon import CORSMiddleware
from peewee import SqliteDatabase
from .models import ClassifierModel, TrackedClassifier, bind

from .classification import RandomClassifier
from .handlers import ActiveClassifierResource, AdminActions, ClassifierResource, PredictionResource, UserActions

logger = logging.getLogger(__name__)


def create_app() -> App:


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
    # admin = AdminActions(classifier)
    # app.add_route('/admin/')

    # Resources
    passive = ClassifierResource()
    app.add_route('/classifiers', passive)
    app.add_route('/classifiers/{id}', passive, suffix='single')

    active = ActiveClassifierResource()
    app.add_route('/active_classifiers', active)
    app.add_route('/active_classifiers/{id}', active, suffix='single')

    pred = PredictionResource()
    app.add_route('/predictions', pred)
    # TODO: by id?

    return app
