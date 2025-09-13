run:
	uvicorn app.main:app --app-dir src --reload --port 8000

install:
	pip install -r requirements.txt
