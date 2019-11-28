# Author: Valeri Kozarev
# Inspired by https://cranklin.wordpress.com/2017/07/11/lets-create-our-own-cryptocurrency/
# Valerium is a non-ICO'd cryptocurrency that is powered by elliptic curve cryptography https://cryptography.io/en/latest/

import cryptography

# method for creating the keys that we need
def create_keys(self, private_key, public_key):
    # store the keys
    if private_key is not None and public_key is not None:
        self.__private_key__ = private_key.decode("hex")
        self.__public_key = public_key.decode("hex")

    # if no keys, create your own
    else:
       # TODO
