import boto.ec2


class Instance:
    region = None
    availability_zone = None
    ami = None
    instance_type = None
    atp = False
    storage_name = None
    storage_size = 0
    keypair = None
    security_group = None
    tags = {}

    _dry_run = False
    _instance = None
    _conn = None
    _bdm = None

    def __init__(self, dry_run):
        ''' Pick up dry-run arg if set '''
        if dry_run:
            self._dry_run = True
        return self

    def get(self):
        ''' Return the actual boto instance representation '''
        return self._instance

    def prep_storage(self, size):
        '''
        If a storage size is specified, set up the EC2 BlockDeviceMapping ready
        to attach it to the instance at launch
        (source: http://stackoverflow.com/a/13604274/258794)
        '''
        if self.storage_size != 0:
            dev_sda1 = boto.ec2.blockdevicemapping.EBSBlockDeviceType()
            dev_sda1.size = self.storage_size
            bdm = boto.ec2.blockdevicemapping.BlockDeviceMapping()
            bdm['/dev/sda1'] = dev_sda1
            self._bdm = bdm
        return self

    def run(self):
        ''' Initiate the instance with boto's run_instances() '''
        if self._conn:
            res = self._conn.run_instances(image_id=self.ami,
                                           key_name=self.keypair.name if self.keypair else None,
                                           security_groups=[self.security_group.name,],
                                           instance_type=self.instance_type,
                                           placement=self.availability_zone.name,
                                           block_device_map=self._bdm if self._bdm else None,
                                           disable_api_termination=self.atp,
                                           dry_run=self._dry_run)
            self._instance = res.instances[0]
        return self

    def set_conn(self, conn):
        ''' Update the internal boto connection property '''
        self._conn = conn
        return self

    def set_storage_tag(self):
        ''' Tag the instance's storage with a name '''
        if self._instance and self.storage_name:
            volumes = self._conn.get_all_volumes(filters={ 'attachment.instance-id': self._instance.id })
            if volumes:
                volumes[0].add_tag('Name', self.storage_name)
                print "EBS volume tags added"
        return self

    def set_tags(self, tags):
        ''' Tag the instance '''
        if self.tags:
            for tag, value in self.tags.iteritems():
                self._instance.add_tag(tag, value)
            print "Instance tags added"
        return self
