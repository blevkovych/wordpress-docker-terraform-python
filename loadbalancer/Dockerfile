FROM ubuntu:18.04

ENV IP=127.0.0.1

RUN apt-get update && apt-get install -yq --no-install-recommends \
    apt-utils \
    nginx

RUN rm /etc/nginx/sites-available/default
RUN touch /etc/nginx/sites-available/default
RUN chmod 755 /etc/nginx/sites-available/default

EXPOSE 80

COPY loadbalancer-entrypoint.sh /usr/local/bin
RUN chmod 755 /usr/local/bin/loadbalancer-entrypoint.sh
ENTRYPOINT ["/usr/local/bin/loadbalancer-entrypoint.sh"]

CMD ["nginx", "-g", "daemon off;"]
