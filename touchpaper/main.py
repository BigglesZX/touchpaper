import boto.ec2
import json
import sys
from boto.ec2 import EC2Connection
from os import environ, getcwd
from os.path import exists, expanduser, join
from .prompts import *


RC_FILE_NAME = '.touchpaperrc'
AWS_KEY_ENV_VAR = 'AWS_ACCESS_KEY_ID'
AWS_SECRET_ENV_VAR = 'AWS_SECRET_ACCESS_KEY'


def main():
    local_config_path = join(getcwd(), RC_FILE_NAME)
    home_config_path = join(expanduser('~'), RC_FILE_NAME)
    config_path = False
    config = False
    
    if exists(local_config_path):
        config_path = local_config_path
    elif exists(home_config_path):
        config_path = home_config_path
    
    if config_path:
        with open(config_path) as f:
            config = json.load(f)
        
    if config is False and (AWS_KEY_ENV_VAR not in environ or AWS_SECRET_ENV_VAR not in environ):
        print "You're not using the %s config file, so please ensure you have configured the %s and %s variables in your environment." % (RC_FILE_NAME, AWS_KEY_ENV_VAR, AWS_SECRET_ENV_VAR)
        sys.exit(1)
    
    if config:
        key, secret = prompt_for_credentials(config)
        conn = EC2Connection(key, secret)
    else:
        print "Using AWS credentials from environment"
        conn = EC2Connection()
    
    region = prompt_for_regions(conn)
    print region
    
    if config:
        conn = boto.ec2.connect_to_region(region.name, aws_access_key_id=key, aws_secret_access_key=secret)
    else:
        conn = boto.ec2.connect_to_region(region.name)
    
    availability_zone = prompt_for_availability_zone(conn)
    print availability_zone
    
    ami = prompt_for_ami()
    print ami
    
    instance_type = prompt_for_instance_type()
    print instance_type
    
    atp = prompt_for_atp()
    print atp
    
    storage = prompt_for_storage()
    print storage
    
    keypair = prompt_for_keypair(conn)
    print keypair
    
    security_group = prompt_for_security_group(conn)
    print security_group
    
    user_data = prompt_for_user_data()
    print user_data
    
    # TODO: launch the instance :)
