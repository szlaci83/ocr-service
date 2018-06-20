FROM python:3
RUN mkdir /ocr
WORKDIR /ocr
RUN mkdir /ocr/logs
RUN mkdir /ocr/temp
COPY *.py /ocr/
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils
RUN apt-get install tesseract-ocr -y
RUN apt-get install tesseract-ocr-eng -y
RUN apt-get install tesseract-ocr-chi-sim -y
RUN apt-get install tesseract-ocr-chi-tra -y
COPY requirements.txt /ocr
RUN pip3 install -r /ocr/requirements.txt
EXPOSE 4567
CMD ["python3", "/ocr/rest_api.py"]