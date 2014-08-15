server {
    listen 80;
    server_name %(hostname)s;
    rewrite     ^   https://$server_name$request_uri? permanent;
}

server {
	keepalive_timeout 70;
	listen 443 ssl;

	ssl on;
	ssl_certificate %(sslcert)s;
	ssl_certificate_key %(sslkey)s;

	server_name %(hostname)s;

	location / {
		proxy_set_header Host $host;
		proxy_set_header X-Real-IP $remote_addr;
		proxy_pass http://%(ipaddress)s;
		proxy_buffering off;
	}
}
