import uuid
import urllib2
import simplejson


bal_en = urllib2.Request(
    data=simplejson.dumps(
        { "text" : "Bal.uyb538",
          "from" : "18185846103",
          "uuid" : str(uuid.uuid4()) } 
        ),
    url="http://localhost:6543/sms/send") 

response = urllib2.urlopen(bal_en)
print("----------------------------") 
print("Testing english balance") 
print(response.read()) 
print("-----------------------------") 


bal_fn = urllib2.Request(
    data=simplejson.dumps(
        { "text" : "solde.uyb538",
          "from" : "18185846103",
          "uuid" : str(uuid.uuid4()) } 
        ),
    url="http://localhost:6543/sms/send") 

response = urllib2.urlopen(bal_fn) 
print("----------------------------") 
print("Testing french balance") 
print(response.read())
print("----------------------------") 
