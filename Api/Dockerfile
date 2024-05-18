FROM python:3.9
WORKDIR /app
COPY . /app
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    tesseract-ocr \
    tesseract-ocr-rus 
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
