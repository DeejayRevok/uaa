# uaa
News service Universal Authenticator and Authorizator microservice

![UAA Service](https://github.com/DeejayRevok/uaa/workflows/UAA%20Service/badge.svg?branch=develop)
[![codecov](https://codecov.io/gh/DeejayRevok/uaa/branch/develop/graph/badge.svg)](https://codecov.io/gh/DeejayRevok/uaa)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=DeejayRevok_uaa&metric=alert_status)](https://sonarcloud.io/dashboard?id=DeejayRevok_uaa)

#### Local running

Run the parent's repo dev docker compose.

Inside the application folder run:
```
export JWT_SECRET={JWT_TOKEN_SECRET}
export PYTHONPATH={FULL_PATH_TO_APPLICATION_FOLDER}
pip install -r requirements.txt
python webapp/main.py -p local
```
