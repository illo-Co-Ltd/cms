class CGIException(Exception):
    def __init__(self, resp):
        super(CGIException, self).__init__()
        self.response = resp

        @property
        def text(self):
            return self.response.text

        @property
        def status_code(self):
            return self.response.status_code
