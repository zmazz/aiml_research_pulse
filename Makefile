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
ML_DIR=~/.data_deepdipper
URL1=https://drive.google.com/file/d/1n_f7ermdFkAx52WAHMyHsxwh3A-k6dRL/view?usp=share_link
URL2=https://drive.google.com/file/d/1c477S829DpSr2xOIauoGaoPKeJaC4Map/view?usp=share_link

# to add once we have: GS_DIR=gs://datascience-mlops/taxi-fare-ny

reset_local_files:
	rm -rf ${ML_DIR}
	mkdir ${ML_DIR}

download:
	-curl ${URL1} > ${ML_DIR}/arxiv-metadata-oai-snapshot.json
	-curl ${URL2} > ${ML_DIR}/arxiv-metadata-ext-citation.csv
