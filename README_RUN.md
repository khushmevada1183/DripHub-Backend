Run (Windows bash):

```bash
.venv/Scripts/activate
bash -lc "python -m pip install -r requirements.txt"
uvicorn app.main:app --reload --port 8000
```