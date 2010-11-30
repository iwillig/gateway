import uuid
import urllib2
import simplejson

account = "cbr236"
token = 78599181440
def make_request(msg,phone="18182124554"): 
    return urllib2.Request(
        data=simplejson.dumps({ "text" : msg,
                                "from" : phone,
                                "uuid" : str(uuid.uuid4()) } 
                              ),url="http://localhost:6543/sms/send")


response = urllib2.urlopen(make_request("bal." + account))
print("----------------------------") 
print("testing english balance") 
print(response.read()) 
print("-----------------------------") 

response = urllib2.urlopen(make_request("bal.1234"))
print("----------------------------") 
print("testing english balance fail conition") 
print(response.read()) 
print("-----------------------------") 

response = urllib2.urlopen(make_request("solde." + account)) 
print("----------------------------") 
print("testing french balance") 
print(response.read())
print("----------------------------") 

response = urllib2.urlopen(make_request("solde.12345")) 
print("----------------------------") 
print("testing french balance fail conition") 
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
print("turn the circuit off fr/en ") 
print(response.read())
print("----------------------------") 

# response = urllib2.urlopen(make_request("use." + account)) 
# print("----------------------------") 
# print("testing use en") 
# print(response.read())
# print("----------------------------") 

# response = urllib2.urlopen(make_request("conso." + account)) 
# print("----------------------------") 
# print("testing use fr") 
# print(response.read())
# print("----------------------------") 


response = urllib2.urlopen(make_request("this should fail" + account)) 
print("----------------------------") 
print("test failure with a response") 
print(response.read())
print("----------------------------") 

# cid = "192.168.1.201"
# meter_name = "demo001"
# # test primary log 
# response = urllib2.urlopen(
#     make_request("Job=pp&cid=" 
#                  + cid  + "&mid=" + meter_name + 
#                  "&wh=10.00&tu=12.12&cr=20.10&status=1",phone="18185846103"))
# print("----------------------------") 
# print("testing primary log") 
# print(response.read())
# print("----------------------------") 

# # test service halt 
# response = urllib2.urlopen(
#     make_request("Job=alerts&mid=" + 
#                  meter_name + "&cid=" + cid + "&alert=md",phone="18185846103")) 
# print("----------------------------") 
# print("testing alert ce") 
# print(response.read())
# print("----------------------------") 
# # test meter sd card not found 
# response = urllib2.urlopen(
#     make_request("Job=alerts&mid=" + 
#                  meter_name + "&cid=" + cid + "&alert=sdc",phone="18185846103")) 
# print("----------------------------") 
# print("testing alert ce") 
# print(response.read())
# print("----------------------------") 
# # test circuit low credit
# response = urllib2.urlopen(
#     make_request("Job=alerts&mid=" + 
#                  meter_name + "&cid=" + cid 
#                  + "&alert=lcw&cr=10.00",phone="18185846103")) 
# print("----------------------------") 
# print("testing alert ce") 
# print(response.read())
# print("----------------------------") 

# # test circuit no credit 
# response = urllib2.urlopen(
#     make_request("Job=alerts&mid=" 
#                  + meter_name + "&cid=" 
#                  + cid + "&alert=nocw&cr=00.00",phone="18185846103")) 
# print("----------------------------") 
# print("testing alert ce") 
# print(response.read())
# print("----------------------------") 
# # test circuit compontent failure 
# response = urllib2.urlopen(
#     make_request("Job=alerts&mid=" 
#                  + meter_name + "&cid=" + cid + "&alert=ce",phone="18185846103")) 
# print("----------------------------") 
# print("testing alert ce") 
# print(response.read())
# print("----------------------------") 
