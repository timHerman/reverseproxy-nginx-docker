import docker, os, glob

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
	router_virtual_port = None
	for env_param in env:
		sp = env_param.split('=')
		if sp[0] == 'ROUTER_VIRTUAL_PORT':
			router_virtual_port = sp[1]
	
	return router_virtual_port


def get_router_virtual_cert(detailList):
	env = detailList["Config"]["Env"]
	router_virtual_cert = None
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

	generatedFileNames = []

	for container in containerList:
		detailList = c.inspect_container(container["Id"])
		print "IP: %s, router_virtual_host: %s" % ( get_ip_address(detailList), get_router_virtual_host(detailList) )

		host_ip = get_ip_address(detailList)
		host_name = get_router_virtual_host(detailList)
		host_cert = get_router_virtual_cert(detailList)
		host_port = get_router_virtual_port(detailList)

		# Check if the mimimum is set
		if host_ip and host_name:
			# Load template and fill with data
			templateFile = open('template/nginx.conf.tpl','r')
			output = templateFile.read() % ( { "hostname": host_name, "ipaddress": host_ip, "cert": host_cert, "port": host_port    } )
			
			# Generate filename
			filePath = 'output/generated.%(filename)s.conf' % ( { "filename": host_name } )
			generatedFileNames.append(filePath)
			# Check if file exists, if there are no changes, do nothing (We want to detect changes later on to reload nginx)
			if os.path.isfile(filePath):
				existingFile = open(filePath, 'r')
				fileContent = existingFile.read()
				if fileContent != output:
					writeFile(filePath, output)
			else:
				writeFile(filePath, output)

	removeOldFiles('output', generatedFileNames)

def removeOldFiles(dir, generatedFileNames):
	for (_, __, files) in os.walk(dir):
		for file in files:
			if file.startswith('generated.'):
				fullPathFile = 'output/%s' % file
				if not fullPathFile in generatedFileNames:
					print "Removing old file %s" % fullPathFile
					os.remove(fullPathFile)

def writeFile(filePath, output):
	outputFile = open(filePath, 'w+')
	outputFile.write(output)
	outputFile.close()

if __name__ == "__main__":
	main()
