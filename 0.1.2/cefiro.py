# -*- coding: utf-8 -*-
from trytond.model import ModelView, ModelSQL, ModelSingleton, fields

from dateutil.relativedelta import *#relativedelta
from datetime import * #datetime, date
from trytond.pool import Pool
from trytond.res import User
from trytond.pyson import Eval, If, DateTime

from lista import *
from hc import *

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


	login = fields.Char('Nombre de usuario interno',required=True)
	password = fields.Function(fields.Char(u'Contraseña',required=True),'mensaje','crear')
	telefono = fields.Char(u'Teléfono')
	mail = fields.Char(u'Correo electrónico')
	pacientes = fields.One2Many('cefiro.paciente','psicologo','Pacientes',readonly=True)
	consultas = fields.Many2Many('cefiro.encuentropsi','persona','evento','Consultas')

	#Esto es para crear el usuario interno
#	confirmacionInterno = fields.Function(fields.Char(u'Confirmación (dejar en blanco)'),'mensaje','crear')

	def mensaje(self,ids,name):
		res = {}
		for elem in self.browse(ids):
#			res[elem.id] = "Usuario interno creado"
			res[elem.id] = "xxxxxxxxxxxxxxxxxxxx"
		return res

	def crear(self,ids,name,value):
		user_obj = Pool().get('res.user')
		for elem in self.browse(ids):
			user_obj.create({'name':elem.name,'login':elem.login,'password':value})
		return
	#Fin de lo del usuario interno

Psicologo()

class Paciente(Persona):
	'Paciente'
	_name = 'cefiro.paciente'
	_description = __doc__
	_rpc={'on_change_with_edad':True}

	sexo = fields.Selection([('M','Masculino'),('F','Femenino')],'Sexo')
	nacimiento = fields.Date('Fecha de Nacimiento')
	edad = fields.Function(fields.Char('Edad',depends=['nacimiento'],on_change_with=['nacimiento']),'get_edad')
	def on_change_with_edad(self,values):
		ahora = date.today()
		edadtemp = relativedelta(ahora,values.get('nacimiento'))
         	res = str(edadtemp.years)+u' años'
		return res
		

	telefono = fields.Char(u'Teléfono fijo') #Char por si hay telefonos internacionales, u otros símbolos
	celular = fields.Char(u'Teléfono celular') #Char por si hay códigos que no sean números
	#
	lista = fields.Many2One('cefiro.lista','Lista de espera')
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
		#usu = User()
		#usu.create([('name','pruebalala'),('login','loolololo')])
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
	ocupado = fields.DateTime(u'fecha de ocupación') #debug

Consultorio()
#--------------------------------------------------------------------------------------


#Clase Consulta-------------------------------------
class Consulta(ModelSQL,ModelView):
	'Consulta'
	_name = 'cefiro.consulta'
	_description = __doc__
	#_rec_name = 'horaIni'

	name = fields.Char('Nombre')

	psicologos = fields.Many2Many('cefiro.encuentropsi','evento','persona',u'Psicólogos')
	pacientes = fields.Many2Many('cefiro.encuentro','evento','persona','Pacientes')	
	estudiantes = fields.Many2Many('cefiro.encuentroest','evento','persona','Estudiantes')

	informe = fields.One2One('cefiro.consultainforme','consulta','informe','Informe')

	horaIni = fields.DateTime('Fecha y hora de inicio',required=True)
	horaFin = fields.DateTime('Fecha y hora de fin',required=True)

	consulLibres = fields.Function(fields.One2Many('cefiro.consultorio',None,'Consultorios libres',on_change_with=['horaIni','horaFin']),'get_libres')
	consultorio = fields.Many2One('cefiro.consultorio','Consultorio',required=True)#,domain=[('name','=','Consultorio 9')])

	def get_libres(self,ids,name):
		res = {}
		objConsul = Pool().get('cefiro.consultorio')
		for elem in self.browse(ids):
			res[elem.id] = []
#			if consultorio_ids:
#				res[elem.id].extend(consultorio_ids)
		return res


#	def on_change_with_consulLibres(self,values):
#		return []

	def on_change_with_consulLibres(self,values):
		objConsultorio = Pool().get('cefiro.consultorio')
		consultoriosTotId = objConsultorio.search([])
		res=[]
		for cons in objConsultorio.browse(consultoriosTotId):
			estaVacio = True
			objConsulta = Pool().get('cefiro.consulta')
			consultasIDs = cons.consultas
			
			listaDic = objConsulta.read(consultasIDs)
			for dic in listaDic:
				i1 = values.get('horaIni')
				f1 = values.get('horaFin')
				i2=dic.get('horaIni')
				f2=dic.get('horaFin')
				if not ((i1==None) or (f1==None)):
					if not((f2<i1) or (f1<i2)):
						estaVacio = False
			if estaVacio:
				res.append(cons.id)
		return res

	#def get_name(self,ids,name):
	#	res = {}
	#	for elem in self.browse(ids):
	#		res[elem.id] = str(elem.horaIni)
	#	return res

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

class ConsultaInforme(ModelSQL):
	'ConsultaInforme'
	_name = 'cefiro.consultainforme'
	_description = __doc__

	consulta = fields.Many2One('cefiro.consulta','Consulta',select=1,required=True)
	informe = fields.Many2One('cefiro.sesion',u'Informe de sesión',select=1,required=True)

ConsultaInforme()
#--------------------------------------------------------------------------------------

#Clases auxiliares para Psicólogo
class PsicoUsuario(ModelSQL):
	'PsicoUsuario'
	_name = 'cefiro.psicousuario'
	_description = __doc__
	#psicologo = Psicologo()
	#usuario = User()
	psicologo = fields.Many2One('cefiro.psicologo',u'Psicólogo',select=1,required=True)
	usuario = fields.Many2One('res.user','Usuario',select=1,required=True)

PsicoUsuario()
#--------------------------------------------------------------------------------------

class Reserva(ModelSQL,ModelView):
	'Reserva'
	_name = 'cefiro.reserva'
	

	horaIni = fields.DateTime('Fecha y hora de inicio')
	horaFin = fields.DateTime('Fecha y hora de fin')
	consulLibres = fields.Function(fields.One2Many('cefiro.consultorio',None,'Consultorios libres',on_change_with=['horaIni','horaFin']),'get_libres')
	consultorio = fields.Many2One('cefiro.consultorio','Consultorio',required=True,domain=[('name','=','Consultorio 9')])

	def get_libres(self,ids,name):
		res = {}
		objConsul = Pool().get('cefiro.consultorio')
		consultorio_ids = objConsul.search([('name','=','Consultorio 9')])
		for elem in self.browse(ids):
			res[elem.id] = []
			if consultorio_ids:
				res[elem.id].extend(consultorio_ids)
		return res


	def on_change_with_consulLibres(self,values):
		objConsul = Pool().get('cefiro.consultorio')
		res = objConsul.search([('name','=','Consultorio 9')])
		return res

Reserva()


