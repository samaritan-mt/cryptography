from operator import truediv
import sys
import random
from unittest import result
iter=4
''' 
Generate a random prime number of length l
'''

def generatePrime(l):
    found = False
    res = 0
    while(not found):
        res = random.randint(pow(10,l-1),pow(10,l))
        if (res%2 == 0):
            res +=1 
        found = isPrime(res,iter)
    return res
'''
Efficient Modular exponentiation
''' 
def power(x, y, p):
    res = 1
    x = x % p
    while (y > 0):
        if (y & 1):
            res = (res * x) % p
 
        y = y>>1
        x = (x * x) % p
    return res



'''
Miller-Rabin primality test
'''
def miillerTest(d, n):
     
    a = 2 + random.randint(1, n - 4)
 
    x = power(a, d, n)
 
    if (x == 1 or x == n - 1):
        return True

    while (d != n - 1):
        x = (x * x) % n
        d *= 2
 
        if (x == 1):
            return False
        if (x == n - 1):
            return True
    return False

'''
Prime testing function with some optimizations calling Miller-Rabin function
'''

def isPrime( numberToTest, iter):
     
    if (numberToTest <= 1 or numberToTest == 4):
        return False
    if (numberToTest <= 3):
        return True
    intermediate1 = numberToTest - 1
    while (intermediate1 % 2 == 0):
        intermediate1 //= 2
 
    # Iterate given number of 'k' times
    for i in range(iter):
        if (miillerTest(intermediate1, numberToTest) == False):
            return False
 
    return True

e=65537



'''
Fonction to calculate d such that e*d = 1 mod (p-1)(q-1) where p and q are prime numbers (Private key)
'''

def computePrivateKey(p,q,e):
    return pow(e,-1,(p-1)*(q-1))
    
'''
Fonction to calculate m^e mod n 
'''
def function(n,m,e=65537):
    return power(m,e,n)

'''
Dict to store a representation of the alphabet
'''
dict = {}
for i in range(10,36):
    dict[chr(i+87)] = i
'''
Function to code a given string chars (lowercase) into a base10 integer 
'''
def code(string):
    res = []
    for i in range(len(string)):
        res.append(dict.get(string[i]))
    result = ''
    for i in range(len(res)):
        result += str(res[i])
    return int(result)

'''
Function to decode a given integer into a string of chars (lowercase) (reverse of code function gives the string corresponding to the integer)
'''
def decode(integer):    
    res = []
    while integer != 0:
        res.append(integer%100)
        integer = (int) (integer/100)
    result = ''
    res.reverse()   
    for i in range(len(res)):
        keys = [k for k, v in dict.items() if v == res[i]]
        result += keys[0]
    return result

'''
Function to encrypt a given string using RSA algorithm given the plaintext and a public key (n,e)
'''
def RSAenc(plaintext,n,e):
    encodedtext = code(plaintext)
    return function(n,encodedtext,e)

'''
Function to decrypt a given ciphertext using RSA algorithm given the ciphertext and a private key (n,d)
'''
def RSAdec(ciphertext,n,d):
    return decode(function(n,ciphertext,d))


if __name__=="__main__":
    p = generatePrime(15)
    q = generatePrime(15)
    print("p = ",p)
    print("q = ",q)
    n = p*q
    d = computePrivateKey(p,q,2**16+1)
    print("n = ",n)
    print("d = ",d)
    cipher = RSAenc('hello',n,e)
    print(cipher)
    plain = RSAdec(cipher,n,d)
    print(plain)