import cv2
import numpy as np
from insightface.app import FaceAnalysis
from insightface.data import get_image as ins_get_image
app = FaceAnalysis(name='/home/advance/.insightface/models/buffalo_l')


def predict(img):
    image_name = img.split(".")[0]
    app.prepare(ctx_id=0, det_size=(640, 640))
    img = ins_get_image(image_name)
    faces = app.get(img)
    return faces, img