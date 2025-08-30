run:
	uvicorn app.main:app --reload --port 8000

install:
	pip install -r requirements.txt
