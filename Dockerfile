FROM --platform=linux/amd64 python:3.10.6
#FROM --platform=linux/amd64 tensorflow/tensorflow:2.10.0

COPY research_pulse research_pulse
COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python -m nltk.downloader all -d /usr/local/nltk_data


CMD uvicorn research_pulse.api.fast:app --host 0.0.0.0 --port $PORT
#CMD streamlit run --server.port 8080 --server.enableCORS false research_pulse.interface.app.py
