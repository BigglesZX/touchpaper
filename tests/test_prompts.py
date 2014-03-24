import mock

from touchpaper.config import get_config


config = get_config()

SAMPLE_AMI_CONFIG = {
    "favourite_amis": {
        "ami-aa56a1dd": "Alestic - eu-west-1 - 12.04 LTS - EBS",
        "ami-3a689f4d": "Alestic - eu-west-1 - 12.04 LTS - instance store"
    }
}

SAMPLE_TAG_CONFIG = {
    "tags": [
        {
            "name": "Name"
        },
        {
            "name": "OS"
        }
    ]
}


def test_prompt_for_ami_noconfig():
    '''
    Test when called with no config, should return value from text_prompt
    '''
    with mock.patch('__builtin__.raw_input', return_value='foo'):
        from touchpaper.prompts import prompt_for_ami
        assert prompt_for_ami() == 'foo'


def test_prompt_for_ami_config_freetext():
    '''
    Test when called with config and string entered, returns string
    '''
    with mock.patch('__builtin__.raw_input', return_value='foo'):
        from touchpaper.prompts import prompt_for_ami
        config.data = SAMPLE_AMI_CONFIG
        assert prompt_for_ami() == 'foo'


def test_prompt_for_ami_config_selection():
    '''
    Test when called with config and int entered, returns matching ami entry
    '''
    with mock.patch('__builtin__.raw_input', return_value=0):
        from touchpaper.prompts import prompt_for_ami
        config.data = SAMPLE_AMI_CONFIG
        selection = prompt_for_ami()
        for k, v in config.data['favourite_amis'].iteritems():
            first = k
            break
        assert selection == k


def test_prompt_for_atp():
    '''
    Test proper conversion of 0/1 prompt into bool
    '''
    with mock.patch('__builtin__.raw_input', return_value=0):
        from touchpaper.prompts import prompt_for_atp
        assert prompt_for_atp() == False

    with mock.patch('__builtin__.raw_input', return_value=1):
        from touchpaper.prompts import prompt_for_atp
        assert prompt_for_atp() == True


def test_prompt_for_availability_zone():
    '''
    Test proper handling of availability zone list from boto
    '''
    class AvailabilityZone:
        name = "Zone"

    class Connection:
        def get_all_zones(self):
            zone1 = AvailabilityZone()
            zone1.name = 'FooZone'
            zone2 = AvailabilityZone()
            zone2.name = 'BarZone'
            return [zone1, zone2,]

    with mock.patch('__builtin__.raw_input', return_value=0):
        from touchpaper.prompts import prompt_for_availability_zone
        assert prompt_for_availability_zone(Connection()).name == 'FooZone'

    with mock.patch('__builtin__.raw_input', return_value=1):
        from touchpaper.prompts import prompt_for_availability_zone
        assert prompt_for_availability_zone(Connection()).name == 'BarZone'


def test_prompt_for_keypair():
    '''
    Test proper handling of keypair list from boto
    '''
    class Keypair:
        name = "Keypair"

    class Connection:
        def get_all_key_pairs(self):
            return []

    # test behaviour of empty keypair list
    from touchpaper.prompts import prompt_for_keypair
    assert prompt_for_keypair(Connection()) == False

    # test behaviour with non-empty list
    class Connection:
        def get_all_key_pairs(self):
            kp1 = Keypair()
            kp1.name = 'FooPair'
            kp2 = Keypair()
            kp2.name = 'BarPair'
            return [kp1, kp2,]

    with mock.patch('__builtin__.raw_input', return_value=0):
        from touchpaper.prompts import prompt_for_keypair
        assert prompt_for_keypair(Connection()).name == 'FooPair'

    with mock.patch('__builtin__.raw_input', return_value=1):
        from touchpaper.prompts import prompt_for_keypair
        assert prompt_for_keypair(Connection()).name == 'BarPair'


def test_prompt_for_region():
    '''
    Test proper handling of region list from boto
    '''
    class Region:
        name = "Region"

    class Connection:
        def get_all_regions(self):
            r1 = Region()
            r1.name = 'FooRegion'
            r2 = Region()
            r2.name = 'BarRegion'
            return [r1, r2,]

    with mock.patch('__builtin__.raw_input', return_value=0):
        from touchpaper.prompts import prompt_for_region
        assert prompt_for_region(Connection()).name == 'FooRegion'

    with mock.patch('__builtin__.raw_input', return_value=1):
        from touchpaper.prompts import prompt_for_region
        assert prompt_for_region(Connection()).name == 'BarRegion'


def test_prompt_for_security_group():
    '''
    Test proper handling of security group list from boto
    '''
    class SecurityGroup:
        name = "SecurityGroup"

    class Connection:
        def get_all_security_groups(self):
            return []

    # test behaviour of empty security group list
    from touchpaper.prompts import prompt_for_security_group
    assert prompt_for_security_group(Connection()) == False

    # test behaviour with non-empty list
    class Connection:
        def get_all_security_groups(self):
            sg1 = SecurityGroup()
            sg1.name = 'FooSecGroup'
            sg2 = SecurityGroup()
            sg2.name = 'BarSecGroup'
            return [sg1, sg2,]

    with mock.patch('__builtin__.raw_input', return_value=0):
        from touchpaper.prompts import prompt_for_security_group
        assert prompt_for_security_group(Connection()).name == 'FooSecGroup'

    with mock.patch('__builtin__.raw_input', return_value=1):
        from touchpaper.prompts import prompt_for_security_group
        assert prompt_for_security_group(Connection()).name == 'BarSecGroup'


def test_prompt_for_storage():
    '''
    Test interpretation of various inputs for storage size
    '''
    with mock.patch('__builtin__.raw_input', return_value=''):
        from touchpaper.prompts import prompt_for_storage
        assert prompt_for_storage() == False

    with mock.patch('__builtin__.raw_input', return_value='0'):
        from touchpaper.prompts import prompt_for_storage
        assert prompt_for_storage() == False

    with mock.patch('__builtin__.raw_input', return_value='8'):
        from touchpaper.prompts import prompt_for_storage
        assert prompt_for_storage() == 8


def test_prompt_for_tags():
    '''
    Test proper interpretation of tags list
    '''
    with mock.patch('__builtin__.raw_input', return_value='foo'):
        from touchpaper.prompts import prompt_for_tags
        config.data = SAMPLE_TAG_CONFIG
        tags = prompt_for_tags()
        assert 'Name' in tags
        assert 'OS' in tags
