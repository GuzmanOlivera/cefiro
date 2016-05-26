# -*- coding: utf-8 -*-
from trytond.model import ModelView, ModelSQL, fields

#Clases asociadas a personas ------------------------
class Persona(ModelSQL,ModelView):
	'Persona'
	_name = 'cefiro.persona'
	_description = __doc__
	name = fields.Char('Nombre')
	cedula = fields.Char('C.I.')

Persona()

class Psicologo(Persona):
	'Psicologo'
	_name = 'cefiro.psicologo'
	_description = __doc__
	pacientes = fields.One2Many('cefiro.paciente','psicologo','Pacientes')
	consultas = fields.Many2Many('cefiro.encuentropsi','persona','evento','Consultas')

Psicologo()


class Paciente(Persona):
	'Paciente'
	_name = 'cefiro.paciente'
	_description = __doc__
	psicologo = fields.Many2One('cefiro.psicologo','Psicologo')
	consultas = fields.Many2Many('cefiro.encuentro','persona','evento','Consultas')

Paciente()

class Estudiante(Persona):
	'Estudiante'
	_name = 'cefiro.estudiante'
	_description = __doc__
	consultas = fields.Many2Many('cefiro.encuentroest','persona','evento','Consultas')

Estudiante()
#--------------------------------------------------------------------------------------

#Clases asociadas a lugares ------------------------

class Consultorio(ModelSQL,ModelView):
	'Consultorio'
	_name = 'cefiro.consultorio'
	_description = __doc__
	name = fields.Char('Nombre')
	consultas = fields.One2Many('cefiro.consulta','consultorio','Consultas',readonly=True)

Consultorio()
#--------------------------------------------------------------------------------------


#Clase Consulta-------------------------------------
class Consulta(ModelSQL,ModelView):
	'Consulta'
	_name = 'cefiro.consulta'
	_description = __doc__
	name = fields.Char('nombreDeFecha')
	fecha = fields.Date('Fecha de la Consulta')
	hora = fields.Time('Hora')
	psicologos = fields.Many2Many('cefiro.encuentropsi','evento','persona','Psicologos')
	pacientes = fields.Many2Many('cefiro.encuentro','evento','persona','Pacientes')	
	estudiantes = fields.Many2Many('cefiro.encuentroest','evento','persona','Estudiantes')
	consultorio = fields.Many2One('cefiro.consultorio','Consultorio')

Consulta()

#Clases auxiliares para Consulta
class Encuentro(ModelSQL):
	'Encuentro'
	_name = 'cefiro.encuentro'
	_description = __doc__
	persona = fields.Many2One('cefiro.paciente','Pacientes',select=1,required=True)
	evento = fields.Many2One('cefiro.consulta','Consultas',select=1,required=True)

Encuentro()

class EncuentroPsi(ModelSQL):
	'EncuentroPsi'
	_name = 'cefiro.encuentropsi'
	_description = __doc__
	persona = fields.Many2One('cefiro.psicologo','Psicologos',select=1,required=True)
	evento = fields.Many2One('cefiro.consulta','Consultas',select=1,required=True)

EncuentroPsi()

class EncuentroEst(ModelSQL):
	'EncuentroEst'
	_name = 'cefiro.encuentroest'
	_description = __doc__
	persona = fields.Many2One('cefiro.estudiante','Estudiantes',select=1,required=True)
	evento = fields.Many2One('cefiro.consulta','Consultas',select=1,required=True)

EncuentroEst()
#--------------------------------------------------------------------------------------


