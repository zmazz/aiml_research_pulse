.DEFAULT_GOAL := default
#################### PACKAGE ACTIONS ###################

env:
	pyenv virtualenv 3.10.6 deepdipper
	pyenv local deepdipper

install:
	pip install --upgrade pip
	pip install -r requirements.txt

run:
	python app.py

streamlit:
	streamlit run research_pulse/interface/app.py

streamlit2:
	streamlit run research_pulse/interface/app2.py

streamlit3:
	streamlit run research_pulse/interface/app3.py

run_api:
	uvicorn research_pulse.api.fast:app --reload

################### DATA SOURCES ACTIONS ################

# Data sources: targets for monthly data imports
ML_DIR=~/.deepdipper

## TO UPDATE WITH GCS
URL1=https://drive.google.com/file/d/1n_f7ermdFkAx52WAHMyHsxwh3A-k6dRL/view?usp=share_link
URL2=https://drive.google.com/file/d/1c477S829DpSr2xOIauoGaoPKeJaC4Map/view?usp=share_link

GS_DIR=gs://deepdipper_data

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

download_locally:
	-curl ${URL1} > ${ML_DIR}/data/arxiv-metadata-oai-snapshot.json
	-curl ${URL2} > ${ML_DIR}/data/arxiv-metadata-ext-citation.csv

## written myself
copy_to_gcs:
	gsutil cp -r ~/deepdipper/data/processed/aiml_arxiv_with_cit.csv  gs://deepdipper_data/data/processed/aiml_arxiv_with_cit.csv

load_to_gbq:
	bq load --autodetect arxiv.cleaned_merged gs://deepdipper_data/data/processed/aiml_arxiv_with_cit_chunk1.json
## for loading to bq, use bq interface and select right entries

#### not tested
reset_bq_files:
	-bq rm --project_id ${GCP_PROJECT} ${BQ_DATASET}.cleaned_merged
	-bq rm --project_id ${GCP_PROJECT} ${BQ_DATASET}.raw_metadata
	-bq rm --project_id ${GCP_PROJECT} ${BQ_DATASET}.raw_citations
	-bq mk --sync --project_id ${GCP_PROJECT} --location=${BQ_REGION} ${BQ_DATASET}.cleaned_merged
	-bq mk --sync --project_id ${GCP_PROJECT} --location=${BQ_REGION} ${BQ_DATASET}.raw_metadata
	-bq mk --sync --project_id ${GCP_PROJECT} --location=${BQ_REGION} ${BQ_DATASET}.raw_citations

reset_gcs_files:
	-gsutil rm -r ${GS_DIR}
	-gsutil mb -p ${GCP_PROJECT} -l ${GCP_REGION} gs://${BUCKET_NAME}

reset_all_files: reset_local_files reset_bq_files reset_gcs_files
