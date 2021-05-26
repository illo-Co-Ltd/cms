from flask_restplus import Api

from .data.company_router import api as _
from .data.cell_router import api as _
from .data.device_router import api as _
from .data.device_entry_router import api as _
from .data.image_router import api as _
from .data.project_router import api as _
from .data.user_router import api as _
from .data.company_router import api as _
from .auth_router import api as _
from .control_router import api as _
from .explorer_router import api as _

from router.dto.data_dto import api_data
from router.dto.auth_dto import api_auth
from router.dto.control_dto import api_control
from router.dto.status_dto import api_status
from router.dto.explorer_dto import api_explorer

api = Api(version='1.0', title='Backend API', description='API for DB access and device control')

# Data accessing API
api.add_namespace(api_data, path='/data')
# Auth API
api.add_namespace(api_auth, path='/auth')
# Device control API
api.add_namespace(api_control, path='/control')
# File explorer API
api.add_namespace(api_explorer, path='/explorer')
# Status check
#api.add_namespace(api_status, path='/status')
