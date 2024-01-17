import random
import math

def check_prime(n, k=5):
    if n <= 1:
        return False
    elif n == 2 or n == 3:
        return True
    elif n % 2 == 0:
        return False

    def miller_rabin_test(d, n):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            return True

        while d != n - 1:
            x = (x * x) % n
            d *= 2
            if x == 1:
                return False
            if x == n - 1:
                return True

        return False

    d, r = n - 1, 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for _ in range(k):
        if not miller_rabin_test(d, n):
            return False

    return True

def generate_prime(bits=1024):
    candidate = random.getrandbits(bits)
    while not check_prime(candidate):
        candidate = random.getrandbits(bits)
    return candidate

def generate_keypair(bits=1024):
    p = generate_prime(bits)
    q = generate_prime(bits)

    n = p * q
    phi = (p - 1) * (q - 1)

    e = random.randint(2, phi - 1)
    while math.gcd(e, phi) != 1:
        e = random.randint(2, phi - 1)

    d = pow(e, -1, phi)
    public_key = (n, e)
    private_key = (n, d)

    return public_key, private_key

def encrypt(msg, public_key):
    n, e = public_key
    encrypted_msg = [pow(ord(char), e, n) for char in msg]
    return encrypted_msg

def decrypt(encrypted_msg, private_key):
    n, d = private_key
    decrypted_msg = ''.join([chr(pow(ch, d, n)) for ch in encrypted_msg])
    return decrypted_msg

public_key, private_key = generate_keypair()
msg = "Hello, RSA!"
print("Original message:", msg)

# Encryption
encrypted_msg = encrypt(msg, public_key)
print("Encrypted message:", encrypted_msg)

# Decryption
dec_msg = decrypt(encrypted_msg, private_key)
print("Decrypted message:", dec_msg)