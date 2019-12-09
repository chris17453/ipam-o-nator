import os

class bam_api:
    account=""
    account_password=""
    header=""


    def __init__(self,url=None,account=None,password=None):
        if account:
            self.account  = account
            self.password = password
            self.url      = url
        else:
            self.account  = os.environ['BAM_ACCOUNT']
            self.password = os.environ['BAM_PASSWORD']
            self.url      = os.environ['BAM_URL']

        self.main_url      = self.bam_url+"/Services/REST/v1/"
        self.getsysinfourl = self.main_url+"getSystemInfo?"
        self.logout_url    = self.main_url+"logout?"
        self.login_url     = self.main_url+"login?username="+self.account+"&password="+self.account_password

    def login(self):
        
        response = requests.get(self.login_url)
        token = str(response.json())
        token = token.split()[2]+" "+token.split()[3]
        header={'Authorization':token,'Content-Type':'application/json'}
        print(response.json())





