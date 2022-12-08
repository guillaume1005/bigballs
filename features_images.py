import time

date = time.time()
import os
from PIL import Image
from dataclassy import values
from torchvision import transforms
import numpy as np
import torch
from tqdm import tqdm
from torchvision import models
import requests
from io import BytesIO


# import matplotlib.pyplot as plt
import pandas as pd
from numpy.testing import assert_almost_equal

# import pickle
import json

# print("importing finished", f"{time.time()-date}")

# needed input dimensions for the CNN
inputDim = (224, 224)
inputDir = (
    "../../JupyterNotebooks/ImageRecommenderResnet18/images"  # change here the model ?
)
inputDirCNN = "../../JupyterNotebooks/ImageRecommenderResnet18/newImages"


# calculating feature vectors add column and line to similarity matrix

# date = time.time()


class Img2VecResnet18:
    def __init__(self):

        self.device = torch.device("cpu")
        self.numberFeatures = 512
        self.modelName = "resnet-18"
        self.model, self.featureLayer = self.getFeatureLayer()
        self.model = self.model.to(self.device)
        self.model.eval()
        self.toTensor = transforms.ToTensor()
        self.normalize = transforms.Normalize(
            mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)
        )

    def getVec(self, img):
        tensorImage = self.toTensor(img)
        image = self.normalize(tensorImage).unsqueeze(0).to(self.device)
        embedding = torch.zeros(1, self.numberFeatures, 1, 1)

        def copyData(m, i, o):
            embedding.copy_(o.data)

        h = self.featureLayer.register_forward_hook(copyData)
        self.model(image)
        h.remove()

        return embedding.numpy()[0, :, 0, 0]

    def getFeatureLayer(self):
        cnnModel = models.resnet18(pretrained=True)
        layer = cnnModel._modules.get("avgpool")
        self.layer_output_size = 512

        return cnnModel, layer


# generate vectors for all the images in the set


def compute_features(
    imgName, buffer, allVectors, img2vec, imageTreated, version="classic"
):
    if version == "classic":
        try:
            # download the image from mongoDb.. or just the link of the image on net
            # buffer = imgName
            # I = Image.open(
            #     buffer
            # )
            # before using buffer
            I = imageTreated

            # the buffer here is not at the good dimension, needs to be imagepath
            # request mongodb
            vec = img2vec.getVec(I)
            allVectors[
                imgName
            ] = vec  # keep this cuz with cmc compute the vectors similar
            mongooseVec = {}
            mongooseVec["image"] = imgName
            mongooseVec["features"] = vec

            # add the new vector to database

            requests.post(
                "http://localhost:3010/addVector", data=mongooseVec
            )  # not necessary to add it to database for cmc
            I.close()

        except Exception as e:
            print(imgName)
            print(e)
    else:  # for cmc
        try:
            # download the image from mongoDb.. or just the link of the image on net
            # buffer = imgName
            I = imageTreated  # work with a buffer BytesIO but also an imagePath
            # request mongodb
            vec = img2vec.getVec(I)
            allVectors[
                imgName
            ] = vec  # keep this cuz after the similarity matrix is with this
            mongooseVec = {}
            mongooseVec["image"] = imgName
            mongooseVec["features"] = vec

            # add the new vector to database

            # requests.post(
            #     "http://localhost:3010/addVector", data=mongooseVec
            # )  # not necessary to add it to database for cmc
            # if the image is in cmc, don't add it to the database
            I.close()

        except Exception as e:
            print(imgName)
            print(e)


def getSimilarityMatrix(vectors):
    v = np.array(list(vectors.values())).T
    sim = np.inner(v.T, v.T) / (
        (np.linalg.norm(v, axis=0).reshape(-1, 1))
        * ((np.linalg.norm(v, axis=0).reshape(-1, 1)).T)
    )
    keys = list(vectors.keys())
    matrix = pd.DataFrame(sim, columns=keys, index=keys)

    return matrix


# top-k list


def top_k(similarityMatrix):
    k = 2
    pd.options.display.max_rows = 4000

    similarNames = pd.DataFrame(index=similarityMatrix.index, columns=range(k))
    similarValues = pd.DataFrame(index=similarityMatrix.index, columns=range(k))

    for j in range(similarityMatrix.shape[0]):  # before tqdm
        kSimilar = similarityMatrix.iloc[j, :].sort_values(ascending=False).head(k)
        similarNames.iloc[j, :] = list(kSimilar.index)
        similarValues.iloc[j, :] = kSimilar.values

    # similarNames.to_pickle("similarNames.pkl")  # dont need to save pickle files
    # similarValues.to_pickle("similarValues.pkl")

    return similarNames, similarValues


def check_similar(similarValues, img):
    if similarValues[1][img] > 0.85:  # before 0.92
        return True
    return False


def getSimilarImages(image, simNames, simVals):
    img = simNames.loc[image, 1]
    val = simVals.loc[image, 1]
    return img, val


def conv_list(allVectors):
    nVectors = {}
    for key in allVectors.keys():
        nVectors[key] = allVectors[key].tolist()
    return nVectors


def conv_array(allVectors):
    nVectors = {}
    for key in allVectors.keys():
        nVectors[key] = np.array(allVectors[key])
    return nVectors


def compute_all_vectors():
    img2vec = Img2VecResnet18()

    allVectors = {}
    print("Converting images to feature vectors:")

    # download all the images from the database
    for image in tqdm(os.listdir(inputDirCNN)):  # make a loop in the database of cmc

        try:
            I = Image.open(os.path.join(inputDirCNN, image))
            # convert to
            vec = img2vec.getVec(I)
            allVectors[image] = vec  # im before here asarray
            I.close()
        except Exception as e:
            print(image)
            print(e)

    buffer = requests.get(
        "http://localhost:3010/imageStream", params={"contract": "bim"}
    ).content

    ImageTreated = Image.open(BytesIO(buffer))

    allVectors = conv_list(allVectors)

    allVectorsFile = open("./allVectors.json", "w")  # put the file in the database
    allVectorsFile.write(json.dumps(allVectors))
    allVectorsFile.close()


def convert_all():
    os.makedirs(inputDirCNN, exist_ok=True)
    transformationForCNNInput = transforms.Compose([transforms.Resize(inputDim)])

    # functions that modify an image in directory
    # convert_all
    for imageName in os.listdir(inputDir):  # loop on the database

        I = Image.open(os.path.join(inputDir, imageName)).convert("RGB")
        newI = transformationForCNNInput(I)

        # copy the rotation information metadata from original image and save, else your transformed images may be rotated

        # print(imageName)
        newI.save(os.path.join(inputDirCNN, imageName))  # put in the database
        newI.close()
        I.close()


def convert_one(
    buffer,
):  # transform the image path arg into image maybe, before imagePath
    transformationForCNNInput = transforms.Compose([transforms.Resize(inputDim)])

    print("there")
    ImageTreated = Image.open(buffer).convert(
        "RGB"
    )  # open with link plus link of database

    newI = transformationForCNNInput(ImageTreated)
    # print("here is the vec")
    # newI = transformationForCNNInput(I)
    # save in the database for imageCNN, maybe after

    # newI.save(
    #     os.path.join(inputDirCNN, imagePath)
    # )
    # save in the database or local (cuz working short time)
    # newI.close()

    # files = {"image": newI}

    # requests.post(
    #     "http://localhost:3010/uploadImagesCNN", files=files, data={"contract": 100000}
    # )

    return newI


def get_token(imagePath):

    print("in get token")

    infos = json.loads(requests.get("http://localhost:3010/infos").content)

    token = infos[imagePath]

    return token


def compute_features_add(buffer, imgName):  # before buffer
    try:
        # convert new image and add it to inputDirCNN
        print("converting image")

        ImageTreated = convert_one(buffer)  # check the size

        img2vec = Img2VecResnet18()

        # get the vectors form database
        allVectorsString = requests.get("http://localhost:3010/allVectors").content
        allVectors = json.loads(allVectorsString)

        # convert to array
        allVectors = conv_array(allVectors)
        compute_features(imgName, buffer, allVectors, img2vec, ImageTreated)

    except Exception as e:
        print(imgName)
        print(e)


def sim_im(imgName, buffer):
    # buffer = imgName # use this to convert the buffer
    # transform images
    # convert_all()
    # print(buffer)
    ImageTreated = convert_one(buffer)

    # add new image to allVectors

    img2vec = Img2VecResnet18()

    allVectorsString = requests.get("http://localhost:3010/allVectors").content
    allVectors = json.loads(allVectorsString)

    # convert to array
    allVectors = conv_array(allVectors)

    compute_features(
        imgName, buffer, allVectors, img2vec, ImageTreated, 1
    )  # does not add the vector in the database

    similarityMatrix = getSimilarityMatrix(allVectors)

    # top k list

    similarNames, similarValues = top_k(similarityMatrix)

    if check_similar(similarValues, imgName):
        print("/////////////////////////////////////////////////////////////////////")

        img, val = getSimilarImages(imgName, similarNames, similarValues)
        print(f"The image is {img} with {imgName} with val at {val}")
        # change file of tokens to buy
        print(f"got onneeeeee !!! it is {img}")
        print("/////////////////////////////////////////////////////////////////////")

        try:
            token = get_token(img)  # here use img, the similar img
            boss = requests.get(
                "http://localhost:3010/token", params={"token": token}
            )  # to buy
            print(f"here is the boss {boss}")

        except Exception as e:  # requests.exceptions.RequestException
            print("here")
            print(e)
            print(
                f"error in db: surely two cmc images that looks the same, because the image is {img}"
            )

        # buy

        # instead, make an api call to express server
        # buyData = json.loads(requests.get("http://localhost:3010/buyData").content)
        # buyData["newToBuy"] = token
        # requests.post("http://localhost:3010/addBuy", {"newToBuy": token})

        return img

    else:
        img, val = getSimilarImages(imgName, similarNames, similarValues)
        print(
            "##########################################################################"
        )
        print(f"Not enough similarity for {img} with {imgName} with a value of {val}")
        print(
            "##########################################################################"
        )
        return img


# sim_im("1643372334439.png")

# compute_all_vectors()

# use in sim_im
