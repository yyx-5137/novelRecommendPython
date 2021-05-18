# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json
import _thread
import learning
import pandas as pd

hostName = "localhost"
serverPort = 8081
WriteInfo = "/doRate"
GetTop10 = "/getTop10"
GetRate = "/getRate"
predictlist = []
times = 0
novels_df = pd.read_csv('ml-latest-small/novels.csv')
ratings_df = pd.read_csv('ml-latest-small/ratings.csv')
class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        print("Get "+self.path)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))
    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        if self.path==WriteInfo:
            WriteNum(self)
        elif self.path==GetTop10:
            GetTop(self)
        elif self.path==GetRate:
            getRateById(self)
        else:
            python2json = {}
            python2json["1"] = "2"
            self.wfile.write(bytes(json.dumps(python2json), "utf-8"))
def WriteNum(this):
    content_length = int(this.headers['Content-Length'])
    post_data = this.rfile.read(content_length)# res bytes
    myjs = post_data.decode('utf8')
    data = json.loads(myjs) # dict
    #
    uid = data['userId']
    nid = data['novelId']
    rate = data['rating']
    print(uid,nid,rate)
    # write to file 
    with open("ml-latest-small/ratings.csv", encoding="utf-8",mode="a") as file:  
        file.write(str(uid)+","+str(nid)+","+str(rate)+",8123618128")
    res = {}
    res["msg"] = "OK"
    this.wfile.write(bytes(json.dumps(res), "utf-8"))
def GetTop(this):
    content_length = int(this.headers['Content-Length'])
    post_data = this.rfile.read(content_length)# res bytes
    myjs = post_data.decode('utf8')
    data = json.loads(myjs) # dict
    print(data)
    user_id = data["userId"]
    predicts = predictlist[0]
    sortedResult = predicts[:, int(user_id)].argsort()[::-1]
    resList = []
    idx = 0
    for i in sortedResult:
        idx+=1
        resList.append(int(novels_df.iloc[i]['novelId']))
        if idx == 10: break
    res = {}
    res["msg"] = resList
    this.wfile.write(bytes(json.dumps(res), "utf-8"))

def getRateById(this):
    content_length = int(this.headers['Content-Length'])
    post_data = this.rfile.read(content_length)# res bytes
    myjs = post_data.decode('utf8')
    data = json.loads(myjs) # dict
    print(data)
    user_id = data["userId"]
    novel_id = data["novelId"]
    rate_csv = pd.read_csv('ml-latest-small/ratings.csv')
    rateLine = rate_csv[(rate_csv.userId==14)&(rate_csv.novelId==1)]
    res = {}
    if rateLine.empty:
        res["msg"] = 0
    else :
        res["msg"] = int(rateLine["rating"])
    this.wfile.write(bytes(json.dumps(res), "utf-8"))
def delayLearn(delay,predictlist):
    while True:
        predictlist[0] = learning.learning()
        time.sleep(delay)
if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))
    predictlist = []
    predictlist.append(None)
    try:
        _thread.start_new_thread( delayLearn, ( 30, predictlist,) )
    except:
        print ("Error: 无法启动线程")
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
