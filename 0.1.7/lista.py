# -*- coding: utf-8 -*-
from trytond.model import ModelView, ModelSQL, ModelSingleton, fields

from cefiro import *

class Lista(ModelSQL,ModelView):
	'Lista'
	_name = 'cefiro.lista'
	_description = __doc__
	name = fields.Char('Nombre de lista de espera',required=True,readonly=True)
	pacientes = fields.Many2Many('cefiro.listapac','lista','paciente','Pacientes en lista de espera')

Lista()


class ListaPac(ModelSQL):
	'ListaPac'
	_name = 'cefiro.listapac'
	_description = __doc__
	lista = fields.Many2One('cefiro.lista','Listas de espera',select=1)
	paciente = fields.Many2One('cefiro.paciente','Pacientes',select=1)

ListaPac()


