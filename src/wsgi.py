import os
import requests, json
from flask import Flask, request, send_from_directory
app = Flask(__name__, static_url_path='')

# https://github.com/bluecatlabs/making-apis-work-for-you/


# Account id stuff...
bam_account =os.environ['BAM_ACCOUNT']
bam_password = os.environ['BAM_PASSWORD']
bam_url = os.environ['BAM_URL']

main_url = "http://"+bam_url+"/Services/REST/v1/"
getsysinfourl = main_url+"getSystemInfo?"
logout_url = main_url+"logout?"

# getEntityByName method
e_parentId=0
e_name=""
e_type=""
getEntityByName = mainurl+"getEntityByName?parentId="+ str(e_parentId) \
                        +"&name="+e_name+"&type="+e_type

# getEntityById
e_id=0
getEntityById = mainurl+"getEntityById?id="+str(e_id)
# addHostRecord
r_viewId = 0
r_absoluteName=""
r_addresses = ""
r_ttl=""
r_properties=""
addHostRecord = mainurl+"addHostRecord?viewId="+str(r_viewId)+"&absoluteName=" \
                +r_absoluteName+"&addresses="+r_addresses+ \
                "&ttl="+r_ttl+"&properties="+r_properties

# addAliasRecord
r_linkedRecordName=""
addAliasRecord = mainurl+"addAliasRecord?viewId="+str(r_viewId)+"&absoluteName=" \
                    +r_absoluteName+"&linkedRecordName="+r_linkedRecordName+ \
                    "&ttl="+r_ttl+"&properties="+r_properties





@app.route('/')
def root():
    return app.send_static_file('pages/home.html')

@app.route('/media/<path:path>')
def send_js(path):
    return send_from_directory('static', path)    




@app.route('/logout')
def logout():
    response=requests.get(logout_url,headers=header)
    session['loggedin']=None
    return response.json()

@app.route('/login')
def login():
    login_url = main_url+"login?username="+bam_account+"&password="+account_password

    response = requests.get(login_url)
    token = str(response.json())
    token = token.split()[2]+" "+token.split()[3]
    header={'Authorization':token,'Content-Type':'application/json'}

    session['loggedin']=token

    return response.json()

@app.route('/bulk_export')
def bulk_export():
    pass

@app.route('/bulk_import')
def bulk_import():
    pass

@app.route('/validate')
def validate():
    pass

# BLOCK MANAGMENT
@app.route('/create_block')
def create_block():
    pass

@app.route('/delete_block')
def delete_block():
    pass

@app.route('/update_block')
def update_block():
    pass

@app.route('/read_block')
def read_block():
    pass

@app.route('/assign_block')
def assign_block():
    pass

@app.route('/unassign_block')
def unassign_block():
    pass


# SUBNET MANAGMENT
@app.route('/create_subnet')
def create_subnet():
    pass

@app.route('/delete_subnet')
def delete_subnet():
    pass

@app.route('/update_subnet')
def update_subnet():
    pass

@app.route('/read_subnet')
def read_subnet():
    pass


if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0',
        port=8080
    )
