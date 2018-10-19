#!/usr/bin/env bash
export SECRET_KEY=muthoni
export DATABASE_URL=postgresql+psycopg2://kellen:Kellen@localhost/blogger
export MAIL_USERNAME=muthonkel@gmail.com
export MAIL_PASSWORD=bulgaria36
python3.6 manage.py server
