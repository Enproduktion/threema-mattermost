==================
Threema-Mattermost
==================

threema-mattermost is a threema webhook server for mattermost. It takes all messages
to a given threema-gateway-id and posts it in the associated mattermost channel.

Known Issues
------------
+ Multi group support missing
+ No image decryption support


Requirements
------------

Threema-Mattermost depends heavily on threema-msgapi-sdk-python. To use group messages,
you'll need the currently pending patches by Enproduktion. As long as those patches
are pending, we recommend installing threema-msgapi-sdk-python by running:

.. code:: bash

    pip install git+https://github.com/Enproduktion/threema-msgapi-sdk-python.git

To see all other requirements, please lookup the Requirements file in the
repository root.

Automated Install
-----------------
Not there yet.

Manual Install on RHEL/Centos 7.x
---------------------------------

Following are the necessary installation steps for RHEL / Centos 7.x (we just pretend you are root and
omit sudo).

Install python and core dependencies:

.. code:: bash

    yum install epel-release
    yum install python-pip python34 python-virtualenv python-pip python34-devel libsodium git

    # Keep in mind not to have Development Tools installed on production hardware.
    # We recommend downloading all pip tools on a dev computer and install the
    # offline binaries on production hardware.
    yum groupinstall "Development Tools"

    pip install --upgrade pip
    pip install --upgrade virtualenv # There is a bug that makes this step necessary

Create user and virtualenv:

.. code:: bash

    useradd threema-mattermost
    su threema-mattermost
    virtualenv -p python3.4 ~/VirtualEnv/threema-mattermost

Clone repository and install dependencies:

.. code:: bash

    cd ~
    git clone https://github.com/Enproduktion/threema-mattermost.git
    cd threema-mattermost
    source ~/VirtualEnv/threema-mattermost/bin/activate
    pip install -r Requirements

Install and setup letsencrypt:

.. code:: bash

    # see letencrypt.com
    mkdir /root/letsencrypt
    git clone https://github.com/letsencrypt/letsencrypt /root/letsencrypt/.
    cd /root/letsencrypt
    ./letsencrypt-auto certonly --standalone -d example.com

Install and setup nginx:

.. code:: bash

    exit
    yum install nginx

    cp /home/threema-mattermost/threema-mattermost/install/nginx/example.com /etc/nginx/conf.d
    vi /etc/nginx/conf.d/example.com
    mv /etc/nginx/conf.d/example.com /etc/nginx/conf.d/mysub.domain.tld

Install the uwsgi service:

.. code:: bash

    # You could also use the uwsgi Emporer Daemon. Bare in mind that it's
    # running in Tyrant in default on RHEL systems. It therefore falls back
    # to uwsgi:uwsgi always.
    # See /usr/lib/systemd/system/uwsgi.service and Emperor uwsgi docs.

    yum install uwsgi uwsgi-plugin-python3

Install the systemd unit file (start script):

.. code:: bash

    cp /home/threema-mattermost/threema-mattermost/install/threema-mattermost.service /etc/systemd/system/

Configure it to your needs:

.. code:: bash

    vi /home/threema-mattermost/threema-mattermost/threema_mm/settings.py
    vi /home/threema-mattermost/threema-mattermost/threema_mm/data/users.py

(Optional) Restrict access on firewall level:

.. code:: bash

    yum install firewalld
    firewall-cmd --permanent --zone=public --add-service=ssh
    # firewall-cmd  --permanent --zone=public --remove-service=https
    firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="5.148.175.192/27" service name="https" log prefix="https" level="info" accept'
    firewall-cmd --reload

Run Threema-Mattermost:

.. code:: bash

    systemctl start threema-mattermost
    #systemctl stop threema-mattermost
    #systemctl status threema-mattermost
