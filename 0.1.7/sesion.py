# -*- coding: utf-8 -*-
from trytond.model import ModelView, ModelSQL, ModelSingleton, fields

from dateutil.relativedelta import relativedelta
from datetime import datetime, date
from trytond.pool import Pool
from trytond.res import User

from cefiro import *

class Sesion(ModelSQL,ModelView):
	'Sesion'
	_name = 'cefiro.sesion'
	_description = __doc__
	_rec_name = 'fecha'
#	name=fields.Char('Nombre')
	
	fecha = fields.DateTime('Fecha y hora de la consulta',required=True)
	asistencia = fields.Boolean(u'El paciente asistió a la consulta')
	#consulta = fields.One2One('cefiro.consultainforme','informe','consulta','Consulta',required=True)
	comentarios = fields.Text(u'Registro de sesión')
	paciente = fields.Many2One('cefiro.paciente','Paciente')

Sesion()
