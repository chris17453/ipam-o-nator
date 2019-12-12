import json
from  .bam_api import bam_api


cred_file='creds.json'

bam=bam_api(creds=cred_file)
bam.login()