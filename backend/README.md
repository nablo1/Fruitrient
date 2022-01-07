# Fruitrient backend

The place where the fruitrient's ML and HTTP interface are implemented.

## Usage
Create a virtual environment
```
python -m venv .venv
source .venv/bin/activate
```
Install dependencies
```
pip install -r requirements.txt
```
Run the app
```
daphne fruitrient.asgi:app
```

The backend also requires a spoonacular api key to function 100% properly, once you have a key put it inside the .env file.
