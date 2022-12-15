from flasgger import Swagger

def init_app(app):
    swagger = Swagger(app, merge=True, template_file = 'docs/swagger.yaml')