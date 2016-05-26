# -*- coding: utf-8 -*-
from trytond.model import ModelView, ModelSQL, ModelSingleton, fields

from cefiro import *

class Lista(ModelSQL,ModelView):
	'Lista'
	_name = 'cefiro.lista'
	_description = __doc__
	name = fields.Char('Nombre de lista de espera',required=True,readonly=True)
	pacientes = fields.One2Many('cefiro.paciente','lista','Pacientes en lista de espera',readonly=True)

Lista()





