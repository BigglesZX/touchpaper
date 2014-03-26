import mock

from touchpaper.config import get_config
from touchpaper.instance import Instance


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
    instance = Instance()
    with mock.patch('__builtin__.raw_input', return_value='foo'):
        from touchpaper.prompts import prompt_for_ami
        prompt_for_ami(instance)
        assert instance.ami == 'foo'


def test_prompt_for_ami_config_freetext():
    '''
    Test when called with config and string entered, returns string
    '''
    instance = Instance()
    with mock.patch('__builtin__.raw_input', return_value='foo'):
        from touchpaper.prompts import prompt_for_ami
        config.data = SAMPLE_AMI_CONFIG
        prompt_for_ami(instance)
        assert instance.ami == 'foo'


def test_prompt_for_ami_config_selection():
    '''
    Test when called with config and int entered, returns matching ami entry
    '''
    instance = Instance()
    with mock.patch('__builtin__.raw_input', return_value=0):
        from touchpaper.prompts import prompt_for_ami
        config.data = SAMPLE_AMI_CONFIG
        prompt_for_ami(instance)
        for k, v in config.data['favourite_amis'].iteritems():
            first = k
            break
        assert instance.ami == k


def test_prompt_for_atp():
    '''
    Test proper conversion of 0/1 prompt into bool
    '''
    with mock.patch('__builtin__.raw_input', return_value=0):
        instance = Instance()
        from touchpaper.prompts import prompt_for_atp
        prompt_for_atp(instance)
        assert instance.atp == False

    with mock.patch('__builtin__.raw_input', return_value=1):
        instance = Instance()
        from touchpaper.prompts import prompt_for_atp
        prompt_for_atp(instance)
        assert instance.atp == True


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
        instance = Instance()
        instance.conn = Connection()
        prompt_for_availability_zone(instance)
        assert instance.availability_zone.name == 'FooZone'

    with mock.patch('__builtin__.raw_input', return_value=1):
        from touchpaper.prompts import prompt_for_availability_zone
        instance = Instance()
        instance.conn = Connection()
        prompt_for_availability_zone(instance)
        assert instance.availability_zone.name == 'BarZone'


def test_prompt_for_keypair():
    '''
    Test proper handling of keypair list from boto
    '''
    class Keypair:
        name = "Keypair"

    class Connection:
        def get_all_key_pairs(self):
            return []

    instance = Instance()

    # test behaviour of empty keypair list
    from touchpaper.prompts import prompt_for_keypair
    instance.conn = Connection()
    prompt_for_keypair(instance)
    assert instance.keypair == None

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
        instance.conn = Connection()
        prompt_for_keypair(instance)
        assert instance.keypair.name == 'FooPair'

    with mock.patch('__builtin__.raw_input', return_value=1):
        from touchpaper.prompts import prompt_for_keypair
        instance.conn = Connection()
        prompt_for_keypair(instance)
        assert instance.keypair.name == 'BarPair'


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
        instance = Instance()
        instance.conn = Connection()
        prompt_for_region(instance)
        assert instance.region.name == 'FooRegion'

    with mock.patch('__builtin__.raw_input', return_value=1):
        from touchpaper.prompts import prompt_for_region
        instance = Instance()
        instance.conn = Connection()
        prompt_for_region(instance)
        assert instance.region.name == 'BarRegion'


def test_prompt_for_security_group():
    '''
    Test proper handling of security group list from boto
    '''
    class SecurityGroup:
        name = "SecurityGroup"

    class Connection:
        def get_all_security_groups(self):
            return []

    instance = Instance()

    # test behaviour of empty security group list
    from touchpaper.prompts import prompt_for_security_group
    instance.conn = Connection()
    prompt_for_security_group(instance)
    assert instance.security_group == None

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
        instance.conn = Connection()
        prompt_for_security_group(instance)
        assert instance.security_group.name == 'FooSecGroup'

    with mock.patch('__builtin__.raw_input', return_value=1):
        from touchpaper.prompts import prompt_for_security_group
        instance.conn = Connection()
        prompt_for_security_group(instance)
        assert instance.security_group.name == 'BarSecGroup'


def test_prompt_for_storage():
    '''
    Test interpretation of various inputs for storage size
    '''
    with mock.patch('__builtin__.raw_input', return_value=''):
        from touchpaper.prompts import prompt_for_storage
        instance = Instance()
        prompt_for_storage(instance)
        assert instance.storage_size == 0

    with mock.patch('__builtin__.raw_input', return_value='0'):
        from touchpaper.prompts import prompt_for_storage
        instance = Instance()
        prompt_for_storage(instance)
        assert instance.storage_size == 0

    with mock.patch('__builtin__.raw_input', return_value='8'):
        from touchpaper.prompts import prompt_for_storage
        instance = Instance()
        prompt_for_storage(instance)
        assert instance.storage_size == 8


def test_prompt_for_tags():
    '''
    Test proper interpretation of tags list
    '''
    with mock.patch('__builtin__.raw_input', return_value='foo'):
        from touchpaper.prompts import prompt_for_tags
        config.data = SAMPLE_TAG_CONFIG
        instance = Instance()
        prompt_for_tags(instance)
        assert 'Name' in instance.tags
        assert 'OS' in instance.tags
