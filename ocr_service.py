# better dataset:
# https://github.com/tesseract-ocr/tesseract/wiki/Data-Files
#
# denoise:
# http://www.fmwconcepts.com/imagemagick/textcleaner/index.php
#
# https://www.imagemagick.org/script/fx.php
import base64
import io
import pyocr.builders
import logging
from PIL import Image as PI
from wand.image import Image, Color
from settings import DEFAULT_RESOLUTION, PREPROCESS, TESSERACT, ENGLISH
from anonutils import ocr_preprocess, jpg_encode, jpg_decode


def _init(Tool = TESSERACT, Lang = ENGLISH):
    '''
    Initialises OCR by selecting the tool and language
    :param Tool: the required OCR tool (Tesseract is default)
    :param Lang: the required language (English is default)
    :return:
    '''
    try:
        selected_tool = pyocr.get_available_tools()[Tool]
        selected_lang = selected_tool.get_available_languages()[Lang]
    except:
        logging.error("ERROR DURING INITIALIZATION IN OCR SERVICE!")
        raise ValueError
    logging.info('SELECTED LANGUAGE: ' + selected_lang)
    return selected_tool, selected_lang


def _pdf_to_jpeg(file_bytes, res=DEFAULT_RESOLUTION):
    '''
    Converts pdf file to jpg
    :param file_bytes: the pdf file as bytes
    :param res: the resolution to use for the output
    :return: the converted file
    '''
    logging.info("CONVERTING PDF to JPG")
    try:
        pdf = Image(blob=file_bytes, resolution=res)
    except:
        logging.error("ERROR DURING PDF TO JPG CONVERSION IN OCR SERVICE!")
        raise ValueError
    return pdf.convert('jpeg')


def _blobbing(image):
    '''
    Blobbing function with preprocessing
    :param image: the image to be blobbed
    :return: sequence of wand images
    '''
    images = []
    logging.info("BLOBBING...")
    # preprocessing using WAND...
    try:
        for img in image.sequence:
            img_page = Image(image=img)
            img_page.background_color = Color('white')
            img_page.level(black=0.2, white=None, gamma=0.2, channel=None)
            img_page.normalize()
            img_page.auto_orient
            images.append(img_page.make_blob('jpeg'))
    except:
        logging.error("ERROR DURING BLOBBING IN OCR SERVICE!")
        raise ValueError
    return images


def _ocr(tool, lang, images):
    '''
    Extracts text from images
    :param tool: The OCR tool
    :param lang: The language to do the ocr with
    :param images: collection of images to be OCR-ed
    :return: the text OCR-ed from the images
    '''
    # https://github.com/openpaperwork/pyocr
    text = []
    logging.info("OCR images")
    try:
        for img in images:
            txt = tool.image_to_string(
                PI.open(io.BytesIO(img)),
                lang=lang,
                builder=pyocr.builders.TextBuilder()
            )
            text.append(txt)
    except:
        logging.error("ERROR DURING OCR-ING IN OCR SERVICE!")
        raise ValueError
    logging.info('THE EXTRACTED TEXT: ' + txt)
    return txt


def ocr_jpg(file_bytes, selected_lang, res=DEFAULT_RESOLUTION):
    '''
    Text recognition on JPG files
    :param file_bytes: the JPG file bytes
    :param selected_lang: the language to do the ocr with
    :param res: the resolution
    :return: the ocr-ed text
    '''
    try:
        tool, lang = _init(Lang=selected_lang)
        file_bytes = jpg_decode(file_bytes)
        logging.info("PREPROCESSING: " + str(PREPROCESS))
        if PREPROCESS:
            blob = ocr_preprocess(file_bytes)
        blob = jpg_encode(blob)
        pic = Image(blob=blob, resolution=res)
        pic = pic.convert('jpeg')
        pics = _blobbing(pic)
    except:
        logging.error("ERROR DURING OCR-ING JPG IN OCR SERVICE!")
        raise ValueError
    return _ocr(tool, lang, pics)


def ocr_pdf(file_bytes, selected_lang):
    '''
    Text recognition on PDF files
    :param file_bytes: the PDF file bytes
    :param selected_lang: the language to do the ocr with
    :return: the ocr-ed text
    '''
    try:
        tool, lang = _init(Lang=selected_lang)
        pic = _pdf_to_jpeg(file_bytes)
        # TODO : try to call ocr_jpg here
        pics = _blobbing(pic)
    except:
        logging.error("ERROR DURING OCR-ING PDF IN OCR SERVICE!")
        raise ValueError
    return _ocr(tool, lang, pics)


def avail_langs():
    '''
    Details of available languages
    :return: The dict of available languages {name: id}
    '''
    try:
        selected_tool = pyocr.get_available_tools()[0]
        langs = selected_tool.get_available_languages()
        lang_dict = {}
        for i in range(len(langs)):
            lang_dict[langs[i]] = i
    except:
        logging.error("ERROR DURING GETTING AVAILABLE LANGUAGES IN OCR SERVICE!")
        raise ValueError
    return lang_dict


def _example():
    '''
    Example usage of OCR service
    :return: None
    '''
    INPUT_FILE = 'Data/input/pic/t7.jpg'
    with open(INPUT_FILE, "rb") as image_file:
        encoded_string = base64.b64encode((image_file.read()))
    print(type(base64.b64decode(encoded_string)))
    print(ocr_jpg(base64.b64decode(encoded_string), 0))
    print(avail_langs())


if __name__ == '__main__':
    _example()
