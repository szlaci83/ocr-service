# File to store the custom error messages returned by the API
JSON_ERROR = {"error": "Bad request", "code": "400", "message": "Field missing, or bad format!"}
LANG_ERROR = {"error": "Exception", "code": "400", "message": "UNKNOWN LANGUAGE"}
FILETYPE_ERROR = {"error": "Exception", "code": "400", "message": "UNKNOWN FILE TYPE"}
OCR_PDF_ERROR = {"error": "Exception", "code": "500", "message": "FAILED TO OCR PDF"}
OCR_JPG_ERROR = {"error": "Exception", "code": "500", "message": "FAILED TO OCR JPG"}
DEC_STORE_ERROR = {"error": "Exception", "code": "500", "message": "FAILED DECOMPOSE & STORE"}
STORE_ERROR = {"error": "Exception", "code": "500", "message": "FAILED TO STORE"}
ID_LIST_ERROR = {"error": "Exception", "code": "500", "message": "FAILED TO GET ID LIST"}
GET_BY_ID_ERROR = {"error": "Exception", "code": "500", "message": "FAILED TO GET DOCUMENT BY ID"}
GET_LANG_ERROR = {"error": "Exception", "code": "500", "message": "FAILED TO GET AVAILABLE LANGUAGES"}
