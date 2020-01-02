import os
import urllib
import requests
import logging
import json


class bam_api:
    history=[]
    account=""
    password=""
    header=""
    hostname=""
    loglevel = ""



    def __init__(self,loglevel = "CRITICAL",creds=None):
        self.loglevel = loglevel
        bam_creds=None

        if creds:
            bam_creds=self.load_creds(creds)
            
        if bam_creds:
            self.account  = bam_creds['bluecat']['account']
            self.password = bam_creds['bluecat']['password']
            self.hostname = bam_creds['bluecat']['hostname']
            self.secure   = bam_creds['bluecat']['secure']
        else:
            self.account  = os.environ['BAM_ACCOUNT']
            self.password = os.environ['BAM_PASSWORD']
            self.hostname = os.environ['BAM_HOSTNAME']
            if os.environ['BAM_SECURE'] !=None and lower(os.environ['BAM_SECURE'])=='true':
                 self.secure=True
            else:
                self.secure=None

        self.main_url      = self.hostname+"Services/REST/v1/"
        self.getsysinfourl = self.main_url+"getSystemInfo?"
        self.logout_url    = self.main_url+"logout?"
        self.login_url     = self.main_url+ "login?"+urllib.parse.urlencode({"username":self.account,"password":self.password})


        self.logger = self.set_loglevel('ipam-o-nator', loglevel)
        self.py_logger = self.set_loglevel('py.warnings', loglevel)
        self.session = self.init_session()
        
        if self.secure:
            host="https://{0}".format(self.hostname)
        else:
            host="http://{0}".format(self.hostname)

        self.baseUrl = '{0}/Services/REST/v1/'.format(host)

        if all(param is not None for param in [self.hostname, self.account, self.password]):
            self.login()
            self.config = self.getConfigs()
            #print(self.config)
        else:
            self.config = None

    
    def load_creds(self,cred_file):
        try:
            with open(cred_file) as json_file:
                data = json.load(json_file)
            return data
        except Exception as ex:
            print(ex)
            return None


    # decorator
    def rest_call(httpMethod):
        def outer(func):
            def inner(self, *args, **kwargs):
                method, params, data = func(self, *args, **kwargs)
                url = self.baseUrl + method
                methodMap = {
                    'delete': self.session.delete,
                    'get': self.session.get,
                    'post': self.session.post,
                    'put': self.session.put
                }
                response = methodMap[httpMethod](url, params=params, json=data)
                self.logger.debug('Request URL: {}'.format(response.request.url))
                self.logger.debug('Response Code: {}'.format(response.status_code))
                self.lastCall = response
                self.history.append(response)
                # Handle non-200 responses
                if response.status_code != 200:
                    raise Exception (response)
                try:
                    data = response.json()
                    self.logger.debug('Response Body: {}'.format(json.dumps(data, indent=2, sort_keys=True)))
                except Exception:
                    data = response.content
                    self.logger.debug('Response Body: {}'.format(data))
                return data
            return inner
        return outer


    def login2(self):
        
        print( self.login_url)
        response = requests.get(self.login_url)
        token = str(response.json())
        token = token.split()[2]+" "+token.split()[3]
        header={'Authorization':token,'Content-Type':'application/json'}
        print(response.json())



    def init_session(self, proxies={'http': None, 'https': None},
                     headers={'Content-Type': 'application/json'},
                     ssl_verify=False):
        session = requests.Session()
        session.proxies.update(proxies)
        session.headers.update(headers)
        session.verify = ssl_verify
        if not ssl_verify:
            logging.captureWarnings(True)
        return session

    def set_loglevel(self, logger_name, loglevel):
        logger = logging.getLogger(logger_name)
        loglevel = loglevel.upper()
        if loglevel in ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']:
            level = getattr(logging, loglevel)
            # logging.basicConfig(level=level)
            logger.setLevel(level=level)
        console_handler = logging.StreamHandler()
        logger.addHandler(console_handler)
        return logger

    @rest_call('get')
    def get_entity_by_name(self, parentId, name, objType):
        method = 'getEntityByName'
        params = {
            'parentId': parentId,
            'name': name,
            'type': objType
        }
        data = None
        return method, params, data

    @rest_call('get')
    def get_networks(self, parent_id, start=0, count=1000):
        return self.get_entities(parent_id, 'IP4Network', start, count)

    @rest_call('get')
    def get_entities(self, parent_id, obj_type, start=0, count=1000):
        method = 'getEntities'
        params = {
            'parentId': parent_id,
            'type': obj_type,
            'start': start,
            'count': count
        }
        data = None
        return method, params, data

    @rest_call('get')
    def get_entity_by_id(self, entityId):
        method = 'getEntityById'
        params = {
            'id': entityId
        }
        data = None
        return method, params, data

    @rest_call('get')
    def get_linked_entities(self, entityId, linkedType='IP4Address', start=0, count=100):
        method = 'getLinkedEntities'
        params = {
            'entityId': entityId,
            'type': linkedType,
            'start': start,
            'count': count
        }
        data = None
        return method, params, data

    @rest_call('delete')
    def delete(self, entity_id):
        method = 'delete'
        params = {
            'objectId': entity_id
        }
        data = None
        return method, params, data

    @rest_call('put')
    def update(self, entity):
        method = 'update'
        params = None
        data = entity
        return method, params, data


    def login(self):
        method = 'login'
        params = {
            'username': self.account,
            'password': self.password
        }
        try:
            response = self.session.get(self.baseUrl + method, params=params)
            self.logger.info(response.content)
            authToken = response.text.split('-> ')[1].split(' <-')[0]
            self.session.headers.update({'Authorization': str(authToken)})
            return response
        except Exception as ex:
            self.logger.error('ERROR: '+ex)
            self.logger.error('ERROR: Login Failed')
            raise Exception("Error Logging in"+str(ex))

    @rest_call('get')
    def logout(self):
        method = 'logout'
        params = None
        data = None
        return method, params, data


    @rest_call('get')
    def get_entity_by_cidr(self, parent_id, cidr, objType):
        """config.id only works for top-level blocks, parent_id must literally be the parent obect's id"""
        method = 'getEntityByCIDR'
        params = {
            'parentId': parent_id,
            'cidr': cidr,
            'type': objType
        }
        data = None
        return method, params, data

    def get_network_by_cidr(self, parent_id, cidr):
        return self.get_entity_by_cidr(parent_id, cidr, 'IP4Network')

    def get_block_by_cidr(self, parent_id, cidr):
        return self.get_entity_by_cidr(parent_id, cidr, 'IP4Block')

    @rest_call('get')
    def get_ip_ranged_by_ip(self, parentId, ipAddr, objType):
        method = 'getIPRangedByIP'
        params = {
            'containerId': parentId,
            'type': objType,
            'address': ipAddr.split('/')[0]
        }
        data = None
        return method, params, data

    def get_network(self, netAddr):
        return self.get_ip_ranged_by_ip(self.config['id'], netAddr, 'IP4Network')

    def get_network_by_ip(self, netAddr):
        return self.get_ip_ranged_by_ip(self.config['id'], netAddr, 'IP4Network')

    def get_block_by_ip(self, netAddr):
        return self.get_ip_ranged_by_ip(self.config['id'], netAddr, 'IP4Block')

    def get_dhcp_scope_by_ip(self, netAddr):
        return self.get_ip_ranged_by_ip(self.config['id'], netAddr, 'DHCP4Range')



    def getConfig(self):
        return self.get_entity_by_name(0, '', 'Configuration')

    def getConfigs(self):
        config=self.get_entities(0,"Configuration")
        print (config)
        res=self.get_entity_by_id(1)
        print(res)
        return config
        #return self.get_entities(0,"Configuration")

