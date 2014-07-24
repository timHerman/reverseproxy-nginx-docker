server {
	#ssl_certificate /etc/nginx/certs/demo.pem;
	#ssl_certificate_key /etc/nginx/certs/demo.key;

	server_name %(hostname)s;

	location / {
		proxy_set_header Host $host;
		proxy_set_header X-Real-IP $remote_addr;
		proxy_pass http://%(ipaddress)s;
		proxy_buffering off;
	}
}
