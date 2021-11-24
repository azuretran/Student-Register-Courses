.. image:: https://badge.fury.io/py/m2secret-py3.svg
   :target: https://pypi.python.org/pypi/m2secret-py3

.. image:: https://travis-ci.org/EnTeQuAk/m2secret.svg?branch=master
   :target: https://travis-ci.org/EnTeQuAk/m2secret

m2secret is a simple encryption and decryption module and CLI utility built
with the M2Crypto library to make it easy to secure strings and files from
prying eyes.

By default it will use 256-bit AES (Rijndael) symmetric-key cryptography in
CBC mode. Key material is derived from submitted password using the PBKDF2
algorithm.

m2secret originally developed by Heikki Toivonen: http://www.heikkitoivonen.net/m2secret/


