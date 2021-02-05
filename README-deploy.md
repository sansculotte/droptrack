
create 'deploy' user on remote system

copy deploy/inventory.dist to deploy/inventory

ansible-playbook deploy/playbook.yml

ansible-playbook -i deploy/inventory deploy/playbook.yml
