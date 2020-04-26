In this project Terraform is gonna generate ssh key, create security group and instance. Python script using paramiko module is going to run some commands to configure instance for example download mariadb-server and docker.io . Also it's going to transport files such as dockerfiles and entrypoints from instance which is running this script to remote instance. After that it will create 2 images one is handmade wordpress image and second one is also handmade nginx loadbalancer image. Then it's going to create 3 containers based on wordpress image and 1 loadbalancer. In between it's going to run database.py script on remote host which is creating databases for each wordpress container (so u can see that loadbalancer is working properly) and users with ip's of containers which were passed here using arguments and giving them all privileges. 

To run the script you need to create aws user with secret key, have terraform and python, install paramiko module and own a user that can run terraform.

Command to run the script: python setup.py << AWS_ACCESS_KEY_ID >> << AWS_SECRET_ACCESS_KEY >> << AWS_DEFAULT_REGION >>

Script is going to print out every output and also containers id's so you know they actually running.
