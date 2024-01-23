#!/bin/bash
# tail -f /dev/null
# pipenv shell
pipenv run python -m gourmandapiapp.models
pipenv run uvicorn gourmandapiapp.main:app --host 0.0.0.0 --port 8000 --reload --ssl-keyfile=./private_key.pem --ssl-certfile=./certificate.pem 
# \
    # --header Strict-Transport-Security:max-age=31536000


# openssl req -x509 -newkey ec -pkeyopt ec_paramgen_curve:secp384r1 -days 3650 \
#   -nodes -keyout private_key.pem -out certificate.pem -subj "/CN=localhost" \
#   -addext "subjectAltName=DNS:localhost"