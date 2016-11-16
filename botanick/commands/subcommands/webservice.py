# -*- coding: utf-8 -*-
import os
from flask import Flask, Blueprint
from flask_restplus import Api, Resource
from botanick.core.harvester import harvest
from botanick.core.converters import tostring
from botanick.const import BASE_PATH
from botanick.const import VERSION


app = Flask("Botanick")

api = Api(version=VERSION, title='Botanick Webservice API',
    description='Search email address for a specified domain',
)

ns_emails = api.namespace('emails', description='Operations related to emails harvesting')

blueprint_index = Blueprint('index', __name__)

@ns_emails.route('/<domain>')
@ns_emails.param('domain', 'The domain name')
class MailList(Resource):

	@classmethod
	def get(cls, domain):
		"""
		Search emails for a specific domain name.
		Arguments:
			domain -- the domain name
		"""
		return tostring(harvest(domain))

@blueprint_index.route('/')
def showIndex():
	"""Return the index page content"""
	with open(os.path.join(BASE_PATH, 'botanick', 'templates', 'index.py')) as template:
		return "".join(template.readlines())


def webservice(args):
	blueprint = Blueprint('api', __name__, url_prefix='/api')
	api.init_app(blueprint)
	api.add_namespace(ns_emails)
	app.register_blueprint(blueprint)

	app.register_blueprint(blueprint_index)

	app.run(debug=True, host=args['host'])
