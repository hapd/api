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
        "age": str(age),
        "dob": req.get('dob'),
        "stage": req.get('stage'),
        "gender": req.get('gender'),
        "contact": req.get('contact'),
        "bloodgroup": req.get('bloodgroup'),
        "nurseId": req.get('nurseId'),
        "image": req.get('image')
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
    data=gh.file_contents
    res={}
    if(req.get("id") in data):
        if(req.get("password")==data.get(req.get("id")).get("password")):
            res["fullfilmentText"]="Access Granted"
        else:
             res["fullfilmentText"]="Access Denied"
    res["source"] = "webhook-hapd-api"
    return res

'''---------------Nurse Information---------------'''
def makeResponseForNurse(req):
    gh = GHFiles("nurse.json")
    data = gh.file_contents
    res = {}
    if(req["req_type"] == "add_nurse"):
        currentNurseId = max(list(data.keys()))
        d = {}
        d["name"] = str(req.get("data").get("name"))
        d["nop"] = "0"
        d["nos1"] = "0"
        d["nos2"] = "0"
        d["nos3"] = "0"
        d["nos4"] = "0"
        d["nos5"] = "0"
        d["email"] = str(req.get("data").get("email"))
        d["password"] = str(req.get("data").get("password"))
        d["contact"] =  str(req.get("data").get("contact"))
        data[str(int(currentNurseId)+1)] = d
        temp = json.dumps(data, indent=4)
        out = gh.update(temp, "nurse.json")
        if(out == True):
            res["fullfilmentText"] = "True"
        else:
            res["fullfilmentText"] = "False"
        res["nurseId"] = str(int(currentNurseId)+1)
    elif(req["req_type"] == "read_nurse"):
        nurseId = req["data"]["nurseId"]
        res["data"] = {
            "nurseId": nurseId,
            "name": data[nurseId]["name"],
            "nop": data[nurseId]["nop"],
            "email": data[nurseId]["email"],
            "contact": data[nurseId]["contact"],
            "nos1": data[nurseId]["nos1"],
            "nos2": data[nurseId]["nos2"],
            "nos3": data[nurseId]["nos3"],
            "nos4": data[nurseId]["nos4"],
            "nos5": data[nurseId]["nos5"]
        }
        res["fullfilmentText"] = "True"
    elif(req["req_type"] == "increment_nop"):
        nurseId = req["data"]["nurseId"]
        nop = int(data[nurseId]["nop"]) + 1
        data[nurseId]["nop"] = str(nop)
        temp = json.dumps(data, indent=4)
        out = gh.update(temp, "nurse.json")
        if(out == True):
            res["fullfilmentText"] = "True"
        else:
            res["fullfilmentText"] = "False"
    elif(req["req_type"] == "increment_nos"):
        nurseId = req["data"]["nurseId"]
        stage = req["data"]["stage"]
        s = "nos%s"%stage
        nos = data[nurseId][s]
        data[nurseId][s] = str(int(nos)+1)
        temp = json.dumps(data, indent = 4)
        gh.update(temp, "nurse.json")
        if(out == True):
            res["fullfilmentText"] = "True"
        else:
            res["fullfilmentText"] = "False"
    res["source"] = "webhook-hapd-api"
    return res
        
