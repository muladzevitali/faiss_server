# Configuring Gunicorn:
```bash
sudo nano /etc/systemd/system/my_project.service
```

```text
[Unit]
Description=Gunicorn instance to serve my_project project
After=network.target

[Service]
User=root
Group=nginx
WorkingDirectory=/root/my_project
Environment="PATH=/root/anaconda3/bin"
ExecStart=/root/anaconda3/bin/gunicorn --workers 3 --bind unix:my_project.sock -m 007 wsgi:application

[Install]
WantedBy=multi-user.target
```


```bash
systemctl start my_project
systemctl enable my_project
systemctl status my_project
```

# Configuring Nginx

```bash
sudo nano /etc/nginx/nginx.conf
```

```text
server {
    listen 80;

    server_name my_project.bog.ge www.my_project.bog.ge;
    client_max_body_size 100M;
    proxy_max_temp_file_size 0;
    proxy_buffering off;
        location / {
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_pass http://unix://root/my_project/my_project.sock; 
        }
    }
```


```bash
sudo ln -s /etc/nginx/sites-available/my_project /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
