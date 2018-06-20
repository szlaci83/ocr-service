import base64
import logging
import ocr_service as service
from flask import Flask, request
from flask_cors import CORS

from settings import PORT, HOST, OK, LOGGING_LEVEL, LOGFILE
from errormessages import *
from anonutils import add_headers, validate_req

app = Flask(__name__)
CORS(app)

@app.route("/ocr", methods=['POST'])
def ocr_only():
    logging.info('REQUEST: ' + str(request))
    fields = ['content', 'filetype', 'lang']
    if not validate_req(request, fields):
        logging.error(str(JSON_ERROR))
        return add_headers(JSON_ERROR, JSON_ERROR['code'])

    req_json = request.json
    LANG = service.avail_langs()

    # setting the language for OCR (the right index from available languages set by POST request)
    try:
        lang = LANG[req_json['lang']]
    except(KeyError):
        logging.error(str(LANG_ERROR) + str(req_json['lang']))
        return add_headers(LANG_ERROR, LANG_ERROR['code'])

    # cut the 'base64' prefix from the base64 string in the content
    if req_json['content'].find(",") >= 0:
        content = req_json['content'].split(",")[1]
    else:
        content = req_json['content']

    # deciding what filetype needs to be ocr-ed
    if req_json['filetype'] == 'pdf':
        logging.info('RECEIVED: PDF')
        try:
            txt = service.ocr_pdf(base64.b64decode(content), lang)
        except:
            logging.error(str(OCR_PDF_ERROR))
            return add_headers(OCR_PDF_ERROR, OCR_PDF_ERROR['code'])

    elif req_json['filetype'] == 'jpg':
        logging.info('RECEIVED: JPG')
        # try:
        txt = service.ocr_jpg(base64.b64decode(content), lang)
        # except:
        #     logging.error(str(OCR_JPG_ERROR))
        #     return add_headers(OCR_JPG_ERROR, OCR_JPG_ERROR['code'])
    else:
        logging.error(str(FILETYPE_ERROR) + str(req_json['filetype']))
        return add_headers(FILETYPE_ERROR, FILETYPE_ERROR['code'])
    logging.info('OCR-ed text: ' + str(txt))
    record = {}
    record['text'] = txt
    return add_headers(record, OK)


@app.route("/languages", methods=['GET'])
def get_available_languages():
    '''
    GET languages
    :return: the available languages in the system
    '''
    logging.info('REQUEST: ' + str(request))
    try:
        langs = service.avail_langs()
    except:
        logging.error(str(GET_LANG_ERROR))
        return add_headers(GET_LANG_ERROR, GET_LANG_ERROR['code'])
    return add_headers(langs, OK)


if __name__ == "__main__":
    if LOGFILE and LOGFILE != '':
        print("running on: " + str(HOST) + ":" + str(PORT) + " see " + LOGFILE + " for details!")
    logging.basicConfig(filename=LOGFILE, level=LOGGING_LEVEL, format="%(asctime)s:%(levelname)s:%(message)s")
    app.run(host=HOST, port=PORT)
