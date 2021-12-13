# Fruitrient

[![license](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](./LICENSE)
[![pipeline](https://git.chalmers.se/courses/dit825/2021/group07/fruitrient/badges/main/pipeline.svg)](https://git.chalmers.se/courses/dit825/2021/group07/fruitrient/-/commits/main)

This README document is a guide of how to use Fruitrient and it's features.

##### Introduction
> Fruitrient is for those who seek motivation in achieving a healthy lifestyle, 
gaining more nutritional information or for those who simply want to 
identify a fruit. It has an intuitive user interface which is easy to use 
for everyone. Just upload or take a photo of your desired fruit to recieve 
the name, nutrient values, condition of the fruit and last but not least, 
different reciepe suggestions for inspiration.

### Installation

```bash
# Clone Repository
git clone git@git.chalmers.se:courses/dit825/2021/group07/fruitrient.git
```

### Front page

Here the user will choose on of the two profile options to continue:
- Admin
- User

### Features

As mentioned above, there are two ways of providing Fruitrient with photos. The first option is two drag and drop a saved photo for the system to upload and process. The second option is to take a live photo, where the user will be asked to first grant the camera access, which the system then will upload and process. After the image has been recieved, either from uploading or the webcam, Fruitrient immdeately processes to identify the type of fruit but also its condition (fresh or rotten). It then provides the user with the information along with nutrition data and reciepe suggestions for the identified fruit.

An overwiev of the different features for both of the profiles are listed below
##### Admin

- Drag and drop images for uploading a photo
- Uploading new image data with labels
- Uploading new models
- Switching between models
- Looking over the performance

##### User

- Receive fruit name and quality (fresh/rotten/stale) to make sure you know what you're eating
- Get nutritional data of a given fruit after you upload an image to stay on top of your health 
- Get recipes for your fruit to make it more delicious and exquisite 
- Drag and drop images for uploading a photo
- Allowing access to the webcam and then turning it on for taking a photo

### Tech

Fruitrient uses a number of open source projects to work properly:

- [Python]
- [Svelte]
- [Tailwind]
- [Chart.js]

## Activity Log

Detailed information on our weekly meetings and discussions are 
documented in the [activity log](documentation/activity-log.md).
