# -*- coding: utf-8 -*-
from trytond.model import ModelView, ModelSQL, ModelSingleton, fields

from dateutil.relativedelta import relativedelta
from datetime import datetime, date

#Clases asociadas a personas ------------------------
class Persona(ModelSQL,ModelView):
	'Persona'
	_name = 'cefiro.persona'
	_description = __doc__
	name = fields.Char('Nombre',required=True)
	cedula = fields.Char('C.I.',required=True)

Persona()

class Psicologo(Persona):
	'Psicologo'
	_name = 'cefiro.psicologo'
	_description = __doc__
	telefono = fields.Char(u'Teléfono')
	mail = fields.Char(u'Correo electrónico')
	pacientes = fields.One2Many('cefiro.paciente','psicologo','Pacientes')
	consultas = fields.Many2Many('cefiro.encuentropsi','persona','evento','Consultas')

Psicologo()

class Paciente(Persona):
	'Paciente'
	_name = 'cefiro.paciente'
	_description = __doc__

	sexo = fields.Selection([('M','Masculino'),('F','Femenino'),('I',u'No contesta/Otro')],'Sexo')
	nacimiento = fields.Date('Fecha de Nacimiento')
	edad = fields.Function(fields.Char('Edad'),'get_edad') #fields.Integer('Edad') #Habría que relacionarlo con la fecha de nacimiento y hacerlo de sólo lectura
	telefono = fields.Char(u'Teléfono fijo') #Char por si hay telefonos internacionales, u otros símbolos
	celular = fields.Char(u'Teléfono celular') #Char por si hay códigos que no sean números
	#
	convenioSAPPA = fields.Selection([('f','Funcionario'),('c',u'Cónyuge'),('p',u'Padre/Madre'),('h',u'Hijo/a')],u'Relación para el convenio')
	lugarTrabajo = fields.Char('Lugar de trabajo')
	funcionario = fields.Char(u'Número de funcionario') #Lo pongo char por si hay letras
	#
	atencionMedica = fields.Selection([('msp',u'MSP/ASSE'),('mut','Mutualista')],u'Tipo de Atención Médica')
	mutualista = fields.Char('Nombre de la Mutualista')
	#
	fechaIngresoExpediente = fields.Date('Fecha de ingreso del expediente')
	motivo = fields.Text('Motivo de Consulta')
	observaciones = fields.Text('Observaciones')
	#	
	horarioPref = fields.Char('Horario de Preferencia')
	psicologo = fields.Many2One('cefiro.psicologo',u'Psicólogo')
	consultas = fields.Many2Many('cefiro.encuentro','persona','evento','Consultas')
	#
	#Formularios entregados para el SAPPA
	form_OQ45T1 = fields.Boolean(u'OQ45-T1')
	form_OQ45T2 = fields.Boolean(u'OQ45-T2')
	form_EncuestaSatisfaccion = fields.Boolean(u'Encuesta de Satisfacción')
	form_EcuestaSatPExtProfesional = fields.Boolean(u'Encuesta de Satisfacción - Prof. Externo : Profesional')
	form_EncuestaSatPExtPaciente = fields.Boolean(u'Encuesta de Satisfacción - Prof. Externo: Paciente')
	#
	profExternoDerivacion = fields.Boolean('Derivado a profesional externo')
	profExternoNombre = fields.Char('Nombre del profesional externo')
	profExternoFecha = fields.Date(u'Fecha de derivación')

	#Cálculo de la edad
	def get_edad(self,ids,name):
		ahora = date.today()
		res = {}
        	for pac in self.browse(ids):
			edadtemp = relativedelta(ahora,pac.nacimiento)
            		res[pac.id] = str(edadtemp.years)+u' años'
        	return res
Paciente()

class Estudiante(Persona):
	'Estudiante'
	_name = 'cefiro.estudiante'
	_description = __doc__
	telefono = fields.Char(u'Teléfono')
	mail = fields.Char(u'Correo electrónico')
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
	fecha = fields.DateTime('Fecha y Hora de la Consulta')
#	hora = fields.Time('Hora')
	psicologos = fields.Many2Many('cefiro.encuentropsi','evento','persona',u'Psicólogos')
	pacientes = fields.Many2Many('cefiro.encuentro','evento','persona','Pacientes')	
	estudiantes = fields.Many2Many('cefiro.encuentroest','evento','persona','Estudiantes')
	consultorio = fields.Many2One('cefiro.consultorio','Consultorio',required=True)

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
	persona = fields.Many2One('cefiro.psicologo',u'Psicólogos',select=1,required=True)
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



