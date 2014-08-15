server {
    listen 80;
    server_name %(hostname)s;
    rewrite     ^   https://$server_name$request_uri? permanent;
}

server {
	listen 443 ssl;
	ssl_certificate %(ssl_pem)s;
	ssl_certificate_key %(ssl_key)s;

	server_name %(hostname)s;

	location / {
		proxy_set_header Host $host;
		proxy_set_header X-Real-IP $remote_addr;
		proxy_pass http://%(ipaddress)s;
		proxy_buffering off;
	}
}
