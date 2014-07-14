import docker

def get_router_virtual_host(detailList):
	env = detailList["Config"]["Env"]
	router_virtual_host = None
	for env_param in env:
		sp = env_param.split('=')
		if sp[0] == 'ROUTER_VIRTUAL_HOST':
			router_virtual_host = sp[1]
	
	return router_virtual_host

def get_router_virtual_port(detailList):
	env = detailList["Config"]["Env"]
	router_virtual_host = None
	for env_param in env:
		sp = env_param.split('=')
		if sp[0] == 'ROUTER_VIRTUAL_PORT':
			router_virtual_port = sp[1]
	
	return router_virtual_port


def get_router_virtual_cert(detailList):
	env = detailList["Config"]["Env"]
	router_virtual_host = None
	for env_param in env:
		sp = env_param.split('=')
		if sp[0] == 'ROUTER_VIRTUAL_CERT':
			router_virtual_cert = sp[1]
	
	return router_virtual_cert


def get_ip_address(detailList):
	return detailList["NetworkSettings"]["IPAddress"]

def main():
	c = docker.Client(base_url='unix://var/run/docker.sock',
			  version='1.12',
			  timeout=10)

	containerList = c.containers(quiet=False, all=False, trunc=True, latest=False, since=None,
		     before=None, limit=-1)


	for container in containerList:
		detailList = c.inspect_container(container["Id"])
		print "IP: %s, router_virtual_host: %s" % ( get_ip_address(detailList), get_router_virtual_host(detailList) )
		
		if get_router_virtual_host(detailList) == None:
			print "TIS EEN NON"

	

if __name__ == "__main__":
	main()

	print """DIT IS EEN CONFIG FILE
	MET INHOUD %(IPAddress)s
	EN MEER HOSTS %(HostAddress)s""" % ( {  "HostAddress": "HOSTJES", "IPAddress": "123.123.123" } )
	
