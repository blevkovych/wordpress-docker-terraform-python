#!/bin/bash
set -e
echo "upstream website {"                                             >> /etc/nginx/sites-available/default
echo "  server "$IP":81;"                                             >> /etc/nginx/sites-available/default
echo "  server "$IP":82;"                                             >> /etc/nginx/sites-available/default
echo "  server "$IP":83;"                                             >> /etc/nginx/sites-available/default
echo "}"                                                              >> /etc/nginx/sites-available/default
echo "server {"                                                       >> /etc/nginx/sites-available/default
echo "  listen 80;"                                                   >> /etc/nginx/sites-available/default
echo "  location / {"                                                 >> /etc/nginx/sites-available/default
echo '  proxy_set_header Host $http_host;'                            >> /etc/nginx/sites-available/default
echo '  proxy_set_header X-Real-IP $remote_addr;'                     >> /etc/nginx/sites-available/default
echo '  proxy_set_header X-Scheme $scheme;'                           >> /etc/nginx/sites-available/default
echo '  proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;' >> /etc/nginx/sites-available/default
echo '  proxy_set_header X-Forwarded-Proto $scheme;'                  >> /etc/nginx/sites-available/default
echo '  proxy_redirect    off;'                                       >> /etc/nginx/sites-available/default
echo '  add_header Pragma "no-cache";'                                >> /etc/nginx/sites-available/default
echo '  add_header Cache-Control "no-cache";'                         >> /etc/nginx/sites-available/default
echo "  proxy_pass http://website;"                                   >> /etc/nginx/sites-available/default
echo "  sub_filter 'action=\"/'  'action=\"/';"                       >> /etc/nginx/sites-available/default
echo "  sub_filter 'href=\"/'  'href=\"/';"                           >> /etc/nginx/sites-available/default
echo "  sub_filter 'src=\"/'  'src=\"/'"                              >> /etc/nginx/sites-available/default
echo "  sub_filter_once off;"                                         >> /etc/nginx/sites-available/default
echo "  }"                                                            >> /etc/nginx/sites-available/default
echo "}"                                                              >> /etc/nginx/sites-available/default
exec "$@"
