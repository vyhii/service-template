FROM python:3.8-slim-buster

RUN apt-get update -y

RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN apt-get install -y wget

RUN /usr/local/bin/python -m pip install --upgrade pip

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]