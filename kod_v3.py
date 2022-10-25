# Szyfr Afiacyjny

from time import time
from sys import exit
import cryptomath, random
from argparse import ArgumentParser
from catalan import catalan

SYMBOLS = """ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~"""

timeStart = time()


def main(myMode=None, cypher=None, localFile=''):
    #try catch na plik
    myMessage = "Blue is the colour, football is the game We're all together, and winning is our aim So cheer us on through the sun and rain 'cause Chelsea, Chelsea is our name."
    #myMessage = """"fX<*h>}(rTH<Rh()?<?T]TH=T<rh<tT<*_))T?<ISrT))I~TSr<Ii<Ir<*h()?<?T*TI=T<_<4(>_S<ISrh<tT)IT=IS~<r4_r<Ir<R_]<4(>_SEf<0X)_S<k(HIS~"""
    if cypher == 'catalan':
        catalan()
    elif cypher == 'random':
        random()
    myKey = 2023
    myMode = 'encrypt' # ustawiamy 'encrypt' lub 'decrypt'

    if myMode == 'encrypt':
        translated = encryptMessage(myKey, myMessage)
    elif myMode == 'decrypt':
        translated = decryptMessage(myKey, myMessage)
    print('Key: %s' % (myKey))
    print('%sed text:' % (myMode.title()))
    print(translated)



def getKeyParts(key):
    keyA = key // len(SYMBOLS)
    keyB = key % len(SYMBOLS)
    return (keyA, keyB)

# Szyfr afiniczny staje się niewiarygodnie słaby, gdy klucz A jest ustawiony na 1. Wybierz inny klucz

def checkKeys(keyA, keyB, mode):
    if keyA == 1 and mode == 'encrypt':
        exit('The affine cipher becomes incredibly weak when key A is set to 1. Choose a different key.')
    if keyB == 0 and mode == 'encrypt':
        exit('The affine cipher becomes incredibly weak when key B is set to 0. Choose a different key.')
    if keyA < 0 or keyB < 0 or keyB > len(SYMBOLS) - 1:
        exit('Key A must be greater than 0 and Key B must be between 0 and %s.' % (len(SYMBOLS) - 1))
    if cryptomath.gcd(keyA, len(SYMBOLS)) != 1:
        exit('Key A (%s) and the symbol set size (%s) are not relatively prime. Choose a different key.' % (keyA, len(SYMBOLS)))


def encryptMessage(key, message):
    keyA, keyB = getKeyParts(key)
    checkKeys(keyA, keyB, 'encrypt')
    ciphertext = ''
    for symbol in message:
        if symbol in SYMBOLS:
            # encrypt this symbol
            symIndex = SYMBOLS.find(symbol)
            ciphertext += SYMBOLS[(symIndex * keyA + keyB) % len(SYMBOLS)]
        else:
            ciphertext += symbol 
    return ciphertext


def decryptMessage(key, message):
    #uwzglednic plik np dodac do org -unecrypted
    keyA, keyB = getKeyParts(key)
    checkKeys(keyA, keyB, 'decrypt')
    plaintext = ''
    modInverseOfKeyA = cryptomath.findModInverse(keyA, len(SYMBOLS))

    for symbol in message:
        if symbol in SYMBOLS:
            # decrypt this symbol
            symIndex = SYMBOLS.find(symbol)
            plaintext += SYMBOLS[(symIndex - keyB) * modInverseOfKeyA % len(SYMBOLS)]
        else:
            plaintext += symbol 
    return plaintext


def getRandomKey():
    while True:
        keyA = random.randint(2, len(SYMBOLS))
        keyB = random.randint(2, len(SYMBOLS))
        if cryptomath.gcd(keyA, len(SYMBOLS)) == 1:
            return keyA * len(SYMBOLS) + keyB



parser = ArgumentParser(description='Co to robi')
modeGroup = parser.add_mutually_exclusive_group(required=True)
modeGroup.add_argument('-e', '--encrypt', action='store_true', help='co robi')
modeGroup.add_argument('-d', '--decrypt', action='store_true', help='co robi')
cypherGroup = parser.add_mutually_exclusive_group(required=True)
cypherGroup.add_argument('-c', '--catalan', action='store_true', help='co robi')
cypherGroup.add_argument('-r', '--random', action='store_true', help='co robi')
cypherGroup.add_argument('-u', '--user', action='store_true', help='co robi')

parser.add_argument('-f', '--file', type=str, help='Full path to local file')
parser.add_argument('-v', '--version', action='version', version='%(prog)s \n version: 1.0')
cliArguments = vars(parser.parse_args())

if __name__ == '__main__':
    
    if cliArguments['encrypt'] is True:
        if cliArguments['catalan'] is True:
            if cliArguments['file']:
                main(myMode='encrypt',cypher='catalan', localFile=cliArguments['file'])
        elif cliArguments['random'] is True:
            if cliArguments['file']:
                main(cypher='random', localFile=cliArguments['file'])
        elif cliArguments['user'] is True:
            if cliArguments['file']:
                main(cypher='user', localFile=cliArguments['file'])        
    
    elif cliArguments['decrypt'] is True:
        if cliArguments['catalan'] is True:
            if cliArguments['file']:
                main(myMode='encrypt',cypher='catalan', localFile=cliArguments['file'])
        elif cliArguments['random'] is True:
            if cliArguments['file']:
                main(cypher='random', localFile=cliArguments['file'])
        elif cliArguments['user'] is True:
            if cliArguments['file']:
                main(cypher='user', localFile=cliArguments['file'])  
print('Time: ', time() - timeStart)