FROM python:3.12

WORKDIR /fastapalchemy

COPY . /fastapalchemy

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "broker.py"]