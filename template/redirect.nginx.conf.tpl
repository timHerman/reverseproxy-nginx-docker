server {
	server_name  %(hostname)s;
	rewrite ^(.*) http://www.%(hostname)s$1 permanent;
}
