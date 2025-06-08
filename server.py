
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
load_dotenv("DB_PASSWORD.env")
db_password = os.getenv("DB_PASSWORD")
app = Flask(__name__)
CORS(app, origins="*")
client = MongoClient(
    db_password,
    server_api=ServerApi('1'),
)
@app.route("/",methods=["GET", "POST"])
def home():
    return "Flask App is Running!", 200
#@app.route("/api/getdata",methods=["GET", "POST"])
#def login():
#    if request.method == "POST":
#        db = client["myfirst"]
#        usersdata = db["storedata"]
#        user_doc = usersdata.find_one({ "data": { "$exists": True } })
#        data = request.json
#        ##print()
#        classes = data.get("class")
#        ID = data.get("id")
#        subject = data.get("subject")
#        tries = data.get("tries")
#        classes = classes.split("/")
#        rfs = 5
#        if classes[0] in user_doc["data"]["bigdata"]:
#            ##print(1)
#            if classes[1] in user_doc["data"]["bigdata"][classes[0]]:
#                ##print(2)
#                ##print(ID)
#                if ID in user_doc["data"]["bigdata"][classes[0]][classes[1]]:
#                    ##print(3)
#        
#                    if subject in user_doc["data"]["bigdata"][classes[0]][classes[1]][ID]:
#                        ##print(4)
#                        sub:dict = user_doc["data"]["bigdata"][classes[0]][classes[1]][ID][subject]
#                        l = len(sub[f"xi {subject}"])
#                        check = {}
#                        graphtopresent = {}
#                        if int(tries) > l:
#                            return jsonify({"error": "Tries exceeds available data"}), 400
#                        for ject in sub.items():
#                            check[ject[0]] = ject[1][int(tries)-1]
#                        for ject in sub.items():
#                            graphtopresent[ject[0]] = ject[1][0:int(tries)]
#                        for ject in graphtopresent.items():
#                            ##print(len(ject[1]),(ject[1]))
#                            if len(ject[1]) - rfs +1  >= 1:
#                                for i in range(len(ject[1]) - rfs):
#                                    del graphtopresent[ject[0]][0]
#                        ##print(graphtopresent)
#                        ##print(check)
#                        
#                        totaldata= []
#                        
#                        for inxd,ject in enumerate(graphtopresent.items()):
#                            ##print(inxd)
#                            ##print(ject[0], ject[1])
#                            #print( int(tries) - rfs)
#                            store = []
#                            for inx,k in enumerate(ject[1]):
#
#                                aps = {}
#                                if int(tries) - rfs < 0:
#                                    aps["tries"] = f"สอบครั้งที่ {inx + 1}"
#                                else:
#                                    aps["tries"] = f"สอบครั้งที่ {inx + int(tries) - len(graphtopresent) + 1}"
#                                aps[[f"xi {subject}",f"percentile {subject}", f"ximax {subject}", f"xipercent {subject}", f"zscore {subject}"][inxd]] = k
#                                aps["subject"] = ject[0]
#                                store.append(aps)
#                            totaldata.append(store)
#                        
#                        ##print(totaldata)
#                            
#                        return jsonify({"message": "Data already exists","userdata":check,"totaldata":totaldata}), 200
#                    else:
#                        return jsonify({"error": "Subject not found"}), 404
#                else:
#                    return jsonify({"error": "ID not found"}), 404
#            else:
#                return jsonify({"error": "Class not found"}), 404
#        else:
#            return jsonify({"error": "Class not found"}), 404
#
#    return jsonify({"ok":True})
@app.route("/api/getdata1",methods=["GET", "POST"])
def logind():
    if request.method == "POST":
        db = client["myfirst"]
        usersdata = db["store data"]
        user_doc = usersdata.find_one({ "data": { "$exists": True } })
        data = request.json
        ##print()
        ID:str = str(data.get("id"))
        subject:str = str(data.get("subject"))
        tries:str = str(data.get("tries"))
        #print(ID,subject,tries)
        rfs = 5
        #print(2)
        if ID in user_doc["data"]["all"]["studenttdata"]:
            #print(3)
            if subject in user_doc["data"]["all"]["studenttdata"][ID]["subject"]:
                #print(4)
                sub = user_doc["data"]["all"]["studenttdata"][ID]["subject"][subject]
                #print(sub)
                witorsil = user_doc["data"]["all"]["studenttdata"][ID]["inclass"]
                l = len(sub)
                if int(tries) < 0:
                    return jsonify({"error": "Tries exceeds available data"}), 400
                if int(tries) > l :
                    return jsonify({"error": "Tries exceeds available data"}), 400
                if int(tries) > len(user_doc["data"]["all"]["totalsubjectdata"][witorsil][subject]):
                    return jsonify({"error": "Tries exceeds available data"}), 400
                st1 = user_doc["data"]["all"]["totalsubjectdata"][witorsil][subject][int(tries)-1]
                stats = user_doc["data"]["all"]["totalsubjectdata"][f"stats {witorsil}"][f"stats {subject}"][int(tries)-1]
                d = []
                
                for iD,obj in user_doc["data"]["all"]["studenttdata"].items():
                    
                    witorsils = obj["inclass"]
                    clas = obj["class"]
                    #print("-------------------------")
                    #print(obj["subject"])
                    if subject in obj["subject"]:
                        sud = obj["subject"][subject][int(tries)-1]
                        std = {}
                        if witorsil == witorsils:
                            std[iD] = sud
                            std["name"] = obj["name"]
                            std["clas"] = clas
                            print(std)
                            d.append(std)
                def get_window(data, input_index, window_size=5):
                    input_index = min(input_index, len(data))  # Clamp to list length
                    start = max(0, input_index - window_size)
                    end = input_index
                    return data[start:end]
                so = get_window(sub, int(tries),5)
                show = {
                    "xi":sub[int(tries)-1]["xi"],
                    "xipercent":sub[int(tries)-1]["xipercent"],
                    "percentile":sub[int(tries)-1]["percentile"],
                    "zscore":sub[int(tries)-1]["zscore"],
                    "rank":sub[int(tries)-1]["rank"]
                }
                st = {
                    "xi":[],
                    "xipercent":[],
                    "percentile":[],
                    "zscore":[],
                    "rank":[]
                }
                for inx,obj in enumerate(so):
                    st["xi"].append({"xi":obj["xi"],"tries":f"{inx+int(tries) - len(so)+1}"})
                    st["xipercent"].append({"xipercent":obj["xipercent"],"tries":f"{inx+int(tries) - len(so)+1}"})
                    st["percentile"].append({"percentile":obj["percentile"],"tries":f"{inx+int(tries) - len(so)+1}"})
                    st["zscore"].append({"zscore":obj["zscore"],"tries":f"{inx+int(tries) - len(so)+1}"})
                    st["rank"].append({"rank":obj["rank"],"tries":f"{inx+int(tries) - len(so)+1}"})
                flat_data = []
                for d in d:
                    for k, v in d.items():
                        if k != "name" and k != "clas":
                            flat_data.append({
                                "id": k,
                                "name": d["name"],
                                **{
                                    "xi": v["xi"],
                                    "percentile": v["percentile"],
                                    "zscore": v["zscore"],
                                    "clas": d["clas"],
                                    "xipercent": v["xipercent"],
                                }
                            })
                flat_data.sort(key=lambda x: -x["xi"])
                for idx, person in enumerate(flat_data):
                    person["rank"] = f"{idx + 1} / {len(flat_data)}"
                new_data = []
                for person in flat_data:
                    new_data.append({
                        person["id"]: {
                            "xi": person["xi"],
                            "percentile": person["percentile"],
                            "zscore": person["zscore"],
                            "rank": person["rank"],
                            "clas": person["clas"],
                            "xipercent": person["xipercent"],
                        },
                        "name": person["name"],
                    })
                #print(st)
                #print(show)
                #print(st1)
                return jsonify({"message": "Data already exists","userdata":show,"totaldata":st,"totals":st1,"stats":stats,"ximax":len(stats)-1,"cl":witorsil,"all":new_data}), 200
            else:
                #print({"error": "Subject not found"})
                return jsonify({"error": "Subject not found"}), 404
        else:
            #print({"error": "ID not found"})
            return jsonify({"error": "ID not found"}), 404

    return jsonify({"ok":True})
@app.route("/api/getdata2",methods=["GET", "POST"])
def logind2():
    if request.method == "POST":
        db = client["myfirst"]
        usersdata = db["store data"]
        user_doc = usersdata.find_one({ "data": { "$exists": True } })
        data = request.json
        ID:str = str(data.get("id"))
        subject:str = str(data.get("subject"))
        if ID in user_doc["data"]["all"]["studenttdata"]:
            if subject in user_doc["data"]["all"]["studenttdata"][ID]["subject"]:
                sub = user_doc["data"]["all"]["studenttdata"][ID]["subject"][subject]
                len(sub)
                d = [x+1 for x in range(len(sub))]
                return jsonify({"data":d})
            else:
                return jsonify({"error": "Subject not found"}), 404
        else:
            #print({"error": "ID not found"})
            return jsonify({"error": "ID not found"}), 404
    return jsonify({"error": "How?"}), 404
#limiter = Limiter(key_func=get_remote_address)
#limiter.init_app(app)
#@app.route("/api/getdata1", methods=["POST"])
##@limiter.limit("5 per minute")
#def test():
#    if request.method == "POST":
#        db = client["myfirst"]
#        usersdata = db["storedata"]
#        user_doc = usersdata.find_one({ "data": { "$exists": True } })
#        data = request.json
#        #print()
#        classes = data.get("class")
#        ID = data.get("id")
#        subject = data.get("subject")
#        tries = data.get("tries")
#        classes = classes.split("/")
#        if classes[0] in user_doc["data"]["bigdata"]:
#            #print(1)
#            if classes[1] in user_doc["data"]["bigdata"][classes[0]]:
#                #print(2)
#                #print(ID)
#                if ID in user_doc["data"]["bigdata"][classes[0]][classes[1]]:
#                    #print(3)
#        
#                    if subject in user_doc["data"]["bigdata"][classes[0]][classes[1]][ID]:
#                        #print(4)
#                        sub:dict = user_doc["data"]["bigdata"][classes[0]][classes[1]][ID][subject]
#                        return jsonify({"message": "Data already exists"}), 200
#                    else:
#                        return jsonify({"error": "Subject not found"}), 404
#                else:
#                    return jsonify({"error": "ID not found"}), 404
#            else:
#                return jsonify({"error": "Class not found"}), 404
#        else:
#            return jsonify({"error": "Class not found"}), 404
#    return jsonify({"ok":True})
#
if __name__ == "__main__":
    app.run(debug=True,port=8000)