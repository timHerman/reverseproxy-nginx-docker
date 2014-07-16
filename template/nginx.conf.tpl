server {
	#ssl_certificate /etc/nginx/certs/demo.pem;
	#ssl_certificate_key /etc/nginx/certs/demo.key;

	server_name www.%(hostname)s;

	location / {
		proxy_set_header Host $host;
		proxy_set_header X-Real-IP $remote_addr;
		proxy_pass http://%(ipaddress)s;
		#proxy_buffers 16 4k;
		#proxy_buffer_size 2k;
		proxy_buffering off;
		proxy_pass http://localhost:8000;
	}
}
