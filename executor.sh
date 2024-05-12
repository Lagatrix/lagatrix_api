source /opt/lagatrix-api/venv/bin/activate
source /opt/lagatrix-api/lagatrix.conf

if [ "$ssl" = "true" ]; then
  uvicorn main:app --host $host --port $port --ssl-keyfile $ssl_key_file --ssl-certfile $ssl_cert_file
else
  uvicorn main:app --host $host --port $port
fi
