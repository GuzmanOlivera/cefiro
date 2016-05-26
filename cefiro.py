#co -*- coding: utf-8 -*-
from trytond.model import ModelView, ModelSQL, ModelSingleton, fields, Workflow

from dateutil.relativedelta import *#relativedelta
from datetime import * #datetime, date
from trytond.pool import Pool
from trytond.res import User
from trytond.pyson import Eval, If, DateTime, Not, Equal

from perfil import *

#Clases asociadas a personas ------------------------
class Persona(ModelSQL,ModelView):
	'Persona'
	_name = 'cefiro.persona'
	_description = __doc__
	name = fields.Char('Nombre',required=True)
	cedula = fields.Char('C.I.',required=True)
	telefono = fields.Char(u'Teléfono',required=True)
Persona()

class Psicologo(Persona):
	'Psicologo'
	_name = 'cefiro.psicologo'
	_description = __doc__


	login = fields.Char('Nombre de usuario interno',required=True)
	password = fields.Function(fields.Char(u'Contraseña',required=True),'mensaje','crear')
	telefono = fields.Char(u'Teléfono')
	mail = fields.Char(u'Correo electrónico')
	pacientes = fields.Many2Many('cefiro.psicopac','psicologo','paciente','Pacientes')
	consultas = fields.Many2Many('cefiro.encuentropsi','persona','evento','Consultas')

	#Esto es para crear el usuario interno
	def mensaje(self,ids,name):
		res = {}
		for elem in self.browse(ids):
			res[elem.id] = "xxxxxxxxxxxxxxxxxxxx"
		return res

	def crear(self,ids,name,value):
		user_obj = Pool().get('res.user')
		for elem in self.browse(ids):
			yaCreados = user_obj.search([('login','=','elem.login')])
			if len(yaCreados)==0:
				user_obj.create({'name':elem.name,'login':elem.login,'password':value})
			else:
				user_obj.write(yaCreados,{'password':value})
					
		return
	#Fin de lo del usuario interno

	#Esto es para reservar horarios por día de la semana
	reserva = fields.Many2Many('cefiro.reservapsic','psicologo','reserva',u'Reservas de horarios')

Psicologo()

#Implemento una clase que maneje las secuencias numéricas a crear. Principalmente para tener un número de paciente definido automáticamente.
class Sec(ModelSingleton,ModelSQL,ModelView):
	'Sec'
	_name = 'cefiro.sec'
	_description = __doc__

	numeropaciente = fields.Property(fields.Many2One('ir.sequence',u'Número de Paciente', required=True,domain=[('code', '=', 'cefiro.paciente')]))

Sec()
#----------------------------------------------------------------------

class Paciente(Persona,Workflow):
	'Paciente'
	_name = 'cefiro.paciente'
	_description = __doc__
	_rpc={'on_change_with_edad':True}
	#_rec_name = 'identidad'

	identidad = fields.Char('ID',readonly=True)

	def create(self, values):
		sequence_obj = Pool().get('ir.sequence')
		config_obj = Pool().get('cefiro.sec')

		values = values.copy()
		config = config_obj.browse(1)
		values['identidad'] = sequence_obj.get_id(config.numeropaciente.id)
		values['procesado_hc'] = False

	        return super(Paciente, self).create(values)

	
	genero = fields.Selection([('M','Masculino'),('F','Femenino'),('O','Otro')],'Genero') # Added - FALTA EN VISTA
	generoEspecificado = fields.Char('Otro Genero',states={'invisible': Not(Equal(Eval('genero'), 'O'))}) # Added - FALTA EN VISTA. Mostrar cuando genero vale O
	sexo = fields.Selection([('M','Masculino'),('F','Femenino')],'Sexo')
	nacimiento = fields.Date('Fecha de Nacimiento')
	edad = fields.Function(fields.Char('Edad',depends=['nacimiento'],on_change_with=['nacimiento']),'get_edad')
	def on_change_with_edad(self,values):
		ahora = date.today()
		edadtemp = relativedelta(ahora,values.get('nacimiento'))
		res = str(edadtemp.years)+u' años'
		return res

	servicio = fields.Char('Servicio') # Added - FALTABA EN VISTA
	lugarNacimiento = fields.Char('Lugar de nacimiento')	 # Added - FALTABA EN VISTA
	etnia = fields.Selection([('B','Blanco'),('N','Afro'),('I',u'Indígena'),('O','Otro')],'Etnia') # Added - FALTA EN VISTA

    #### ATENCION MEDICA ESTA EN INFOSAPPA ! #####

	telefono = fields.Char(u'Teléfono fijo') #Char por si hay telefonos internacionales, u otros símbolos
	celular = fields.Char(u'Teléfono celular') #Char por si hay códigos que no sean números
	#
	lista = fields.Many2Many('cefiro.listapac','paciente','lista','Lista de espera')
	#
	infosappa = fields.One2Many('cefiro.infosappa','paciente','SAPPA')

#	domicilio = fields.One2Many('cefiro.domiciliopac','dom_id','Domicilio')  ## Asi es como anda, pero esto implica 1 paciente y N domicilios
#	domicilio = fields.Many2One('cefiro.domiciliopac','Domicilio', context={'cefiro.domiciliopac': True}) # Asi es como tendria que ser 

	motivo = fields.Text('Motivo de Consulta')
	observaciones = fields.Text('Observaciones')
	#	
	horarioPref = fields.Char('Horario de Preferencia')
	psicologo = fields.Many2Many('cefiro.psicopac','paciente','psicologo',u'Psicólogo')
	consultas = fields.Many2Many('cefiro.encuentro','persona','evento','Consultas')
	estudiante = fields.Many2Many('cefiro.estudiante','paciente','estudiante','Estudiante')

	calle = fields.Char('Calle')
	esquina = fields.Char('Esquina')
	barrio = fields.Char('Barrio/Localidad')
	nroPuerta = fields.Char(u'Nº de puerta')
	apto = fields.Boolean('Apartamento')
	departamento = fields.Selection([('ar','Artigas'),('ca','Canelones'),('ce','Cerro Largo'),('co','Colonia'),('du','Durazno'),('flore','Flores'),('flori','Florida'),('lav','Lavalleja'),('mal','Maldonado'),('mon','Montevideo'),('pay',u'Paysandu'),('rio',u'Rio Negro'),('riv','Rivera'),('roc','Rocha'),('sal','Salto'),('san',u'San Jose'),('sor','Soriano'),('tac',u'Tacuarembo'),('tre','Treinta y Tres')],'Departamento')

	#
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

	#Ahora agrego la parte de historias clínicas
#	formularioInicial = fields.One2Many('cefiro.formulario','paciente','Formulario Inicial')
	formularioInicial = fields.One2Many('cefiro.formulario', 'paciente', 'Formulario Inicial', context={'cefiro.formulario': True}) 

	informesSesion = fields.One2Many('cefiro.sesion','paciente',u'Informes de Sesión')
	formularioFinal = fields.One2Many('cefiro.final','paciente',u'Formularios de Fin de Intevención')

	#Para el grupo HC
	procesado_hc = fields.Boolean(u'Códigos asignados')

	def get_id():
		return identidad

Paciente()

#Clases auxiliares para Paciente
class PsicoPac(ModelSQL):
	'PsicoPac'
	_name = 'cefiro.psicopac'
	_description = __doc__
	psicologo = fields.Many2One('cefiro.psicologo',u'Psicólogo(s)',select=1)
	paciente = fields.Many2One('cefiro.paciente','Pacientes',select=1)

PsicoPac()

# Added - FALTA EN VISTA c/campo de DomicilioPac
#class DomicilioPac(ModelSQL,ModelView):
	#'DomicilioPac'
	#_name = 'cefiro.domiciliopac'
	#_description = __doc__
#	dom_id = fields.Many2One('cefiro.paciente','Paciente') # Asi anda pero no esta bien. Esto implica 1 Paciente, N domicilios
	#paciente = fields.One2Many('cefiro.paciente','domicilio','Paciente')

#DomicilioPac()

class InfoSappa(ModelSQL,ModelView):
	'InfoSappa'
	_name = 'cefiro.infosappa'
	_description = __doc__
#	_history = True
	
	#
	convenioSAPPA = fields.Selection([('f','Funcionario'),('c',u'Cónyuge'),('p',u'Padre/Madre'),('h',u'Hijo/a')],u'Relación para el convenio')
	lugarTrabajo = fields.Char('Lugar de trabajo')
	funcionario = fields.Char(u'Número de funcionario') #Lo pongo char por si hay letras
	#
	atencionMedica = fields.Selection([('msp',u'MSP/ASSE'),('mut','Mutualista'),('pol','Policial/Militar'),('seg','Seguro')],u'Tipo de Atención Médica')
	mutualista = fields.Char('Nombre de la Mutualista')
	#
	fechaIngresoExpediente = fields.Date('Fecha de ingreso del expediente')

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
	  
	#
	profExternoDerivacion = fields.Boolean('Derivado a profesional externo')
	profExternoNombre = fields.Char('Nombre del profesional externo')
	profExternoFecha = fields.Date(u'Fecha de derivación')

	paciente = fields.Many2One('cefiro.paciente','Paciente')
	creacion = fields.DateTime(u'Creación')
        
	@classmethod
	def default_creacion(cls):
		return datetime.today()

InfoSappa()

#--------------------------------------------------------------------------------------

class Estudiante(Persona):
	'Estudiante'
	_name = 'cefiro.estudiante'
	_description = __doc__
	telefono = fields.Char(u'Teléfono')
	mail = fields.Char(u'Correo electrónico')
	
	login = fields.Char('Nombre de usuario interno',required=True)
	password = fields.Function(fields.Char(u'Contraseña',required=True),'mensaje','crear')	
	
	consultas = fields.Many2Many('cefiro.encuentroest','persona','evento','Consultas')
	pacientes = fields.Many2Many('cefiro.estpac','paciente','paciente','Paciente')

	#Esto es para crear el usuario interno

	def mensaje(self,ids,name):
		res = {}
		for elem in self.browse(ids):
			res[elem.id] = "xxxxxxxxxxxxxxxxxxxx"
		return res

	def crear(self,ids,name,value):
		user_obj = Pool().get('res.user')
		for elem in self.browse(ids):
			yaCreados = user_obj.search([('login','=','elem.login')])
			if len(yaCreados)==0:
				user_obj.create({'name':elem.name,'login':elem.login,'password':value})
			else:
				user_obj.write(yaCreados,{'password':value})
					
		return
	#Fin de lo del usuario interno

	#Esto es para reservar horarios por día de la semana
	reserva = fields.Many2Many('cefiro.reservaest','estudiante','reserva',u'Reservas de horarios')


Estudiante()

class EstPac(ModelSQL):
	'EstPac'
	_name = 'cefiro.estpac'
	_description = __doc__
	estudiante = fields.Many2One('cefiro.estudiante','Estudiante(s)',select=1) # Select=1 indica que se indexa este campo
	paciente = fields.Many2One('cefiro.paciente','Pacientes',select=1)

EstPac()

#--------------------------------------------------------------------------------------

#Clases asociadas a lugares ------------------------

class Consultorio(ModelSQL,ModelView):
	'Consultorio'
	_name = 'cefiro.consultorio'
	_description = __doc__
	name = fields.Char('Nombre')
	consultas = fields.One2Many('cefiro.consulta','consultorio','Consultas')
	ocupado = fields.DateTime(u'fecha de ocupación') #debug

Consultorio()
#--------------------------------------------------------------------------------------


#Clase Consulta-------------------------------------
class Consulta(ModelSQL,ModelView):
	'Consulta'
	_name = 'cefiro.consulta'
	_description = __doc__
	_rec_name = 'horaini'

	name = fields.Char('Nombre')

	libres=[]

	psicologos = fields.Many2Many('cefiro.encuentropsi','evento','persona',u'Psicólogos')
	pacientes = fields.Many2Many('cefiro.encuentro','evento','persona','Pacientes')	
	estudiantes = fields.Many2Many('cefiro.encuentroest','evento','persona','Estudiantes')


	horaini = fields.DateTime('Fecha y hora de inicio',required=True)
	horaFin = fields.DateTime('Fecha y hora de fin',required=True)

	consulLibres = fields.Function(fields.One2Many('cefiro.consultorio',None,'Consultorios libres',on_change_with=['horaini','horaFin']),'get_libres')

	consultorio = fields.Many2One('cefiro.consultorio','Consultorio',required=True,domain=[('id','in',Eval('consulLibres'))])

	def get_libres(self,ids,name):
		res = {}
		objConsul = Pool().get('cefiro.consultorio')
		for elem in self.browse(ids):
			res[elem.id] = elem.libres
		return res


	def on_change_with_consulLibres(self,values):
		res = []
		i1 = values.get('horaini')
		f1 = values.get('horaFin')
		#Chequeo que la entrada sea correcta
		if ((i1==None) or (f1==None)):
			return res
		else:
			if(f1 < i1):
				return res
		objConsultorio = Pool().get('cefiro.consultorio')
		objConsulta = Pool().get('cefiro.consulta')
		consultoriosTotId = objConsultorio.search([])
		for cons in objConsultorio.browse(consultoriosTotId):
			estaVacio = True
			consultasIDs = cons.consultas
			
			listaDic = objConsulta.read(consultasIDs)
			for dic in listaDic:
				i2 = dic.get('horaini')
				f2 = dic.get('horaFin')
				if not((f2<i1) or (f1<i2)):
					estaVacio = False
			if estaVacio:
				res.append(cons.id)

		self.libres = res		

		return res


Consulta()

#Clases auxiliares para Consulta
class Encuentro(ModelSQL):
	'Encuentro'
	_name = 'cefiro.encuentro'
	_description = __doc__
	persona = fields.Many2One('cefiro.paciente','Pacientes',select=1)
	evento = fields.Many2One('cefiro.consulta','Consultas',select=1)

Encuentro()

class EncuentroPsi(ModelSQL):
	'EncuentroPsi'
	_name = 'cefiro.encuentropsi'
	_description = __doc__
	persona = fields.Many2One('cefiro.psicologo',u'Psicólogos',select=1)
	evento = fields.Many2One('cefiro.consulta','Consultas',select=1)

EncuentroPsi()

class EncuentroEst(ModelSQL):
	'EncuentroEst'
	_name = 'cefiro.encuentroest'
	_description = __doc__
	persona = fields.Many2One('cefiro.estudiante','Estudiantes',select=1)
	evento = fields.Many2One('cefiro.consulta','Consultas',select=1)

EncuentroEst()

#--------------------------------------------------------------------------------------

#Clases auxiliares para Psicólogo
class PsicoUsuario(ModelSQL):
	'PsicoUsuario'
	_name = 'cefiro.psicousuario'
	_description = __doc__
	#psicologo = Psicologo()
	#usuario = User()
	psicologo = fields.Many2One('cefiro.psicologo',u'Psicólogo',select=1)
	usuario = fields.Many2One('res.user','Usuario',select=1)

PsicoUsuario()
#--------------------------------------------------------------------------------------

#Clases auxiliares para Estudiante
class EstUsuario(ModelSQL):
	'EstUsuario'
	_name = 'cefiro.estusuario'
	_description = __doc__

	estudiante = fields.Many2One('cefiro.estudiante','Estudiante',select=1)
	usuario = fields.Many2One('res.user','Usuario',select=1)

EstUsuario()

# <string name="ss"><![CDATA[<b>Bold.</b> <u>Underlined.</u> <i>Italic.</i> <big>Big.</big> <small>Small</small>]]></string>


#<group string="Enfermedades crónicas y deficiencias personales" id="cronicas" xexpand="1" xfill="1" col="8">
#<![CDATA[<b>Bold.</b>]]></group>