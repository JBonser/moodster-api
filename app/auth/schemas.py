from flask_restplus import fields, Model


auth_login_view_schema = Model('auth_login_view', {
    'access_token': fields.String(description='access token')
})
