FROM python:3.10-slim

WORKDIR /app

RUN pip install --upgrade pip setuptools
RUN pip install pipenv

COPY Pipfile* .
RUN pipenv install --system --deploy --ignore-pipfile

COPY . /app

CMD ["/bin/bash", "-c", "streamlit run main.py"]