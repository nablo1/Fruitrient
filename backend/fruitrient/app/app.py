# Author: Ruthger 

import logging
import pickle
import falcon
from falcon.media.multipart import MultipartFormHandler, MultipartParseOptions
from falcon.asgi import App
from falcon import CORSMiddleware
from peewee import SqliteDatabase
from .models import ClassifierModel, TrackedClassifier, bind
from dotenv import load_dotenv
import os

from .classification import RandomClassifier

from .resources.admin import AdminActions
from .resources.user import UserActions
from .resources.classifier import ClassifierResource, ClassifierHistoryResource
from .resources.prediction import PredictionResource
from .resources.dataset import DataSetResource
from .resources.nutrition import NutritionResource

logger = logging.getLogger(__name__)

# Creates a new falcon app and sets up all the routes
def create_app() -> App:

    load_dotenv()

    # Createa new sqlite database connection
    db = SqliteDatabase("testing.db")
    assert db.connect(True)

    bind(db)

    # If there does not exist any classifier (checked by simple .get()) then we create dummy ones so that the system is still usuable.
    try:
        nice = ClassifierModel.get()
    except Exception as e:
        logger.info(e)
        logger.info("No classifier found, creating a dummy!")

        # Generally expected labels for the system
        labels = {
            0: "freshApple",
            1: "freshBanana",
            2: "freshOrange",
            3: "rottenApple",
            4: "rottenBanana",
            5: "rottenOrange"
        }
        
        # function to make random classifier
        make_model = lambda name: ClassifierModel(
            name = name,
            model_bytes = pickle.dumps(RandomClassifier(labels)),
            performance = (1/len(labels))*100,
            generation = 1
        ).save()

        nice = make_model("Default - Random")
        make_model("Default - Random 2")
        make_model("Default - Random 3")

    # check we have atleast a clasifier in the database
    if nice == None:
        assert False

    # Add CORS middleware to prevent security rejections
    app = App(middleware=[CORSMiddleware()])


    # Override mutlipart limits as we are uploading large amounts of data and can cause rejections
    # in the future some form of streaming would be better
    mopts = MultipartParseOptions()
    mopts.max_body_part_count = 8192
    mopts.max_body_part_headers_size = 8192 * 16
    
    app.req_options.media_handlers.update({falcon.MEDIA_MULTIPART: MultipartFormHandler(mopts)})
    app.resp_options.media_handlers.update({falcon.MEDIA_MULTIPART: MultipartFormHandler(mopts)})

    # Actions
    # Simple classification for the public
    classifier = TrackedClassifier()
    user = UserActions(classifier)
    app.add_route('/user/classify', user)

    # Administrative actions like retraining and checking performance
    admin = AdminActions()
    app.add_route('/admin/check_perf/{classifier_id}', admin, suffix='check_perf')
    app.add_route('/admin/retrain/{classifier_id}', admin, suffix='retrain')

    # Resources
    passive = ClassifierResource()
    app.add_route('/classifiers', passive)
    app.add_route('/classifiers/{id}', passive, suffix='single')

    active = ClassifierHistoryResource()
    app.add_route('/active_classifiers', active)
    app.add_route('/active_classifiers/{id}', active, suffix='single')

    pred = PredictionResource()
    app.add_route('/predictions', pred)
    app.add_route('/predictions/{id}/image', pred, suffix="image")

    dataset = DataSetResource()
    app.add_route('/datasets', dataset)


    # Load up the spoonacular key to access the api
    key =  os.getenv("SPOONACULAR_API_KEY", "")
    if key == "":
        logger.info("No proper spoonacular api key found, expect failure!")
    nutrition = NutritionResource(key)
    app.add_route('/nutrition_facts/{ingredient}', nutrition, suffix='nutrition')
    app.add_route('/recipes/{ingredient}', nutrition, suffix='recipes')

    return app
