# Fruitrient

[![license](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](./LICENSE)
[![pipeline](https://git.chalmers.se/courses/dit825/2021/group07/fruitrient/badges/main/pipeline.svg)](https://git.chalmers.se/courses/dit825/2021/group07/fruitrient/-/commits/main)

This README document is a guide of how to use Fruitrient and it's features.

### Introduction

Fruitrient is for those who seek motivation in achieving a healthy lifestyle, gaining more nutritional information or for those who simply want to identify a fruit. It has an intuitive user interface which is easy to use for everyone.

Just upload or take a photo of your desired fruit to recieve
the name, nutrient values, condition of the fruit and last but not least, different recipe suggestions for inspiration.

### Installation

```bash
# Clone Repository
git clone git@git.chalmers.se:courses/dit825/2021/group07/fruitrient.git
```

More information can be found in the [backend](backend/README.md) and [frontend](frontend/README.md) directories.

### Features

As mentioned above, there are two ways of uploading photos to Fruitrient as a user. The first option is to drag and drop a saved photo from your device, which the system will upload and process. The second option is to take a picture via webcam, where the user will be asked to first grant camera access, which the system then will upload and process. After the image has been recieved, either from uploading or the webcam, Fruitrient immdeately processes the image to identify the type of fruit and it's quality (fresh or rotten). It then provides the user with the information along with nutrition data and recipe suggestions for the identified fruit.

An overview of the different features for both of the profiles are listed below

#### Admin

- Uploading new image data with labels
- Uploading new models
- Run performance checks
- Retrain models
- Switching between models
- View previous models' performance

#### User

- Drag and drop images for uploading a photo
- Using the webcam to take live images
- Receive fruit name and quality (fresh/rotten/stale) to make sure you know what you're eating
- Get nutritional data of a given fruit after you upload an image to stay on top of your health
- Get recipes for your fruit to make it more delicious and exquisite

### Tech

Fruitrient uses a number of open source projects and libraries:

- [Python](https://www.python.org/)
- [Svelte](https://svelte.dev/)
- [Keras](https://keras.io/)
- [scikit-learn](https://scikit-learn.org/stable/)

## Activity Log

Detailed information on our weekly meetings and discussions are documented in the [activity log](documentation/activity-log.md).
