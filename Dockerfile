FROM python:3.10.6
#FROM --platform=linux/amd64 tensorflow/tensorflow:2.10.0

EXPOSE 8077

COPY research_pulse research_pulse
COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt


#CMD make run_api
CMD uvicorn research_pulse.api.fast:app --host 0.0.0.0 --port 8077
