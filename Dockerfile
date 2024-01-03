FROM python:3-slim-buster

RUN apt update

RUN apt-get install libgl1-mesa-glx -y

RUN apt-get install libglib2.0-0 -y

WORKDIR /app

COPY requirements.txt .

RUN pip install opencv-python-headless --force-reinstall

RUN pip install -r requirements.txt

COPY . .

EXPOSE 7000
CMD ["uvicorn", "main:app", "--reload", "--host=0.0.0.0", "--port=7000"]