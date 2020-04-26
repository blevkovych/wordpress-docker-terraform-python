FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive \
	DB_NAME=name \
	DB_USER=user \
	DB_PASSWORD=pass \
	DB_HOST=127.0.0.1

RUN apt-get update && apt-get install -yq --no-install-recommends \
    apt-utils \
    apache2 \
    php7.2 \
    php7.2-mysql \
    wget \
    tar \
    mariadb-client \
    ca-certificates

RUN rm /var/www/html/index.html
RUN cd /tmp
RUN wget http://wordpress.org/latest.tar.gz
RUN tar -xvf latest.tar.gz --strip-components=1 -C /var/www/html/
RUN rm latest.tar.gz
RUN chown -R www-data:www-data /var/www/html/
RUN touch /var/www/html/wp-config.php
RUN chmod 755 /var/www/html

COPY wordpress-entrypoint.sh /usr/local/bin
RUN chmod 777 /usr/local/bin/wordpress-entrypoint.sh
ENTRYPOINT ["/usr/local/bin/wordpress-entrypoint.sh"]

EXPOSE 80

CMD /usr/sbin/apache2ctl -D FOREGROUND 
