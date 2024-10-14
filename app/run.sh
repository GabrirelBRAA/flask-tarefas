#!/bin/sh 

set -e

openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -sha256 -days 3650 -nodes -subj "/C=XX/ST=StateName/L=CityName/O=CompanyName/OU=CompanySectionName/CN=CommonNameOrHostname"

uwsgi --https 0.0.0.0:5000,cert.pem,key.pem --workers 4 --master --enable-threads --module app:app 