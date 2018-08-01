import sys
sys.path.append('../encryption/')
import SlightlyAdvancedECC as SAECC
import socket

class Client:
	# (571) Chosen because it is prime, and results in more than 255 valid coordinates
	def __init__(self, a = 2, b = 31, q = 571, start_point = 3):
		self.secret = 6
		self.shared_base = 5
		self.shared_prime = 23
		self.server_ip = 'localhost'
		self.port_number = 8089
		self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.ec = self.defineCurve(a, b, q)
		self.eg = self.defineEG(x = 12)

	def startConnection(self):
		self.clientsocket.connect(('localhost', 8089))

	def sendMessage(self, message = '/end_server'):
		self.clientsocket.send(str.encode(message))

	def defineCurve(self, a, b, q):
		return SAECC.EllipticCurve(a, b, q)

	def defineEG(self, x):
		# Get coordinate at one of the valid points
		g, _ = self.ec.at(x)
		# Verify that the point is under the correct order (max of q)
		assert self.ec.order(g) <= self.ec.q

    	# ElGamal encoding/decoding usage
		return SAECC.ElGamal(self.ec, g)

