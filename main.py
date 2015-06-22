import os, server, logging, time
from config import path, ip, password, users, servers

def run_servers(path, users, servers):
	if isinstance(servers, dict): servers = servers.keys()
	return [server.Server(ip, path, users, port, password).start_thread() for port in servers if port and isinstance(port, int)]

path = os.path.realpath(path)
if not os.path.exists(path): os.makedirs(path)

logfile = os.path.join(path, 'ftp.log')
logging.basicConfig(format='[%(asctime)s] %(message)s', filename=logfile, level=logging.INFO)

print 'ftp directories and logs under %s' % path
servers = run_servers(path, users, servers)

try:
	while 1: time.sleep(1)
except:
	pass

print 'stopping servers...'
[s.server.close_all() for s in servers]

