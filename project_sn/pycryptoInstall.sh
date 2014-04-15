#! /bin/bash

wget http://ftp.dlitz.net/pub/dlitz/crypto/pycrypto/pycrypto-2.6.1.tar.gz
gunzip pycrypto-2.6.1.tar.gz
tar xvf pycrypto-2.6.1.tar
sudo apt-get install python3.2-dev
cd pycrypto-2.6.1
python3.2 setup.py build
sudo python3.2 setup.py install
