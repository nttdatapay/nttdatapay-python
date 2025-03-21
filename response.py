#!C:\Users\Dell\AppData\Local\Programs\Python\Python39\python.exe -u

import cgi
import json
import binascii
from AESCipher import *

data = cgi.FieldStorage()
rawData = data.getvalue('encData')
cipher = AESCipher('self')
decrypted = cipher.decrypt(rawData)
#
size = len(decrypted)
jstring = decrypted.replace("", " ")
decodedData = json.loads(jstring)

print("Content-type: text/html \n\r\n")
print("<br>")
#print(decodedData)
if decodedData['payInstrument']['responseDetails']['statusCode'] == "OTS0000":
    print("Transaction Result : " + decodedData['payInstrument']['responseDetails']['statusCode'] +"<br>")
    print("Merchant Transaction Id : " + decodedData['payInstrument']['merchDetails']['merchTxnId']+"<br>")
    print("Transaction Date : " + decodedData['payInstrument']['merchDetails']['merchTxnDate']+"<br>")
    print("Bank Transaction Id : " + decodedData['payInstrument']['payModeSpecificData']['bankDetails']['bankTxnId'])
    print("<br>")
    print("<br>")
    print("<br>")
    print("All Response Data = <br> <br>")
    print(decodedData)
else:   
    print("Payment failed, Please try again.. <br>")