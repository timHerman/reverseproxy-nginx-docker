server {
	client_max_body_size 1G;
	server_name %(hostname)s;

	location / {
		proxy_set_header Host $host;
		proxy_set_header X-Real-IP $remote_addr;
		proxy_pass http://%(ipaddress)s;
		proxy_buffering off;
	}
}
