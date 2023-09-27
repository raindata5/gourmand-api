# from python:3.8.10

# ENV NAME="RONALD"

# WORKDIR /gourmandapi

# COPY requirements.txt ./

# RUN pip install --no-cache-dir -r requirements.txt

# COPY . .


FROM ubuntu

ENV NAME="RONALD"

WORKDIR /gourmandapi


RUN apt update

RUN apt-get install -y python3 python3-pip

RUN apt-get install -y libpq-dev python-dev

RUN  PATH=$PATH:/usr/pgsql-9.3/bin/


RUN pip install pipenv

COPY Pipfile ./

COPY requirements.txt ./

RUN pipenv install

RUN pipenv install -r requirements.txt

COPY . .

ENV LANG="C.UTF-8"


RUN python3 -m pip install --upgrade build

RUN python3 -m build --wheel

RUN pipenv install -e .


# ENTRYPOINT []
# ENTRYPOINT ["tail", "-f", "/dev/null"]
ENTRYPOINT [ "pipenv", "run", "gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "gourmandapiapp.main:app", "--bind", "0.0.0.0:8000"]