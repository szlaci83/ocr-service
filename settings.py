# settings file for the different parts of the system
from anonutils import disp_img
from pprint import pprint
import logging

# Setting for verbose printing and displaying images
VERBOSE = True
VERBOSE_DISP = False
pretty_verbose_print = pprint if VERBOSE else lambda *a, **k: None
verbose_display = disp_img if VERBOSE_DISP else lambda *a, **k: None

# Logging level
LOGGING_LEVEL = logging.DEBUG
# logfile's name  or empty string for console logging
# logs/anon.log
LOGFILE = ''

# OCR settings
TESSERACT = 0
ENGLISH = 0
DEFAULT_RESOLUTION = 150
PREPROCESS = True

# HTTP settings
PORT = 4567
HOST = "0.0.0.0"
OK = 200
