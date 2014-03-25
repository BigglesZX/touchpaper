'''
This is the primary touchpaper module; the `main` function is called when you
run `touchpaper` on the command line.
'''

import boto.ec2
import sys

from boto.ec2 import EC2Connection
from colorama import init, Fore
from os import environ
from time import sleep

from ._version import get_version
from .config import get_config
from .instance import Instance
from .prompts import *
from .utils import get_argument_parser, choice_prompt


config = get_config()


'''
Main package routine

Pulls it all together. Initiates various prompts to the user to build an EC2
API query to launch an instance.
'''
def main():
    ''' Colorama init '''
    init(autoreset=True)

    ''' Argument parser init '''
    parser = get_argument_parser()
    args = parser.parse_args()

    if args.version:
        print "touchpaper v%s" % get_version()
        sys.exit(0)

    if args.dry_run:
        print Fore.YELLOW + "Warning: dry-run mode is active"

    ''' Retrieve and check config object and warn if env vars aren't set '''
    global config
    config.load(location_override=args.config_file_location)
    if config.data is False and (config.AWS_KEY_ENV_VAR not in environ or config.AWS_SECRET_ENV_VAR not in environ):
        print Fore.RED + "Error: you're not using %s, so you need to configure the %s and %s variables in your environment." % (config.RC_FILE_NAME, config.AWS_KEY_ENV_VAR, config.AWS_SECRET_ENV_VAR)
        sys.exit(1)

    ''' Set up initial EC2 connection '''
    if config.data:
        key, secret = prompt_for_credentials()
        conn = EC2Connection(key, secret)
    else:
        print Fore.YELLOW + "Using AWS credentials from environment"
        conn = EC2Connection()

    ''' Instantiate instance '''
    instance = Instance(args.dry_run)

    instance.region = prompt_for_region(conn)

    ''' Establish region using selected credentials, or default to environment
    variables '''
    if config.data:
        conn = boto.ec2.connect_to_region(instance.region.name, aws_access_key_id=key, aws_secret_access_key=secret)
    else:
        conn = boto.ec2.connect_to_region(instance.region.name)

    instance.set_conn(conn)

    instance.availability_zone = prompt_for_availability_zone(conn)

    instance.ami = prompt_for_ami()

    instance.instance_type = prompt_for_instance_type()

    instance.atp = prompt_for_atp()

    storage_size = prompt_for_storage()
    if storage_size:
        '''
        If a storage size was specified, prompt for the name to assign to the
        volume and set up the EC2 BlockDeviceMapping ready to attach it to the
        instance at launch (source: http://stackoverflow.com/a/13604274/258794)
        '''
        storage_name = prompt_for_storage_name()

        dev_sda1 = boto.ec2.blockdevicemapping.EBSBlockDeviceType()
        dev_sda1.size = storage_size
        bdm = boto.ec2.blockdevicemapping.BlockDeviceMapping()
        bdm['/dev/sda1'] = dev_sda1

        instance.storage_size = storage_size
        instance.storage_name = storage_name

    instance.keypair = prompt_for_keypair(conn)
    if instance.keypair is False:
        print Fore.RED + "Warning: no keypairs found on account, you will not be able to SSH into the new instance"

    instance.security_group = prompt_for_security_group(conn)
    if instance.security_group is False:
        print Fore.RED + "Warning: no security groups found on account, you will not be able to access the new instance via the network"

    if config.data and 'tags' in config.data:
        instance.tags = prompt_for_tags()
    else:
        print Fore.YELLOW + "Warning: no tags defined in config"

    ''' Regurgitate selected parameters for user confirmation '''
    print Fore.GREEN + "\nReady to launch instance. You selected the following:"
    print "Region: %s" % instance.region.name
    print "Availability zone: %s" % instance.availability_zone.name
    print "AMI: %s" % instance.ami
    print "Instance type: %s" % instance.instance_type
    print "Accidental termination protection: %s" % ("Yes" if instance.atp else "No")
    print "Storage: %s" % (('%dGB EBS' % instance.storage_size) if instance.storage_size else "None")
    print "Keypair: %s" % (instance.keypair.name if instance.keypair else "None")
    print "Security group: %s" % instance.security_group.name
    if instance.tags:
        print "Tags:"
        for tag, value in instance.tags.iteritems():
            print '- "%s": "%s"' % (tag, value)

    if not bool(choice_prompt(['No', 'Yes'], 'Are these details correct?')):
        print Fore.YELLOW + "Quitting"
        sys.exit(0)

    print Fore.CYAN + "Launching instance..."

    instance.run()

    ''' That's it! '''
    print "Done."


if __name__ == '__main__':
    main()
