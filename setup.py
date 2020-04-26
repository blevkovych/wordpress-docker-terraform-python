import os, sys, paramiko, time
def AWS():
    KeyID = sys.argv[1]
    SecretKey = sys.argv[2]
    Region = sys.argv[3]
    credentials = ('export AWS_ACCESS_KEY_ID='+KeyID+' && export AWS_SECRET_ACCESS_KEY='+SecretKey+
    ' && export AWS_DEFAULT_REGION='+Region)
    return credentials

def ssh_key():
    if os.path.isfile('sshkey'):
        print('\n'"sshkey already exists no need to create new one")
    else:
        os.system("ssh-keygen -f sshkey -q -N ''")

def Terraform():
    ssh_key()
    credentials = AWS()
    os.system(credentials + ' && cd terraform && terraform init && terraform apply -auto-approve')

def ConfiguringInstance():
    time.sleep(60)
    publicip = open("terraform/docker_public_ip", "r").read()
    publicip = publicip.rstrip('\n')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=publicip, username='ubuntu', key_filename='sshkey')

    stdin, stdout, stderr = client.exec_command('sudo apt-get update')
    print(stdout.read().decode('utf-8'))
    stdin, stdout, stderr = client.exec_command('sudo apt-get install software-properties-common -y')
    print(stdout.read().decode('utf-8'))
    stdin, stdout, stderr = client.exec_command('sudo apt-get update')
    print(stdout.read().decode('utf-8'))
    stdin, stdout, stderr = client.exec_command('sudo apt-get install docker.io mariadb-client mariadb-server -y')
    print(stdout.read().decode('utf-8'))
    stdin, stdout, stderr = client.exec_command('sudo apt-get install python python-pip -y')
    print(stdout.read().decode('utf-8'))
    stdin, stdout, stderr = client.exec_command('pip install mysql-connector-python')
    print(stdout.read().decode('utf-8'))
    stdin, stdout, stderr = client.exec_command('sudo mkdir ~/wordpress ~/loadbalancer')
    stdin, stdout, stderr = client.exec_command('sudo chmod 777 ~/wordpress ~/loadbalancer')
    stdin, stdout, stderr = client.exec_command('sudo chmod 777 /etc/mysql/mariadb.conf.d/50-server.cnf')

    ftp_client = client.open_sftp()
    ftp_client.put("wordpress/Dockerfile", "wordpress/Dockerfile")
    ftp_client.put("wordpress/wordpress-entrypoint.sh", "wordpress/wordpress-entrypoint.sh")
    ftp_client.put("loadbalancer/Dockerfile", "loadbalancer/Dockerfile")
    ftp_client.put("loadbalancer/loadbalancer-entrypoint.sh", "loadbalancer/loadbalancer-entrypoint.sh")
    ftp_client.get("/etc/mysql/mariadb.conf.d/50-server.cnf", "mariadb.conf")
    conf = open("mariadb.conf", "r")
    list_of_lines = conf.readlines()
    list_of_lines[28] = "#bind-address            = 127.0.0.1\n"
    conf = open("mariadb.conf", "w")
    conf.writelines(list_of_lines)
    conf.close()
    ftp_client.put("mariadb.conf", "/etc/mysql/mariadb.conf.d/50-server.cnf")
    ftp_client.put("database.py", "database.py")
    ftp_client.close()

    os.system('sudo rm mariadb.conf')
    stdin, stdout, stderr = client.exec_command('sudo chmod 0444 /etc/mysql/mariadb.conf.d/50-server.cnf')
    stdin, stdout, stderr = client.exec_command('sudo systemctl restart mariadb')
    print(stdout.read().decode('utf-8'))

    client.close()

def Docker():
    publicip = open("terraform/docker_public_ip", "r").read()
    publicip = publicip.rstrip('\n')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=publicip, username='ubuntu', key_filename='sshkey')

    stdin, stdout, stderr = client.exec_command('ifconfig eth0 | grep -Eo "inet (addr:)?([0-9]*\.){3}[0-9]*" | grep -Eo "([0-9]*\.){3}[0-9]*" | grep -v "127.0.0.1"')
    privateip = stdout.read().decode('utf-8')
    privateip = privateip.rstrip('\n')
    stdin, stdout, stderr = client.exec_command('sudo docker build -t wordpress ~/wordpress')
    print(stdout.read().decode('utf-8'))
    stdin, stdout, stderr = client.exec_command('sudo docker build -t loadbalancer ~/loadbalancer')
    print(stdout.read().decode('utf-8'))
    for num in range(1, 4):
        stdin, stdout, stderr = client.exec_command(
            'sudo docker run -e DB_NAME=wordpress'+str(num)+' -e DB_PASSWORD=pass -e DB_USER=wpuser -e DB_HOST="$LC_WPIP" --name wordpress'+str(num)+' -d -p 8'+str(num)+':80 wordpress', environment={"LC_WPIP": privateip})
        print(stdout.read().decode('utf-8'))
        stdin, stdout, stderr = client.exec_command('sudo docker inspect wordpress'+str(num)+' --format "{{ .NetworkSettings.IPAddress }}"')
        containerip = stdout.read().decode('utf-8')
        containerip = containerip.rstrip('\n')
        stdin, stdout, stderr = client.exec_command('cd ~ && sudo python database.py wordpress'+str(num)+' '+containerip)
    stdin, stdout, stderr = client.exec_command('sudo docker run -e IP="$LC_LBIP" --name loadbalancer -d -p 80:80 loadbalancer', environment={"LC_LBIP": publicip})
    print(stdout.read().decode('utf-8'))

    client.close()
Terraform()
ConfiguringInstance()
Docker()
