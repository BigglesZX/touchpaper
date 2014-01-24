import boto.ec2
import os
import sys
from boto.ec2 import EC2Connection
from .prompts import *


# TODO: use boto's own env vars
AWS_KEY = os.environ['TOUCHPAPER_AWS_KEY']
AWS_SECRET = os.environ['TOUCHPAPER_AWS_SECRET']

# TODO: save this somewhere useful
DEFAULT_AMI = 'ami-66ef0111'


def main():
    if 'TOUCHPAPER_AWS_KEY' not in os.environ or 'TOUCHPAPER_AWS_SECRET' not in os.environ:
        print "Please ensure you have configured the TOUCHPAPER_AWS_KEY and TOUCHPAPER_AWS_SECRET variables in your environment."
        sys.exit(1)
    
    conn = EC2Connection(AWS_KEY, AWS_SECRET)
    
    region = prompt_for_regions(conn)
    print region

    conn = boto.ec2.connect_to_region(region.name, aws_access_key_id=AWS_KEY, aws_secret_access_key=AWS_SECRET)
    
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
