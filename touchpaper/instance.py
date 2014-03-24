class Instance():
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

    _instance = None
    _conn = None

    def add_storage_tag(self, name):
        ''' Tag the instance's storage with a name '''
        pass

    def add_tags(self, tags):
        ''' Tag the instance '''
        pass

    def get(self):
        ''' Return the actual boto instance representation '''
        return self.instance

    def prep_storage(self, size):
        ''' Prepare blockdevicemapping for instance '''
        pass

    def run(self):
        ''' Initiate the instance with boto's run_instances() '''
        pass

    def set_conn(self, conn):
        ''' Update the internal boto connection property '''
        self._conn = conn
        return self
