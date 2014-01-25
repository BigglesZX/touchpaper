from .utils import (choice_prompt,
                    get_instance_types,
                    text_prompt)


def prompt_for_ami(config):
    if config and 'favourite_amis' in config and config['favourite_amis']:
        favourite_amis = ["%s: %s" % (k, v) for k, v in config['favourite_amis'].iteritems()]
        selection = choice_prompt(favourite_amis, 'Please select an AMI or enter an AMI ID:')
        if isinstance(selection, int):
            return favourite_amis[selection].split(':')[0]
        else:
            return selection
    else:
        return text_prompt('Please enter an AMI ID:')


def prompt_for_atp():
    return choice_prompt(['No', 'Yes'], 'Do you want to enable Accidental Termination Protection?')


def prompt_for_availability_zone(conn):
    available_zones = conn.get_all_zones()
    return available_zones[choice_prompt([x.name for x in available_zones], 'Please select a target availability zone:')]


def prompt_for_credentials(config):
    selection = choice_prompt([x['name'] for x in config['aws_credentials']], 'Please select a set of AWS credentials:')
    return (config['aws_credentials'][selection]['key'], config['aws_credentials'][selection]['secret'])


def prompt_for_instance_type():
    instance_types = get_instance_types()
    return instance_types[choice_prompt(instance_types, 'Please select an instance type:')]


def prompt_for_keypair(conn):
    available_keypairs = conn.get_all_key_pairs()
    if not available_keypairs:
        return False
    return available_keypairs[choice_prompt([x.name for x in available_keypairs], 'Please select a keypair:')]


def prompt_for_regions(conn):
    available_regions = conn.get_all_regions()
    return available_regions[choice_prompt([x.name for x in available_regions], 'Please select a target region:')]


def prompt_for_security_group(conn):
    # TODO: option to create new security group with sensible defaults
    available_security_groups = conn.get_all_security_groups()
    return available_security_groups[choice_prompt([x.name for x in available_security_groups], 'Please select a security group:')]


def prompt_for_storage():
    # TODO: options to instantiate new EBS volume at sensible size
    return


def prompt_for_tags():
    # TODO: load local definition of common fields to prompt for (e.g. name)
    name = text_prompt('Enter a name for the instance:')
    return {
        'Name': name,
    }
