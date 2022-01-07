# Author: Ruthger

import falcon
from falcon.asgi import Request, Response
import logging
import json
import requests

logger = logging.getLogger(__name__)

# Resource that delegates api calls to the spoonacular api
class NutritionResource:
    api_key: str
    baseuri: str = "https://api.spoonacular.com"

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    # Simplifies spoonacular api access by prefilling boilerplate and doing the request call
    def get(self, uri: str, params: str = ""):
        res = requests.get(f"{self.baseuri}{uri}?apiKey={self.api_key}{params}")
        if res.status_code != 200:
            return None
        return res

    async def on_get_nutrition(self, _: Request, resp: Response, ingredient: str) -> None:
        resp.status = falcon.HTTP_404
        res = self.get("/food/ingredients/search", f"&query={ingredient}")
        
        if res == None:
            logger.info("Failure to get nutrition")
            return

        media = res.json()["results"]

        if not len(media) > 0:
            logger.info(f"Ingredient {ingredient} did not have any search results!")
            return

        # Get the first match of the query
        id = media[0]["id"]
        
        res = self.get(f"/food/ingredients/{id}/information", "&amount=1")

        if res == None:
            logger.info(f"Coudn't get nutrition facts for {ingredient} with id {id}")
            return
        
        resp.status = falcon.HTTP_200
        resp.text = res.text


    # Fetches recipes based on the given ingredienent, e.g. "Apple" or "Orange"
    async def on_get_recipes(self, _: Request, resp: Response, ingredient: str) -> None:
        resp.status = falcon.HTTP_404
        res = self.get("/recipes/findByIngredients", f"&ingredients={ingredient}&number=3")
        if res == None:
            logger.info(f"Failure to get recipes for {ingredient}")
            return
        
        ret = []
        for obj in res.json():
            id = obj["id"]
            res = self.get(f"/recipes/{id}/information", "&includeNutrition=false")

            if res == None:
                logger.info(f"Failed to get recipe information")
                continue
                
            ret.append(res.json())
        
        # Fail if we have no recipes
        if len(ret) == 0:
            return
        
        resp.status = falcon.HTTP_200
        resp.text = json.dumps(ret)
        resp.content_type = "image/png"
