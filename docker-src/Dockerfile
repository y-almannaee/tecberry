# Comments are preserved for posterity

# Use phusion/baseimage as base image. To make your builds reproducible, make
# sure you lock down to a specific version, not to `latest`!
# See https://github.com/phusion/baseimage-docker/blob/master/Changelog.md for
# a list of version numbers.
FROM phusion/baseimage:focal-1.1.0

# Use baseimage-docker's init system.
CMD ["/sbin/my_init"]

# ...put your own build instructions here...
RUN apt-get update && /sbin/install_clean curl build-essential libpcre3 libpcre3-dev zlib1g zlib1g-dev libssl-dev openssl libgd-dev libxml2 libxml2-dev uuid-dev git
RUN git clone --depth 1 https://github.com/arut/nginx-rtmp-module && git clone --depth 1 https://github.com/aperezdc/ngx-fancyindex && curl https://nginx.org/download/nginx-1.21.6.tar.gz -o nginx-1.21.6.tar.gz && tar xvf nginx-1.21.6.tar.gz
RUN /bin/bash -c "cd nginx-1.21.6/ && ./configure \
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
	--add-module=/ngx-fancyindex \
	--with-cc-opt='-O2 -flto -funsafe-math-optimizations -fstack-protector-strong -fstack-clash-protection -pipe --param=ssp-buffer-size=4 -Wp,-D_FORTIFY_SOURCE=2'"
RUN /bin/bash -c 'cd /nginx-1.21.6 && make && make install \
	&& mkdir -p /etc/nginx/sites-enabled && mkdir -p /etc/nginx/certs && mkdir -p /var/cache/nginx \
	&& rm -r /etc/nginx/sites-enabled || :  && mkdir -p /etc/nginx/sites-enabled && mkdir -p /etc/nginx/default-site-conf'
RUN /bin/bash -c 'rm -r /nginx-1.21.6 || : && rm -r /nginx-rtmp-module || : && rm -r /ngx-fancyindex || : && rm -r /nginx-1.21.6.tar.gz || : '

COPY nginx-conf/nginx.conf /etc/nginx/nginx.conf
COPY nginx-conf/main_server /etc/nginx/default-site-conf/main_server
COPY nginx-conf/ffdhe2048.txt /etc/nginx/ffdhe2048.txt
COPY nginx-conf/selfsigned.crt /etc/nginx/certs/certificate.crt
COPY nginx-conf/selfsigned.key /etc/nginx/certs/certificate.key

RUN mkdir -p /etc/service/nginx
COPY run-nginx.sh /etc/service/nginx/run
RUN chmod +x /etc/service/nginx/run
# RUN adduser --system --no-create-home --shell /bin/false --group --disabled-login www-data && chmod +x /etc/service/nginx/run

RUN mkdir -p /etc/my_init.d
COPY setup_nginx.sh /etc/my_init.d/setup_nginx.sh
RUN chmod +x /etc/my_init.d/setup_nginx.sh

RUN apt-get update && /sbin/install_clean python3 python3-pip

RUN mkdir -p /etc/pyserver
COPY python-src/* /etc/pyserver/

RUN mkdir -p /etc/service/pyserver
COPY run-py.sh /etc/service/pyserver/run
RUN chmod +x /etc/service/pyserver/run

RUN /bin/bash -c 'rm -r /etc/nginx/html || : && mkdir -p /etc/nginx/html'
COPY demo-sveltekit-src/build /etc/nginx/html

# Clean up APT when done.
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*