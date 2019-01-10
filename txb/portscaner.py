#coding=UTF-8
import socket,re,sys

def check_server(address,port):
	s = socket.socket()
	print ('尝试链接 %s 端口 %s' %(address,port))

	try:
		s.connect((address,port))
		print ('端口开放')
		return (True)

	except socket.error as e:
		print ('端口不开放')
		return (False)

if __name__ == '__main__':
	
	from optparse import OptionParser
	parser = OptionParser()
	parser.add_option('-a','--address',dest = 'address',default = 'localhost',help = '服务器的IP地址',metavar = 'ADDRESS')
	parser.add_option('-p' , '--port' ,type = 'int' , default = 80 , help = '服务器的端口' , metavar = 'PORT')
	(options,args) = parser.parse_args()
	print ('选项 %s ,args %s'%(options,args))
	print (options.address,options.port)
	check = check_server(options.address,options.port)
	print ('端口有%s'%check)
	sys.exit(not check)