from flask_restplus import Api

from .data.company_router import api as company_ns
from .data.project_router import api as project_ns
from .data.device_router import api as device_ns
from .data.device_entry_router import api as device_entry_ns
from .data.cell_router import api as cell_ns
from .data.image_router import api as image_ns
from .auth import api as auth_ns
# from camera import api as camera_ns
from .check import api as check_ns

api = Api(version='1.0', title='illo API', description='API for DB access and device control')

# Data accessing APIs
api.add_namespace(company_ns, path='/data/company')
api.add_namespace(project_ns, path='/data/project')
api.add_namespace(device_ns, path='/data/device')
api.add_namespace(device_entry_ns, path='/data/device_entry')
api.add_namespace(cell_ns, path='/data/cell')
api.add_namespace(image_ns, '/data/image')

# Other APIs
api.add_namespace(auth_ns, path='/auth/user')
# api.add_namespace(camera_ns)
api.add_namespace(check_ns, path='/check')
