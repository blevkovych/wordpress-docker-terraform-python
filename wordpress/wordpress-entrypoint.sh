#!/bin/bash
set -e
echo "<?php"                                                        >> /var/www/html/wp-config.php
echo "define(' WP_SITEURL', 'http://' . \$_SERVER['HTTP_HOST']);"   >> /var/www/html/wp-config.php
echo "define(' WP_HOME', 'http://' . \$_SERVER['HTTP_HOST']);"      >> /var/www/html/wp-config.php
echo "define( 'DB_NAME', '"$DB_NAME"' );"                           >> /var/www/html/wp-config.php
echo "define( 'DB_USER', '"$DB_USER"' );"                           >> /var/www/html/wp-config.php
echo "define( 'DB_PASSWORD', '"$DB_PASSWORD"' );"                   >> /var/www/html/wp-config.php
echo "define( 'DB_HOST', '"$DB_HOST"' );"                           >> /var/www/html/wp-config.php
echo "define( 'DB_CHARSET', 'utf8' );"                              >> /var/www/html/wp-config.php
echo "define( 'DB_COLLATE', '' );"                                  >> /var/www/html/wp-config.php
echo "define( 'AUTH_KEY',         'put your unique phrase here' );" >> /var/www/html/wp-config.php
echo "define( 'SECURE_AUTH_KEY',  'put your unique phrase here' );" >> /var/www/html/wp-config.php
echo "define( 'LOGGED_IN_KEY',    'put your unique phrase here' );" >> /var/www/html/wp-config.php
echo "define( 'NONCE_KEY',        'put your unique phrase here' );" >> /var/www/html/wp-config.php
echo "define( 'AUTH_SALT',        'put your unique phrase here' );" >> /var/www/html/wp-config.php
echo "define( 'SECURE_AUTH_SALT', 'put your unique phrase here' );" >> /var/www/html/wp-config.php
echo "define( 'LOGGED_IN_SALT',   'put your unique phrase here' );" >> /var/www/html/wp-config.php
echo "define( 'NONCE_SALT',       'put your unique phrase here' );" >> /var/www/html/wp-config.php
echo "\$table_prefix = 'wp_';"                                      >> /var/www/html/wp-config.php
echo "define( 'WP_DEBUG', false );"                                 >> /var/www/html/wp-config.php
echo "if ( ! defined( 'ABSPATH' ) ) {"                              >> /var/www/html/wp-config.php
echo "	define( 'ABSPATH', dirname( __FILE__ ) . '/' );"            >> /var/www/html/wp-config.php
echo "}"                                                            >> /var/www/html/wp-config.php
echo "require_once( ABSPATH . 'wp-settings.php' );"                 >> /var/www/html/wp-config.php

exec "$@"
