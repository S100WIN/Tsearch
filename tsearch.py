import sys
import requests
from bs4 import BeautifulSoup

class Tsearch():
    def __init__(self):
        self.validArgumentList = ['--nocss','-w','-u','-r','-o','-d','-v','-h','--help']
        self.keyList= ["key","api","secret","password","username","config","document.location","url","postmessage"
                       ,"innerhtml","eval(","document.write","location.href","document.url","document.cookies"
                       ,"navigation.referrer","window.name","settimeout","setinterval","location.assign"
                       ,"admin","token","permission","client","host","portal","auth","jwt","bearer","ssrf","https://"
                       ,"graphql","port","xml","sql","route","JSON.stringify"]
        self.setArgument()     
        print("\n***************************************")
    def makeRequest(self,url):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 OPR/99.0.0.0'
            }
            self.response = requests.get(url,headers=headers)
        except:
            print("Error occurred by finding domain! Please check the url and try again. ")
            sys.exit()
        self.response.raw
        self.soup = BeautifulSoup(self.response.text,"html.parser") 
    def searchUrl(self):
        string = f"{self.response.url} -->  "
        zero = 0
        for n in self.keyList:
            if n in self.response.text.lower():
                if zero == 0:
                    string = string + n
                    zero = 1
                else:
                    string = string + "," + n
        if zero == 0:
            string = string + "NONE"
        print(string)
    def scrapeEndpoints(self):
        list = []
        link = self.soup.findAll("script") 
        for  n in link:
            src = n.get("src")
            if src == None:
                continue
            if  not "http" in src: 
                list.append(self.core+src)
        if self.nocss == False:
            relLinks = link = self.soup.findAll("link")
            for  n in relLinks:
                href = n.get("href")
                if href == None:
                    continue
                if  not "http" in href: 
                    list.append(self.core+href)
        return list
    def setArgument(self):
        validCount = 0
        self.nocss = False
        if len(sys.argv) == 1:
            self.help()
            sys.exit()
        else:
            count = 0
            for arg in sys.argv:
                if arg in self.validArgumentList:
                    try:
                        match arg:
                            case "-w":
                                self.w = sys.argv[count+1]
                            case "-u":
                                self.u = sys.argv[count+1]
                                a = self.u.split("/")
                                self.core = f"{a[0]}/{a[1]}/{a[2]}/"
                            case "-r":
                                self.r = sys.argv[count+1]
                            case "-o":
                                self.o = sys.argv[count+1]
                            case "--nocss":
                                self.nocss = True
                            case "-d":
                                self.d = sys.argv[count+1]
                            case "-v":
                                self.v = sys.argv[count+1]
                            case "-h":
                                self.help()
                            case "--help":
                                self.help()  
                        validCount += 1  
                    except:
                        validCount = 0  
                count += 1         
            if validCount == 0:
                print("Please enter the valid arguments. (use --help or -h)")
                sys.exit()
    def help(self):
        print("""///////////////////--------\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
Welcome to the Tsearch. Lets Fun!

Arguments              Description

-w                      Has a url contains wordlists which seperate per line
-u                      Url: https://example.com/      
-r                      Set redirect enabled (Default: false)
-o                      Set a output file
-d                      Debug mode on
-v                      Set verbose mode true (Default: false)
--nocss                 For the not searching css file 
-h / --help             Help

Example
              
python3 tsearch.py -u https://www.example.com
        """)

tsearch = Tsearch()
tsearch.makeRequest(tsearch.u)
tsearch.searchUrl()
endpoints = tsearch.scrapeEndpoints()
if endpoints:
    for endpoint in endpoints:
        tsearch.makeRequest(endpoint)
        tsearch.searchUrl()       


