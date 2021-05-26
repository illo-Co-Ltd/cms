from flask_restplus import Namespace, fields

api_explorer = Namespace('explorer', description='File explorer API')


class ListDirDTO:
    api = api_explorer
    model = api.model('listdir', {
        'children': fields.List(fields.String)
    })