import sys
sys.path.append('../encryption/')
import SlightlyAdvancedECC as SAECC
import socket

class Server:
	def __init__(self, a = 2, b = 31, q = 571):
		self.secret = 15
		self.shared_base = 5
		self.shared_prime = 23
		self._isRunning = False;
		self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.serversocket.bind(('localhost', 8089))
		self.serversocket.listen(5)
		self.known_clients = []
		pass

	def start(self):
		self._isRunning = True

		while(self._isRunning):
			connection, address = self.serversocket.accept()
			print(address[0])
			if(address[0] not in self.known_clients):
				self.known_clients.append(address[0])
			else:
				print("Hello again {}".format(address[0]))
			buf = connection.recv(64)
			if len(buf) > 0:
				print(buf)
				if(buf.decode() == "/end_server"):
					print("Terminating the server")
					self._isRunning = False
		pass

	def defineCurve(self, a, b, q):
		self.ec = SAECC.EllipticCurve(a, b, q)
		pass





