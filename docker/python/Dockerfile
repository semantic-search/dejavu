FROM python:3.7
RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install \
    gcc nano \
    ffmpeg libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0 \
    postgresql postgresql-contrib -y
RUN pip install numpy scipy matplotlib pydub pyaudio psycopg2

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . ./

RUN chmod +rwx wait-for-it.sh
# CMD uvicorn --host=0.0.0.0 --port 8080 api:app --reload
# CMD ["python", "main.py"]