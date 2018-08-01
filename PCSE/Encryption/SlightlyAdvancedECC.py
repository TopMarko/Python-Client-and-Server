# An ECC curve (E) is a curve given by y^2 = x^3 + ax + b
# If we have a point P1 = (x1,y1)
# and we want to find P2(x2,y2) such that
# P2 = 2(P1) This is known as point doubling
# It is done as:
#   Let lambda = x1 + (y1/x1)
#   then    x2 = a + lambda + lambda^2
#   and     y2 = (x1+x2)lambda + x2 + y1
#
# If we have two points: P1 = (x1,y1)
#                        P2 = (x2,y2)
# And we want to find    P3 = (x3,y3)
# such that              P3 = P1 + P2
# This is known as Point Addition
# It is done as:
#   Let lambda = (y1+y2)/(x1+x2)
#   then    x3 = a + lambda + lambda^2 + x1 + x2
#   and     y3 = (x2+x3)lambda + x3 + x2
#
# ECC involves elliptic curves over a finite field
# There are two fields of interest:
#   Prime Fields GF(p)
#   Binary finite fields GF(2^m)
# Points on the elliptic curves are
# written as P(x,y) where x and y are elements of GF(p)
#
# The size of a set of a elliptic curve domain parameters
# on a prime curve is defined as as the number of bits
# in the binary representation of the field order
# commonly denoted 'p'
#
# Size on a characteristic-2 curve is defined as the number
# of bits in the binary representation of the field
# commonly denoted 'm'
#
# Elliptic Curve Discrete Logarithmic Problem (ECDLP)
# has the following components:
#   A well defined finite field GF(p) or GF(2^m)
#   A point P, of higher order, present on the elliptic curve E
#   A scalar mutliple of P, let's say k
#       such that k.P = P+P+P+P+...+P (k times)
#
# So ECDLP involves scalar multiplication
# When we have k and P it is easy to find k.P
# But it is really hard to find k from k.P and P
#
# For GF(p) the finite fields can be from the following defined set
#   p = {112; 128; 160; 192; 224; 256; 384; 512; 1024}
# For GF(2^m) the finite fields can be from the following defined set
#   m = {113; 131; 163; 193; 233; 239; 283; 409; 571}
# Many different curves can be chosen for the same field by different users
# Many such curves and their domain parameters
# Are defined in Standards for Efficient Cryptography
#
#
# --- COMPONENTS NEEDED ---
#   A prime number    'p'
#   A point           'P' (with its components on a defined elliptic curve
#   A scalar multiple 'k'
#   Let 'b' be character base. as 54xx is as 16-bit processor
#       so 'b' = 2^16
#   A positive integer 'R' which is larger than p and co-prime with p
#       we may use R = b^t > p. t is taken as 10
#       so R in this case is is 2^160
#           NOTE: values of p, point P, and k used are from
#                 the Recommended Domain Parameters

import collections


def sqrt(n, q):
    # sqrt on PN modulo: returns two numbers or exception if does not exist
    assert n < q
    # For all numbers up until the prime
    for i in range(1, q):
        # If number squared, modulo the prime equals the original number
        # Then it is a square root
        if i * i % q == n:
            # Return the square roots
            return (i, q-i)
        pass
    raise Exception("not found")


def inv(n, q):
    # Div on PN modulo a/b mod q as  a * inv(b, q) mod q
    for i in range(q):
        # For values i up to max q
        if (n * i) % q == 1:
            # print(i)
            return i
        pass
    assert False, "unreached"
    pass

Coord = collections.namedtuple("Coord", ["x", "y"])


class EllipticCurve(object):
    # System of Elliptic Curve
    def __init__(self, a, b, q):
        # a, b: params of the curve formula
        # q   : prime number
        # break if a <= 0 or a >= q or 0 >= b or b >= q or q <= 2
        assert 0 < a and q > a and b > 0 and q > b and q > 2
        assert (4 * (a ** 3) + 27 * (b ** 2)) % q != 0
        self.a = a
        self.b = b
        self.q = q
        # Set a zero coordinate for use with "add" (it is not on the curve)
        self.zero = Coord(0, 0)

    def at(self, x):
        # Find the point on the curve at x
        # x is an int < q
        # Returns: ((x, y), (x, -y)) or not found exception
        assert x < self.q
        # Find the value then modulo it into range on the curve
        y_squared = (x**3 + self.a * x + self.b) % self.q
        # Find the square roots using our defined function
        y, y_negative = sqrt(y_squared, self.q)
        return Coord(x, y), Coord(x, y_negative)

    def order(self, g):
        # Returns the order of point g
        # Make sure the point is valid and not (0, 0)
        #                     is valid returns true of (0, 0)
        assert self.is_valid(g) and g != self.zero

        # For each integer from 1 to q + 1
        for i in range(1, self.q + 1):
            if self.mul(g, i) == self.zero:
                return i
            pass
        raise Exception("Invalid Order")

    def mul(self, p, n):
        orig_n = n
        # Multiply point p, n times
        r = self.zero
        m2 = p
        # O(log2(n)) add
        # While n is a positive number
        while 0 < n:
            # If n bitwise add 1 == 1
            if n & 1 == 1:
                r = self.add(r, m2)
                pass
            n, m2 = n >> 1, self.add(m2, m2)
            pass
        # reference O(n) add
        # for i in range(n):
        #   r = self.add(r, p)
        #   pass
        # print("{} multiplied by {} = {}".format(p, orig_n, r))
        return r


    def add(self, p1, p2):
        # Add the points

        # If either of the points are zero
        # then them added is just the non-zero point
        if p1 == self.zero: return p2
        if p2 == self.zero: return p1

        if p1.x == p2.x and (p1.y != p2.y or p1.y == 0):
            # basically means the points add to (0, 0)
            # p1 + -p1 == (0, 0)
            return self.zero

        if p1.x == p2.x:
            # Use the tangent line of p1 as (p1, p1) line
            l = (3 * p1.x * p1.x + self.a) * inv(2 * p1.y, self.q) % self.q
            pass
        else:
            l = (p2.y - p1.y) * inv(p2.x - p1.x, self.q) % self.q
            pass
        x = (l * l - p1.x - p2.x) % self.q
        y = (l * (p1.x - x) - p1.y) % self.q
        return Coord(x, y)

    def is_valid(self, p):
        # If the point is (0,0) it is valid
        if p == self.zero: return True
        left = (p.y ** 2) % self.q
        right = ((p.x ** 3) + self.a * p.x + self.b) % self.q
        # If the y coordinate squared, modulo q == The curve at x coordinate, modulo q
        # It is a valid coordinate
        return left == right

    def neg(self, p):
        # Negate p
        # print("P: {}\nNegated P: {}".format(p, Coord(p.x, -p.y % self.q)))
        return Coord(p.x, -p.y % self.q)


class ElGamal(object):
    # Public key encryption as replacing (mulmod, powmod) to (ec.add, ec.mul)
    # ec: elliptical curve
    # g : a (random) point on ec

    def __init__(self, ec, g):
        # Make sure g is a valid point on ec
        assert ec.is_valid(g)
        self.ec = ec  # The curve
        self.g = g  # A point on the curve
        self.n = ec.order(g)  # The order of the point on the curve
        pass

    def gen(self, priv):
        # Generate the public key
        # priv: private key as random int < ec.q
        # returns: public key as points on ec
        return self.ec.mul(self.g, priv)

    def enc(self, plain, pub, r):
        # Encrypt
        # plain  : data as a point on ec
        # pub    : public key as points on ec
        # r      : random int < ec.q
        # returns: (cipher1, cipher2) as points on ec

        # Verify that plain and pub are points on the curve
        assert self.ec.is_valid(plain)
        assert self.ec.is_valid(pub)

        # Return the encoded information
        return (self.ec.mul(self.g, r), self.ec.add(plain, self.ec.mul(pub, r)))

    def dec(self, cipher, priv):
        # Decrypt
        # Cipher: (cipher1, cipher2) as points on the ec
        # priv: private key as int < ec.q
        # Returns: plain as a point on ec

        # Split cipher into its two component ciphers
        c1, c2 = cipher

        # Verify that the ciphers are both on ec
        assert self.ec.is_valid(c1) and self.ec.is_valid(c2)

        # Return the "plain" point
        return self.ec.add(c2, self.ec.neg(self.ec.mul(c1, priv)))
    pass







if __name__ == "__main__":
    a_val = 2
    b_val = 31
    q_val = 571  # Chosen because it is prime, and results in more than 255 valid coordinates

    # Create the elliptic curve
    elliptic_curve = EllipticCurve(a_val, b_val, q_val)

    # This part is unneeded. It is here to check all the valid points
    valid_points = []
    for i in range(q_val):
        try:
            valid_points.append(elliptic_curve.at(i)[0])
        except Exception:
            pass

    # Get coordinate at one of the valid points
    g, _ = elliptic_curve.at(12)

    # Verify that the point is under the correct order (max of q)
    assert elliptic_curve.order(g) <= elliptic_curve.q

    # ElGamal encoding/decoding usage
    eg = ElGamal(elliptic_curve, g)

    # Mapping value to elliptic_curve point
    # "Masking": value 'k' to point elliptic_curve.mul(g, k)
    # ("Imbedding" on proper n: use a point of x as 0 <= n*v <= x < n*(v+1) < q)
    mapping = [elliptic_curve.mul(g, i) for i in range(eg.n)]
    # mapping is a list of all the points on the curve

    # The private key
    priv = 5

    # Generate the public key
    pub = eg.gen(priv)
    print("Public key: {}".format(pub))

    message = "Hello World!"

    # Split the message into its individual characters
    chars_to_encrypt = []
    for letter in message:
        chars_to_encrypt.append(letter)

    # Convert each letter to its ordinal value and get the coordinate at that index in the map
    mapped_chars = []
    for char in chars_to_encrypt:
        mapped_chars.append(mapping[ord(char)])

    # Encrypt each of the coordinates
    cipher_coords = []
    for coord in mapped_chars:
        cipher_coords.append(eg.enc(coord, pub, 15))

    # Decrypt the encrypted coordinates
    deciphered_chars = []
    for cipher in cipher_coords:
        deciphered_chars.append(chr(mapping.index(eg.dec(cipher, priv))))

    decoded_message = "".join(deciphered_chars)
    print(decoded_message)

    pass


