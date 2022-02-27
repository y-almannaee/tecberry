#!/bin/sh

rm -r /etc/nginx/certs || :
mkdir -p /etc/nginx/certs
cp /var/lib/peltier_controller/certificates/*.key /etc/nginx/certs/certificate.key
cp /var/lib/peltier_controller/certificates/*.issuer.crt /etc/nginx/certs/certificate.issuer.crt
cp /var/lib/peltier_controller/certificates/*[^issuer].crt /etc/nginx/certs/certificate.crt
cp /etc/nginx/default-site-conf/main_server /etc/nginx/sites-enabled
sed -i \
-e 's@#INCLUDEOCSPSTAPLING@# OCSP stapling\
	ssl_stapling on;\
	ssl_stapling_verify on;\
\
	# verify chain of trust of OCSP response using Root CA and Intermediate certs\
	ssl_trusted_certificate /etc/nginx/certs/certificate.issuer.crt;@' \
-e 's/#INCLUDESERVERNAME/server_name '"$HOSTNAME"';/' /etc/nginx/sites-enabled/main_server