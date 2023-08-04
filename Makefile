install:
	pip install --upgrade pip &\
		pip install -r requirements.txt
	CT_CUBLAS=1 pip install ctransformers --no-binary ctransformers

format:
	black *.py

ingest:
	python ingest.py