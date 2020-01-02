import json
from  .bam_api import bam_api


cred_file='/home/cwatkin1/repos/chris17453/ipam-o-nator/creds.json'

bam=bam_api(creds=cred_file)
bam.login()