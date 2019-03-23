git clone https://github.com/cosmocat27/searchtool.git
sudo apt install python-pip
sudo apt-get install pip
curl -O https://bootstrap.pypa.io/get-pip.py
sudo apt-get install python3-distutils
python3 get-pip.py --user
export PATH=~/.local/bin:$PATH
source ~/.bashrc
pip install virtualenv --user
python virtualenv
activate
cd searchtool/
pip install -r requirements.txt 
sudo apt install sqlite3
sudo apt-get install openjdk-8-jre
echo export JAVA_HOME=\"$(readlink -f $(which java) | grep -oP '.*(?=/bin)')\" >> ~/.bashrc
source .bashrc
wget -qO - https://packages.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
echo "deb https://packages.elastic.co/elasticsearch/2.x/debian stable main" | sudo tee -a /etc/apt/sources.list.d/elasticsearch-2.x.list
sudo apt-get update
sudo apt-cache search elastic
sudo apt-get install elasticsearch
sudo /bin/systemctl daemon-reload
sudo /bin/systemctl enable elasticsearch.service
sudo /bin/systemctl start elasticsearch.service
pip install elasticsearch
pip install flask --user
python setup.py .
pip install -e . --user
export FLASK_APP=searchapp
sudo apt-get install kibana

sudo service elasticsearch restart
sudo service kibana restart
sudo service nginx restart
gunicorn --workers 3 --bind 0.0.0.0:8000 searchapp &

# ok, this is too confusing ><
# basically, make sure elasticsearch and kibana are upgraded
# then edit the kibana.yml file to root it at /search

# nginx file:

# server {
#    listen 80;
#    server_name server_domain_or_IP;
#
#    location / {
#        include proxy_params;
#        proxy_pass http://localhost:8000;
#
#    location /search/ {
#        include proxy_params;
#        proxy_pass http://localhost:5601;

# kibana.yml file:

# server.host: 0.0.0.0
# server.basePath: "/search"
# server.rewriteBasePath: true

