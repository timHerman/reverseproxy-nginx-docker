#!/usr/bin/env python

import docker, os, logging, logging.handlers

LOG_FILENAME = 'generater.log'
logger = logging.getLogger('generator')
logger.setLevel(logging.DEBUG)

handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=1048576, backupCount=5)
logger.addHandler(handler)

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

def removeOldFiles(dir, generatedFileNames):
	for (_, __, files) in os.walk(dir):
		for file in files:
			if file.startswith('generated.'):
				fullPathFile = 'output/%s' % file
				if not fullPathFile in generatedFileNames:
					logger.debug('Removing old file %s' % fullPathFile)
					os.remove(fullPathFile)

def writeFile(filePath, output):
	outputFile = open(filePath, 'w+')
	outputFile.write(output)
	outputFile.close()
	logger.debug('Add new file %s' % filePath)

def generateTemplate(templateFile, filePath, host_name, host_ip, host_cert, host_port):
	# Load template and fill with data
	templateFile = open(templateFile,'r')
	output = templateFile.read() % ( { "hostname": host_name, "ipaddress": host_ip, "cert": host_cert, "port": host_port    } )

	# Check if file exists, if there are no changes, do nothing (We want to detect changes later on to reload nginx)
	if os.path.isfile(filePath):
		existingFile = open(filePath, 'r')
		fileContent = existingFile.read()
		if fileContent != output:
			writeFile(filePath, output)
	else:
		writeFile(filePath, output)


def main():
	c = docker.Client(base_url='unix://var/run/docker.sock',
			  version='1.12',
			  timeout=10)

	containerList = c.containers(quiet=False, all=False, trunc=True, latest=False, since=None,
		     before=None, limit=-1)

	generatedFileNames = []

	for container in containerList:
		detailList = c.inspect_container(container["Id"])

		host_ip = get_ip_address(detailList)
		host_name = get_router_virtual_host(detailList)
		host_cert = get_router_virtual_cert(detailList)
		host_port = get_router_virtual_port(detailList)

		logger.debug('Handling container IP %s & VHost %s' % ( host_ip, host_name ))

		if host_name and host_name.startswith('www.'):
			host_name = host_name[4:]

		# Check if the mimimum is set
		if host_ip and host_name:
			filePath = 'output/generated.%s.conf' % host_name
			generateTemplate('template/nginx.conf.tpl', filePath, host_name, host_ip, host_cert, host_port)
			generatedFileNames.append(filePath)

			filePath = 'output/generated.redirect.%s.conf' % host_name
			generateTemplate('template/redirect.nginx.conf.tpl', filePath, host_name, host_ip, host_cert, host_port)
			generatedFileNames.append(filePath)

	removeOldFiles('output', generatedFileNames)
			

if __name__ == "__main__":
	main()

"""

SCRAPZONE

"""
