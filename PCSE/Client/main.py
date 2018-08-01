import sys
sys.path.append('../encryption/')
from client import Client
import SlightlyAdvancedECC as SAECC

c = Client()
c.startConnection()
c.sendMessage("hello world")
c.sendMessage()

#Start point can be public (only determined by one [server])
#End point is public
#Curve is public
#Private key is all that needs to be agreed on


# Define the curve
# Get coordinate at one of the valid points
# Verify that the point is under the correct order (max of q)
# ElGamal encoding/decoding usage
# Mapping value to elliptic_curve point

# Do DH to determine private key
# The private key
# Use private key to generate public ec-eg key

# Split the message into its individual characters
# Convert each letter to its ordinal value and get the coordinate at that index in the map
# Encrypt each of the coordinates
# Decrypt the encrypted coordinates



# Needed for encryption:
	#-data, public key, r : random int < ec.q
		#returns cipher

# needed for decryption:
	#-cipher, private key
		#returns data



