# -*- coding: utf-8 -*-
from trytond.model import ModelView, ModelSQL, ModelSingleton, fields

from dateutil.relativedelta import *#relativedelta
from datetime import * #datetime, date
from trytond.pool import Pool
from trytond.res import User
from trytond.pyson import Eval, If, DateTime
from trytond.transaction import Transaction

from cefiro import *

class Perfil(ModelSQL,ModelView):
	'Perfil'
	_name = 'cefiro.perfil'
	_description = __doc__

	name=fields.Char('Nombre')

	user = fields.Function(fields.Char('Usuario'),'get_usuario')

	#reg_usuario = fields.Reference('Registro Referencia')
	#reg_usuario = fields.Function(fields.Reference('Registro Usuario'),'get_reg_usuario')

	#def get_reg_usuario(self,ids,name):
	#	res = {}
	#	user_obj = Pool().get('res.user')
	#	usrid = Transaction().user
	#	for elem in self.browse(ids):
	#		res[elem.id] = '<res.user>,<'+str(usrid)+'>'
	#	return res


	perf=[]
	perf2=None

	def get_usuario(self,ids,name):
		res = {}
		user_obj = Pool().get('res.user')
		usrid = Transaction().user
		usuario = user_obj.browse(usrid)
		for elem in self.browse(ids):
			res[elem.id] = usuario.login
		return res


	#password = fields.Function(fields.Char(u'Contraseña'),'mensaje','crear')


	perfiles = fields.Function(fields.One2Many('cefiro.psicologo',None,'Perfiles'),'get_perfiles','set_perfiles')

	perfilesEst = fields.Function(fields.One2Many('cefiro.estudiante',None,'Perfiles'),'get_perfilest','set_perfiles')

	def get_perfilest(self,ids,name):
		res = {}

		user_obj = Pool().get('res.user')
		usrid = Transaction().user
		usuario = user_obj.browse(usrid)

		est_obj = Pool().get('cefiro.estudiante')
		estIDsTot = est_obj.search([])

		for elem in self.browse(ids):
			sol=[]
			for est in est_obj.browse(estIDsTot):
				if (est.login==usuario.login):
					sol.append(est.id)
			res[elem.id]=sol
		return res

	def get_perfiles(self,ids,name):
		res = {}

		user_obj = Pool().get('res.user')
		usrid = Transaction().user
		usuario = user_obj.browse(usrid)

		psi_obj = Pool().get('cefiro.psicologo')
		psiIDsTot = psi_obj.search([])

		for elem in self.browse(ids):
			sol=[]
			for psi in psi_obj.browse(psiIDsTot):
				if (psi.login==usuario.login):
					sol.append(psi.id)
			res[elem.id]=sol
		return res

	def set_perfiles(self,ids,name,value):
		return

	#perfiles = fields.One2Many('cefiro.psicologo',None,'Perfiles',domain=[('login','=',Eval('user'))])

Perfil()





