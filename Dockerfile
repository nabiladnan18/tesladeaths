FROM python:3.10-slim

WORKDIR /app

RUN pip install pipenv

COPY Pipfile* .
RUN pipenv install --system --deploy --ignore-pipfile

COPY . /app

CMD ["/bin/bash", "-c", "streamlit run main.py --server.address 0.0.0.0"]