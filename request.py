#!C:\Users\Dell\AppData\Local\Programs\Python\Python39\python.exe -u

#Developed by Sagar Gopale, Senior Software Engineer, Atom Technologies Ltd

import cgi
import requests
import json
import uuid
from time import gmtime, strftime
from AESCipher import *

amount = '10.00'
merchTxnId = uuid.uuid4().hex[:12]
merchId = '8952'
password = 'Test@123'
product = 'NSE'
custEmail = 'sagar.gopale@atomtech.in'
custMobile = '8976286911'
returnUrl = 'http://localhost/kits/python3Kit/response.py'
txnDate = strftime("%Y-%m-%d %H:%M:%S", gmtime())

jsondata = '{ "payInstrument": { "headDetails": { "version": "OTSv1.1", "api": "AUTH", "platform": "FLASH" }, "merchDetails": { "merchId": "'+str(merchId)+'", "userId": "", "password": "'+str(password)+'", "merchTxnId": "'+str(merchTxnId)+'", "merchTxnDate": "'+str(txnDate)+'" }, "payDetails": { "amount": "'+str(amount)+'", "product": "'+str(product)+'", "custAccNo": "213232323", "txnCurrency": "INR" }, "custDetails": { "custEmail": "'+str(custEmail)+'", "custMobile": "'+str(custMobile)+'" }, "extras": {"udf1": "udf1","udf2": "udf2","udf3": "udf3","udf4": "udf4","udf5": "udf5"} } }'

cipher = AESCipher('self')
encrypted = cipher.encrypt(bytes(jsondata, encoding="raw_unicode_escape"))

url = "https://caller.atomtech.in/ots/aipay/auth"
payload = "encData="+encrypted+"&merchId="+str(merchId)
headers = {
    'content-type': "application/x-www-form-urlencoded",
    'cache-control': "no-cache"
}
cafile = 'cacert.pem'
response = requests.request("POST", url, data=payload, headers=headers, verify=cafile)

arraySplit = response.text.split('&')
arraySplitTwo = arraySplit[1].split('=')
#
decrypted = cipher.decrypt(arraySplitTwo[1])
json_string = decrypted.replace("", " ")
y = json.loads(json_string)
atomTokenId = y['atomTokenId']

print("Content-type: text/html \n\r\n")
print ("<html><head>")      
print ('<meta charset="utf-8">')
print ('<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">')
print ('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">')
print ("</head><body>")
print ('<div class="container my-5">')
print ('<h3 class="">Merchant Shop</h3>')
print ("<p>Transaction Id: "+str(merchTxnId)+"</p>")
print ("<p>Atom Token Id: "+str(atomTokenId)+"</p>")
print ('<p>Pay Rs. '+str(amount)+'</p>')
print ('<a class="btn btn-primary" href="javascript:openPay(\''+str(atomTokenId)+'\', \''+str(merchId)+'\' , \''+str(custEmail)+'\' , \''+str(custMobile)+'\', \''+str(returnUrl)+'\')" role="button">Pay Now</a>')
print ('</div>')
print ('<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script><script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script><script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script><script src="https://pgtest.atomtech.in/staticdata/ots/js/atomcheckout.js"></script><script src="main.js"></script>')
print ("</body></html>")