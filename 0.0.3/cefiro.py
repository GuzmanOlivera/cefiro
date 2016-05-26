# -*- coding: utf-8 -*-
from trytond.model import ModelView, ModelSQL, fields

class Persona(ModelSQL,ModelView):
	'Persona'
	_name = 'cefiro.persona'
	_description = __doc__
	name = fields.Char('Nombre')
	cedula = fields.Char('C.I.')

Persona()

class Consulta(ModelSQL,ModelView):
	'Consulta'
	_name = 'cefiro.consulta'
	_description = __doc__
	name = fields.Char('nombreDeFecha')
	fecha = fields.Date('Fecha de la Consulta')
	hora = fields.Time('Hora')
	psicologos = fields.One2Many('cefiro.psicologo','consultas','Psicologos')
	pacientes = fields.Many2Many('cefiro.encuentro','evento','persona','Pacientes')	

Consulta()

class Psicologo(ModelSQL,ModelView):
	'Psicologo'
	_name = 'cefiro.psicologo'
	_description = __doc__
	nombre = fields.Char('Nombre')
	cedula = fields.Char('C.I.')
	pacientes = fields.One2Many('cefiro.paciente','psicologo','Pacientes')
	consultas = fields.Many2One('cefiro.consulta','Consultas')

Psicologo()


class Paciente(Persona):
	'Paciente'
	_name = 'cefiro.paciente'
	_description = __doc__
	psicologo = fields.Many2One('cefiro.psicologo','Psicologo')
	consultas = fields.Many2Many('cefiro.encuentro','persona','evento','Consultas')

Paciente()


#Clase auxiliar para Consulta
class Encuentro(ModelSQL):
	'Encuentro'
	_name = 'cefiro.encuentro'
	_description = __doc__
	persona = fields.Many2One('cefiro.paciente','Paciente',select=1,required=True)
	evento = fields.Many2One('cefiro.consulta','Consulta',select=1,required=True)

Encuentro()

