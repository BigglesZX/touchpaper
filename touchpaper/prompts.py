from .utils import (choice_prompt,
                    get_instance_types,
                    text_prompt)


def prompt_for_ami():
    # TODO: read from local list of favourite AMIs
    return text_prompt('Please enter an AMI ID:')


def prompt_for_atp():
    return choice_prompt(['No', 'Yes'], 'Do you want to enable Accidental Termination Protection?')


def prompt_for_availability_zone(conn):
    available_zones = conn.get_all_zones()
    return available_zones[choice_prompt([x.name for x in available_zones], 'Please select a target availability zone:')]


def prompt_for_instance_type():
    instance_types = get_instance_types()
    return instance_types[choice_prompt(instance_types, 'Please select an instance type:')]


def prompt_for_keypair(conn):
    # TODO: deal with lack of keypairs on account
    available_keypairs = conn.get_all_key_pairs()
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


def prompt_for_user_data():
    # TODO: load local definition of common fields to prompt for (e.g. name)
    return
