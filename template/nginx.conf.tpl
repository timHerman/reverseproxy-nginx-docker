server {
	#ssl_certificate /etc/nginx/certs/demo.pem;
	#ssl_certificate_key /etc/nginx/certs/demo.key;

	server_name %(hostname)s;

	location / {
	    proxy_pass http://%(ipaddress)s;
	}
}
