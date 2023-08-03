install:
	pip install --upgrade pip &\
		pip install -r requirements.txt

format:
	black *.py

ingest:
	python ingest.py