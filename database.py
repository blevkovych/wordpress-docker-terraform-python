import sys, mysql.connector as mariadb
database = sys.argv[1]
containerip = sys.argv[2]
client = mariadb.connect(host="localhost", user="root", passwd="", unix_socket="/var/run/mysqld/mysqld.sock")
cursor = client.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS "+database+";")
cursor.execute("CREATE USER IF NOT EXISTS 'wpuser'@'"+containerip+"' IDENTIFIED BY 'pass';")
cursor.execute("GRANT ALL ON "+database+".* TO 'wpuser'@'"+containerip+"' IDENTIFIED BY 'pass';")
cursor.execute("FLUSH PRIVILEGES;")
