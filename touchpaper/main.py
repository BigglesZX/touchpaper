import argparse
import boto.ec2
import sys
from boto.ec2 import EC2Connection
from os import environ
from time import sleep
from .prompts import *
from .utils import choice_prompt, find_config


RC_FILE_NAME = '.touchpaperrc'
AWS_KEY_ENV_VAR = 'AWS_ACCESS_KEY_ID'
AWS_SECRET_ENV_VAR = 'AWS_SECRET_ACCESS_KEY'
RUNNING_STATE = 'running'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', dest='dry_run', action='store_true')
    args = parser.parse_args()
    
    if args.dry_run:
        print "Dry-run mode is active"
    
    config = find_config()        
    if config is False and (AWS_KEY_ENV_VAR not in environ or AWS_SECRET_ENV_VAR not in environ):
        print "You're not using %s, so you need to configure the %s and %s variables in your environment." % (RC_FILE_NAME, AWS_KEY_ENV_VAR, AWS_SECRET_ENV_VAR)
        sys.exit(1)
    
    if config:
        key, secret = prompt_for_credentials(config)
        conn = EC2Connection(key, secret)
    else:
        print "Using AWS credentials from environment"
        conn = EC2Connection()
    
    region = prompt_for_regions(conn)
    
    if config:
        conn = boto.ec2.connect_to_region(region.name, aws_access_key_id=key, aws_secret_access_key=secret)
    else:
        conn = boto.ec2.connect_to_region(region.name)
    
    availability_zone = prompt_for_availability_zone(conn)
    
    ami = prompt_for_ami(config)
    
    instance_type = prompt_for_instance_type()
    
    atp = bool(prompt_for_atp())
    
    storage = prompt_for_storage()
    
    keypair = prompt_for_keypair(conn)
    if keypair is False:
        print "Warning: no keypairs found on account, you will not be able to SSH into the new instance"
    
    security_group = prompt_for_security_group(conn)
    
    tags = prompt_for_tags()
    
    print "Ready to launch instance. You selected the following:"
    print "Region: %s" % region.name
    print "Availability zone: %s" % availability_zone.name
    print "AMI: %s" % ami
    print "Instance type: %s" % instance_type
    print "Accidental termination protection: %s" % ("Yes" if atp else "No")
    #print "Storage: %s" % storage
    print "Keypair: %s" % (keypair if keypair else "None")
    #print "Security group: %s" % security_group.name
    print "Tags: %s" % tags
    
    if not bool(choice_prompt(['No', 'Yes'], 'Is this correct?')):
        sys.exit(0)
        
    print "Launching instance..."
    
    reservation = conn.run_instances(image_id=ami,
                                     key_name=keypair,
                                     security_groups=[security_group.name,],
                                     instance_type=instance_type,
                                     placement=availability_zone.name,
                                     #block_device_map=storage,
                                     disable_api_termination=atp,
                                     dry_run=args.dry_run)
    instance = reservation.instances[0]
    
    while instance.state != RUNNING_STATE:
        print "Instance state: %s ..." % instance.state
        sleep(5)
        instance.update()
    print "Instance running! ID: %s; public DNS: %s" % (instance.id, instance.public_dns_name)
    
    if tags:
        for tag, value in tags.iteritems():
            instance.add_tag(tag, value)
        print "Tags added"
    
    print "Done."
    

if __name__ == '__main__':
    main()