from python:3.8.10

WORKDIR /gourmandapi

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "gourmandapiapp.main:app", "--host", "0.0.0.0", "--port", "8000"]