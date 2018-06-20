import cv2
from flask import jsonify, make_response
import numpy as np
import base64

def jpg_encode(img):
    '''
    Converts image to a numpy array
    :param img: image file
    :return: numpy array of the file
    '''
    ret, mat = cv2.imencode('.jpg', img)
    return mat


def jpg_decode(img):
    '''
    Converts numpy array to jpg
    :param img: numpy array of an image
    :return: jpg file bytes of the image
    '''
    nparray = np.fromstring(img, np.uint8)
    return cv2.imdecode(nparray, cv2.IMREAD_COLOR)


def disp_img(name, img):
    '''
    displays an image on the screen
    :param name: name of the window
    :param img: the image
    :return: None
    '''
    cv2.imshow(name, img)
    cv2.waitKey(0)


def add_headers(response, http_code):
    '''
    Wraps a Http response and a given http code into CORS and JSON headers
    :param response: The response to wrap
    :param http_code: The http code to wrap
    :return: the wrapped HTTP response with headers
    '''
    response = jsonify(response), http_code
    response = make_response(response)
    response.headers['Access-Control-Allow-Origin'] = "*"
    response.headers['content-type'] = "application/json"
    return response


def validate_req(req, fields):
    '''
    Validates a http request against a list of required fields
    :param req: the http request
    :param fields: the required fields
    :return: False if the request does not contain all the required fields, True otherwise
    '''
    for field in fields:
        if not req.json or not field in req.json:
            return False
    return True


def add_contrast(img):
    '''
    Adds contrast to an image
    :param img: the image as a numpy array
    :return: the image with increased contrast
    '''
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    limg = cv2.merge((cl, a, b))
    result = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    return result


def add_contrast2(img):
    '''
    Adds contrast to an image
    :param img: the image as a numpy array
    :return: the image with increased contrast
    '''
    hist, bins = np.histogram(img.flatten(), 256, [0, 256])
    cdf = hist.cumsum()
    cdf_normalized = cdf * hist.max() / cdf.max()
    #plot(cdf_normalized)
    cdf_m = np.ma.masked_equal(cdf, 0)
    cdf_m = (cdf_m - cdf_m.min()) * 255 / (cdf_m.max() - cdf_m.min())
    cdf = np.ma.filled(cdf_m, 0).astype('uint8')
    result = cdf[img]
    return result


def to_gray(img):
    '''
    Creates the grayscale version of an image
    :param img:
    :return:
    '''
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gray


def mser_preprocess(img):
    '''
    Preprocessing function for MSER service
    uses bilateral filter, adds contrast, and converts to grayscale
    :param img: the image to be preprocessed
    :return: the preprocessed image
    '''
    img = cv2.bilateralFilter(img, 5, 5, 5)
    img = add_contrast2(img)
    img = to_gray(img)
    return img


def to_base64_str(filepath):
    '''
    Converts a file to base64 string
    :param filepath: the location of the file
    :return: the base64 encoded file
    '''
    with open(filepath, "rb") as image_file:
        encoded_string = base64.encodebytes(image_file.read())
    return encoded_string.decode("utf-8")


def ocr_preprocess(img):
    '''
    Pre-process function for the OCR service
    adds contrast, converts to B&W
    :param img: the image to be preprocessed
    :return: the preprocessed image
    '''
    img = add_contrast(img)
    img_grey = to_gray(img)
    # To B&W :
    (thresh, img) = cv2.threshold(img_grey, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    img = cv2.threshold(img_grey, thresh, 255, cv2.THRESH_BINARY)[1]
    return img


def to_array(img):
    '''
    re-open the image as numpy array
    :param img: image to convert
    :return: converted image
    '''
    img.save(filename="temp/temp.jpg")
    return cv2.imread("temp/temp.jpg")

    ###################################################################################################################
    # After reading this lots of python code, lets sing a song (afterall the project is dedicated to my daughters too):
    # See the little bunnies sleeping til it’s nearly noon
    # Shall we wake them with a merry tune?
    # They're so still, are they ill?
    # No! Wake up bunnies!
    # Hop little bunnies, hop, hop, hop
    # Hop little bunnies, hop, hop, hop
    # Hop little bunnies, hop, hop, hop
    # Hop little bunnies, hop and stop

if __name__ == '__main__':
    pass
