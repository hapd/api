from init_gh import GHFiles
import json
import datetime

'''------------Add user--------------'''
def makeResponseForAddUser(req):
    gh = GHFiles("users.json")
    temp = gh.file_contents
    pid = temp["currentPID"]
    year = str(req.get('dob')).split("/")[2]
    age = datetime.datetime.now().year - int(year)
    temp[str(pid)] = {
        "name": req.get('name'),
        "pin": req.get('pin'),
        "nurse": req.get('nurse'),
        "age": age,
        "dob": req.get('dob'),
        "gender": req.get('gender'),
        "contact": req.get('contact')
    }
    temp["currentPID"] = str(int(temp["currentPID"])+1)
    temp = json.dumps(temp, indent=4)
    out = gh.update(temp, "users.json")
    res = {}
    if(out == True):
        res["fullfilmentText"] = "Account creation successful"
    elif(out == False):
        res["fullfilmentText"] = "Account creation failed"
    res["source"] = "webhook-hapd-api"
    res["PID"] = pid
    return res

'''------------Check Login--------------'''
def makeResponseForCheckLogin(req):
    gh = GHFiles("users.json")
    temp = gh.file_contents
    pid = req.get('pId')
    pin = req.get('pin')
    if(temp[pid]['pin'] == pin):
        fullfilmentText = 'True'
    else:
        fullfilmentText = 'False'
    res = {}
    res["fullfilmentText"] = fullfilmentText
    res["source"] = "webhook-hapd-api"
    return res

'''--------------Who Am I---------------'''
def makeResponseForWhoAmI(req):
    gh = GHFiles('users.json')
    temp = gh.file_contents
    pid = req.get('pId')
    information = temp[pid]
    data = {}
    data["name"] = information["name"]
    dob = information["dob"]
    year = str(dob).split("/")[2]
    age = datetime.datetime.now().year - int(year)
    data["age"] = age
    data["dob"] = dob
    res = {}
    res["fullfilmentText"] = "Data Found"
    res["data"] = data
    res["source"] = "webhook-hapd-api"
    return res

'''---------------Schedule---------------'''
def makeResponseForSchedule(req):
    gh = GHFiles('schedule.json')
    temp = gh.file_contents
    pid = req.get("pId")
    res = {}
    out = False
    if(req.get("req_type") == "add_schedule"):
        temp[pid] = req.get("data")
        temp = json.dumps(temp, indent=4)
        out = gh.update(temp, "schedule.json")
    if(req.get("req_type") == "read_schedule"):
        if(pid in temp):
            schedule = temp[pid]
            print(temp[pid])
            res["schedule"] = { "tasks":schedule, "found": "True"}
        else:
            res["schedule"] = { "found": "False" }
    if(out == True):
        res["fullfilmentText"] = ("%s successful")%str(req.get("req_type"))
    else:
        res["fullfilmentText"] = ("%s failed")%str(req.get("req_type"))
    res["source"] = "webhook-hapd-api"
    return res


'''---------------AuthenticateNurse---------------'''
def makeResponseForAuthenticateNurse(req):
    gh=GHFiles("nurse.json")
    data=gh.file_content
    res={}
    if(req.get("id") in data):
        if(req.get("password")==data.get(req.get("id")).get("password")):
            res["fullfilmentText"]="Access Granted"
        else:
             res["fullfilmentText"]="Access Denied"
    res["source"] = "webhook-hapd-api"
    return res




