FROM python:3.11

RUN python -m pip install --upgrade pip

WORKDIR /frenchResortFront

COPY requirements.txt requirements.txt

COPY ./src/ .

RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "app.py" ]
