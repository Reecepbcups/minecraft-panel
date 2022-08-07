```
pacman -S nginx

systemctl enable nginx
systemctl start nginx

nano /etc/nginx/sites-enabled/default
 # add: ( you caan also do in main nginx.conf file)

server {
    listen 80;
    server_name api.crafteconomy.io;
    location / {
        proxy_set_header Host $host;
        proxy_pass http://127.0.0.1:4000;
        proxy_redirect off;
    }
}
```