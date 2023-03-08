.DEFAULT_GOAL := default
#################### PACKAGE ACTIONS ###################

env:
	@pyenv virtualenv 3.10.6 deepdipper
	@pyenv local deepdipper

install:
	@pip install --upgrade pip
	@pip install -r requirements.txt

run:
	@python app.py

streamlit:
	@streamlit run app.py


################### DATA SOURCES ACTIONS ################

# Data sources: targets for monthly data imports
ML_DIR=~/.deepdipper
URL1=https://drive.google.com/file/d/1n_f7ermdFkAx52WAHMyHsxwh3A-k6dRL/view?usp=share_link
URL2=https://drive.google.com/file/d/1c477S829DpSr2xOIauoGaoPKeJaC4Map/view?usp=share_link

# to add once we have: GS_DIR=gs://datascience-mlops/taxi-fare-ny

create_dir:
	mkdir ${ML_DIR}
	mkdir ${ML_DIR}/data/
	mkdir ${ML_DIR}/data/raw
	mkdir ${ML_DIR}/data/processed
	mkdir ${ML_DIR}/training_outputs
	mkdir ${ML_DIR}/training_outputs/metrics
	mkdir ${ML_DIR}/training_outputs/models
	mkdir ${ML_DIR}/training_outputs/params

reset_local_files:
	rm -rf ${ML_DIR}
	mkdir -p ${ML_DIR}/data/
	mkdir ${ML_DIR}/data/raw
	mkdir ${ML_DIR}/data/processed
	mkdir ${ML_DIR}/training_outputs
	mkdir ${ML_DIR}/training_outputs/metrics
	mkdir ${ML_DIR}/training_outputs/models
	mkdir ${ML_DIR}/training_outputs/params

download:
	-curl ${URL1} > ${ML_DIR}/data/arxiv-metadata-oai-snapshot.json
	-curl ${URL2} > ${ML_DIR}/data/arxiv-metadata-ext-citation.csv
