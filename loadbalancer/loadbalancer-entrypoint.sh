#!/bin/bash
set -e
echo "upstream website {"                     >> /etc/nginx/sites-available/default
echo "  server "$IP":81;"                     >> /etc/nginx/sites-available/default
echo "  server "$IP":82;"                     >> /etc/nginx/sites-available/default
echo "  server "$IP":83;"                     >> /etc/nginx/sites-available/default
echo "}"                                      >> /etc/nginx/sites-available/default
echo "server {"                               >> /etc/nginx/sites-available/default
echo "  listen 80;"                           >> /etc/nginx/sites-available/default
echo '  add_header Cache-Control "no-store";' >> /etc/nginx/sites-available/default
echo "  location / {"                         >> /etc/nginx/sites-available/default
echo "    proxy_pass http://website;"         >> /etc/nginx/sites-available/default
echo "    proxy_set_header Host \$host;"      >> /etc/nginx/sites-available/default
echo "  }"                                    >> /etc/nginx/sites-available/default
echo "}"                                      >> /etc/nginx/sites-available/default
exec "$@"
