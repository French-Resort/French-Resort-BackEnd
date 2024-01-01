FROM python:3.11

RUN python -m pip install --upgrade pip

WORKDIR /frenchResortFront

COPY requirements.txt requirements.txt

COPY ./src/ .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5001

CMD [ "python", "app.py" ]
