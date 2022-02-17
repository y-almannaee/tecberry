# Comments are preserved for posterity

# Use phusion/baseimage as base image. To make your builds reproducible, make
# sure you lock down to a specific version, not to `latest`!
# See https://github.com/phusion/baseimage-docker/blob/master/Changelog.md for
# a list of version numbers.
FROM phusion/baseimage:focal-1.1.0

# Use baseimage-docker's init system.
CMD ["/sbin/my_init"]

# ...put your own build instructions here...
RUN apt-get update && apt-get upgrade -y -o Dpkg::Options::="--force-confold"
RUN apt-get update && /sbin/install_clean curl build-essential libpcre3 libpcre3-dev zlib1g zlib1g-dev libssl-dev openssl libgd-dev libxml2 libxml2-dev uuid-dev git
RUN git clone --depth 1 https://github.com/arut/nginx-rtmp-module && git clone --depth 1 https://github.com/aperezdc/ngx-fancyindex && curl https://nginx.org/download/nginx-1.21.6.tar.gz -o nginx-1.21.6.tar.gz && tar xvf nginx-1.21.6.tar.gz
RUN /bin/bash -c 'cd nginx-1.21.6/ && ./configure \
--prefix=/etc/nginx \
--sbin-path=/usr/sbin/nginx \
--conf-path=/etc/nginx/nginx.conf \
--error-log-path=/var/log/nginx/error.log \
--http-log-path=/var/log/nginx/access.log \
--pid-path=/var/run/nginx.pid \
--lock-path=/var/run/nginx.lock \
--http-client-body-temp-path=/var/cache/nginx/client_temp \
--http-proxy-temp-path=/var/cache/nginx/proxy_temp \
--http-fastcgi-temp-path=/var/cache/nginx/fastcgi_temp \
--http-uwsgi-temp-path=/var/cache/nginx/uwsgi_temp \
--http-scgi-temp-path=/var/cache/nginx/scgi_temp \
--user=www-data \
--group=www-data \
--with-http_ssl_module \
--with-http_realip_module \
--with-http_addition_module \
--with-http_sub_module \
--with-http_dav_module \
--with-http_flv_module \
--with-http_mp4_module \
--with-http_gunzip_module \
--with-http_gzip_static_module \
--with-http_random_index_module \
--with-http_secure_link_module \
--with-http_stub_status_module \
--with-http_auth_request_module \
--with-file-aio \
--with-http_v2_module \
--with-ipv6 \
--with-threads \
--with-stream \
--with-stream_ssl_module \
--with-http_slice_module \
--add-module=/nginx-rtmp-module \
--add-module=/ngx-fancyindex\
--with-cc-opt='-O2 -flto -funsafe-math-optimizations -fstack-protector-strong -fstack-clash-protection -pipe --param=ssp-buffer-size=4 -Wp,-D_FORTIFY_SOURCE=2' \
&& mkdir /var/cache/nginx && make && make install && mkdir /etc/nginx && mkdir /etc/nginx/sites-enabled && mkdir /etc/nginx/certs'

RUN mv /etc/nginx/nginx.conf /etc/nginx/nginx_default.conf
COPY nginx-conf/nginx.conf /etc/nginx/nginx.conf
COPY nginx-conf/main_server /etc/nginx/sites-enabled
COPY nginx-conf/ffdhe2048.txt /etc/nginx/ffdhe2048.txt
COPY nginx-conf/selfsigned.crt /etc/nginx/certs/certificate.crt
COPY nginx-conf/selfsigned.key /etc/nginx/certs/certificate.key

RUN mkdir /etc/service/nginx
COPY run-nginx.sh /etc/service/nginx/run
RUN adduser --system --no-create-home --shell /bin/false --group --disabled-login www-data && chmod +x /etc/service/nginx/run

# Clean up APT when done.
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*