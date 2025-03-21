# nttdatapay-python

## Prerequisites
- UAT MID and keys provided by the NDPS team

## Installation
1. Install the python server.

2. Use below commands to install pycryptodome and requests package
- Install `pycryptodome` for encryption and decryption
    
    pip install pycryptodome
    
- Install `requests` for rest API calling
    
    pip install requests

3. Modify the request.py file
- Change the configuration details like merchId, password, product etc.
- Configure `authurl` and `atomcheckout.js` according to UAT and Production environments.

4. Change the keys provided by NDPS in `AESCipher.py `

5. To handle the response use `response.py`

## How to use
1. Click on `Pay Now` button, which will open the NTTDATA Payment Gateway.

2. When the transaction is completed, you will get the response on your return url in this case `response.py`


