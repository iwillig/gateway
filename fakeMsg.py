import uuid
import urllib2
import simplejson

account = "bph583"
token = 94215924356
def make_request(msg): 
    return urllib2.Request(
        data=simplejson.dumps({ "text" : msg,
                                "from" : "18185846103",
                                "uuid" : str(uuid.uuid4()) } 
                              ),url="http://localhost:6543/sms/send")

response = urllib2.urlopen(make_request("bal." + account))
print("----------------------------") 
print("testing english balance") 
print(response.read()) 
print("-----------------------------") 

response = urllib2.urlopen(make_request("solde." + account)) 
print("----------------------------") 
print("testing french balance") 
print(response.read())
print("----------------------------") 

response = urllib2.urlopen(make_request("prim." + account + ".18182124554")) 
print("----------------------------") 
print("set primary number english") 
print(response.read())
print("----------------------------") 

response = urllib2.urlopen(make_request("tel." + account +  ".18185846103")) 
print("----------------------------") 
print("set primary number fr") 
print(response.read())
print("----------------------------") 

response = urllib2.urlopen(
    make_request("add." + account + "." + str(token))) 
print("----------------------------") 
print("add credit in en") 
print(response.read())
print("----------------------------") 

response = urllib2.urlopen(
    make_request("recharge." + account  +"." + str(token))) 
print("----------------------------") 
print("add credit in fr") 
print(response.read())
print("----------------------------") 

response = urllib2.urlopen(make_request("on." + account)) 
print("----------------------------") 
print("turn the circuit on fr/en ") 
print(response.read())
print("----------------------------") 

response = urllib2.urlopen(make_request("off." + account)) 
print("----------------------------") 
print(" turn the circuit off fr/en ") 
print(response.read())
print("----------------------------") 

response = urllib2.urlopen(make_request("use." + account)) 
print("----------------------------") 
print(" turn the circuit off fr/en ") 
print(response.read())
print("----------------------------") 

response = urllib2.urlopen(make_request("conso." + account)) 
print("----------------------------") 
print(" turn the circuit off fr/en ") 
print(response.read())
print("----------------------------") 


response = urllib2.urlopen(make_request("this should fail" + account)) 
print("----------------------------") 
print(" test failure ") 
print(response.read())
print("----------------------------") 
