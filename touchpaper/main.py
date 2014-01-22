import boto.ec2
import os
import sys
from .utils import choice_prompt, text_prompt


# TODO: use boto's own env vars
AWS_KEY = os.environ['TOUCHPAPER_AWS_KEY']
AWS_SECRET = os.environ['TOUCHPAPER_AWS_SECRET']

# TODO: save this somewhere useful
DEFAULT_AMI = 'ami-66ef0111'

INSTANCE_TYPES = [
    "t1.micro",
    "m1.small",
    "m1.medium",
    "m1.large",
    "m1.xlarge",
    "m3.xlarge",
    "m3.2xlarge",
    "c1.medium",
    "c1.xlarge",
    "m2.xlarge",
    "m2.2xlarge",
    "m2.4xlarge",
    "cr1.8xlarge",
    "hi1.4xlarge",
    "hs1.8xlarge",
    "cc1.4xlarge",
    "cg1.4xlarge",
    "cc2.8xlarge",
    "g2.2xlarge",
    "c3.large",
    "c3.xlarge",
    "c3.2xlarge",
    "c3.4xlarge",
    "c3.8xlarge",
    "i2.xlarge",
    "i2.2xlarge",
    "i2.4xlarge",
    "i2.8xlarge",
]


def prompt_for_ami():
    # TODO: read from local list of favourite AMIs
    return text_prompt('Please enter an AMI ID:')


def prompt_for_atp():
    return choice_prompt(['No', 'Yes'], 'Do you want to enable Accidental Termination Protection?')


def prompt_for_availability_zone(conn):
    available_zones = conn.get_all_zones()
    return available_zones[choice_prompt([x.name for x in available_zones], 'Please select a target availability zone:')]


def prompt_for_instance_type():
    return INSTANCE_TYPES[choice_prompt(INSTANCE_TYPES, 'Please select an instance type:')]


def prompt_for_keypair(conn):
    # TODO: deal with lack of keypairs on account
    available_keypairs = conn.get_all_key_pairs()
    return available_keypairs[choice_prompt([x.name for x in available_keypairs], 'Please select a keypair:')]


def prompt_for_regions():
    available_regions = boto.ec2.regions(aws_access_key_id=AWS_KEY, aws_secret_access_key=AWS_SECRET)
    return available_regions[choice_prompt([x.name for x in available_regions], 'Please select a target region:')]


def prompt_for_security_group(conn):
    # TODO: option to create new security group with sensible defaults
    available_security_groups = conn.get_all_security_groups()
    return available_security_groups[choice_prompt([x.name for x in available_security_groups], 'Please select a security group:')]


def prompt_for_storage():
    # TODO: options to instantiate new EBS volume at sensible size
    return


def prompt_for_user_data():
    # TODO: load local definition of common fields to prompt for (e.g. name)
    return


def main():
    if 'TOUCHPAPER_AWS_KEY' not in os.environ or 'TOUCHPAPER_AWS_SECRET' not in os.environ:
        print "Please ensure you have configured the TOUCHPAPER_AWS_KEY and TOUCHPAPER_AWS_SECRET variables in your environment."
        sys.exit(1)
    
    region = prompt_for_regions()
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
