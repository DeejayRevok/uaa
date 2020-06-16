# uaa
News service Universal Authenticator and Authorizator microservice

#### Local running

Run the parent's repo dev docker compose.

Inside the application folder run:
```
export JWT_SECRET={JWT_TOKEN_SECRET}
export PYTHONPATH={FULL_PATH_TO_APPLICATION_FOLDER}
pip install -r uaa/requirements.txt
python uaa/webapp/main.py -p local
```