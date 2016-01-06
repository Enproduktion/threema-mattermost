server {
    listen              443 ssl;
    server_name         example.com; # enter (sub)domain for the service
    ssl_certificate     /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

    # ATTENTION: Following protocols and ciphers are not optimal
    # They are taken from nginx' examples and should be updated
    # to the best current options. Ask your local administrator
    # what they are.
    ssl_protocols       TLSv1 TLSv1.1 TLSv1.2;
    ssl_ciphers         HIGH:!aNULL:!MD5;

    location / {
        include uwsgi_params;
        uwsgi_pass unix:/var/run/threema-mattermost.sock;
    }
}
