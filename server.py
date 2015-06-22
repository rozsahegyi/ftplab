import sys, os, time, logging, threading
from functools import partial

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer, ThreadedFTPServer


class CustomFTP(FTPHandler):
	def __init__(self, auth, number, path, password):
		self.authorizer = auth
		self.number = number
		self.path = path

	def __call__(self, *args, **kw):
		instance = FTPHandler(*args, **kw)
		instance.authorizer = self.authorizer
		instance.log_prefix = 'server #%d %%(username)s@%%(remote_ip)s' % self.number
		instance.logfile = os.path.join(self.path, '%d.log' % self.number)
		instance.log = partial(self.log.im_func, instance)
		return instance

	def log(self, msg, logfun=logging.info):
		with open(self.logfile, 'a') as f: f.write('%s | %-15s | %s\n' % (time.strftime('%y%m%d %X'), self.username or '--', msg))

class Server(threading.Thread):
	def __init__(self, ip, path, users, port, password):
		super(Server, self).__init__()
		self.ip = ip
		self.path = path
		self.users = users
		self.port = port
		self.auth = DummyAuthorizer()
		self.handler = CustomFTP(self.auth, self.port, path, password)
		# self.handler.authorizer = self.auth
		print 'starting server on port %d' % (self.port)
		[self.add_user(self.path, u, password) for u in self.users]

	def start_thread(self):
		self.start()
		return self

	def add_user(self, path, user, password):
		pathn = os.path.join(path, str(self.port))
		if not os.path.exists(pathn): os.mkdir(pathn)
		self.auth.add_user(user, password, pathn, perm="elr") # elradfmw

	def run(self):
		self.server = ThreadedFTPServer((self.ip, self.port), self.handler)
		self.server.serve_forever()
