# -*- coding: utf-8 -*-
from trytond.model import ModelView, ModelSQL, ModelSingleton, fields

from dateutil.relativedelta import relativedelta
from datetime import datetime, date
from trytond.pool import Pool
from trytond.res import User
from trytond.pyson import Eval, If, Bool, Equal, Not, And, Or
from psycopg2.extensions import AsIs
from formulario import *

from cefiro import *

class FormularioViviendaTrabajo(ModelSQL,ModelView):
	'Formvt'
	_name = 'cefiro.formvt'
	_description = __doc__

	###################
	### F I E L D S ###
	###################

	tipoVivienda = fields.Selection([('casa','La casa'),('calle','La calle'),('inst',u'Institución protectora'),('car','Privado de libertad')],'Vive en',required=True)

	#convive = fields.One2Many() Hay que hacer uno para familiares posibles. Por ahora va un Selection.
	conviveSolo = fields.Selection([('si',u'Sí'),('no','No')],'Vive solo',required=True)

	conviveMadre = fields.Boolean('Madre',states={
			'required':
				And(And(
					Not(Bool(Eval('convivePadre'))),
					Not(Bool(Eval('conviveMadrastra'))),
					Not(Bool(Eval('convivePadrastro'))),
					Not(Bool(Eval('conviveHermanos'))),
					Not(Bool(Eval('convivePareja'))),
					Not(Bool(Eval('conviveHijos'))),
					Not(Bool(Eval('conviveOtros')))
				),
				Equal(Eval('conviveSolo'),'no'))
		})
	convivePadre = fields.Boolean('Padre',states={
			'required':
				And(And(
					Not(Bool(Eval('conviveMadre'))),
					Not(Bool(Eval('conviveMadrastra'))),
					Not(Bool(Eval('convivePadrastro'))),
					Not(Bool(Eval('conviveHermanos'))),
					Not(Bool(Eval('convivePareja'))),
					Not(Bool(Eval('conviveHijos'))),
					Not(Bool(Eval('conviveOtros')))
				),
				Equal(Eval('conviveSolo'),'no'))
		})
	conviveMadrastra = fields.Boolean('Madrastra',states={
			'required':
				And(And(
					Not(Bool(Eval('convivePadre'))),
					Not(Bool(Eval('conviveMadre'))),
					Not(Bool(Eval('convivePadrastro'))),
					Not(Bool(Eval('conviveHermanos'))),
					Not(Bool(Eval('convivePareja'))),
					Not(Bool(Eval('conviveHijos'))),
					Not(Bool(Eval('conviveOtros')))
				),
				Equal(Eval('conviveSolo'),'no'))
		})
	convivePadrastro = fields.Boolean('Padrastro',states={
			'required':
				And(And(
					Not(Bool(Eval('convivePadre'))),
					Not(Bool(Eval('conviveMadrastra'))),
					Not(Bool(Eval('conviveMadre'))),
					Not(Bool(Eval('conviveHermanos'))),
					Not(Bool(Eval('convivePareja'))),
					Not(Bool(Eval('conviveHijos'))),
					Not(Bool(Eval('conviveOtros')))
				),
				Equal(Eval('conviveSolo'),'no'))
		})
	conviveHermanos = fields.Boolean(u'Hermano/a(s)',states={
			'required':
				And(And(
					Not(Bool(Eval('convivePadre'))),
					Not(Bool(Eval('conviveMadrastra'))),
					Not(Bool(Eval('convivePadrastro'))),
					Not(Bool(Eval('conviveMadre'))),
					Not(Bool(Eval('convivePareja'))),
					Not(Bool(Eval('conviveHijos'))),
					Not(Bool(Eval('conviveOtros')))
				),
				Equal(Eval('conviveSolo'),'no'))
		})
	convivePareja = fields.Boolean('Pareja',states={
			'required':
				And(And(
					Not(Bool(Eval('convivePadre'))),
					Not(Bool(Eval('conviveMadrastra'))),
					Not(Bool(Eval('convivePadrastro'))),
					Not(Bool(Eval('conviveHermanos'))),
					Not(Bool(Eval('conviveMadre'))),
					Not(Bool(Eval('conviveHijos'))),
					Not(Bool(Eval('conviveOtros')))
				),
				Equal(Eval('conviveSolo'),'no'))
		})
	conviveHijos = fields.Boolean('Hijo(s)',states={
			'required':
				And(And(
					Not(Bool(Eval('convivePadre'))),
					Not(Bool(Eval('conviveMadrastra'))),
					Not(Bool(Eval('convivePadrastro'))),
					Not(Bool(Eval('conviveHermanos'))),
					Not(Bool(Eval('convivePareja'))),
					Not(Bool(Eval('conviveMadre'))),
					Not(Bool(Eval('conviveOtros')))
				),
				Equal(Eval('conviveSolo'),'no'))
		})
	conviveOtros = fields.Boolean('Otros',states={
			'required':
				And(And(
					Not(Bool(Eval('convivePadre'))),
					Not(Bool(Eval('conviveMadrastra'))),
					Not(Bool(Eval('convivePadrastro'))),
					Not(Bool(Eval('conviveHermanos'))),
					Not(Bool(Eval('convivePareja'))),
					Not(Bool(Eval('conviveHijos'))),
					Not(Bool(Eval('conviveMadre')))
				),
				Equal(Eval('conviveSolo'),'no'))
	})

	situacionCony = fields.Selection([('sol',u'Soltero/a'),('casado',u'Casado/a (incluye separado/a sin divorcio)'),('divor',u'Divorciado/a'),('viudo',u'Viudo/a'),('ulibre',u'Unión libre'),('slibre',u'Separado de unión libre')],'Estado Conyugal',required=True)

	vivHabitaTot = fields.Integer('Habitaciones totales',required=True)
	vivHabitaDor = fields.Integer('Dormitorios',required=True)
	vivBanos = fields.Integer(u'Cantidad de Baños',required=True)
	vivBanoComp = fields.Boolean(u'Baño compartido')
	vivBanoTipo = fields.Selection([('red','Red general'),('fosa',u'Fosa séptica o pozo negro'),('otro',u'Otro (hueco en suelo, superficie)')],u'Tipo de instalación sanitaria',required=True)
	vivEnergiaElectrica = fields.Boolean(u'Energía eléctrica')
	vivAguaPotable = fields.Boolean(u'Agua potable')
	vivObs = fields.Text('Observaciones')

	trabSituacion = fields.Selection([('trab','Trabaja'),('bus','Busca por primera vez'),('no','No trabaja'),('pas',u'Pasantía'),('pens','Pensionista'),('jub','Jubilado')],u'Situación Laboral',required=True)
	trabMulti = fields.Boolean('Multiempleo',
		states = {'invisible': 

		Or(Equal(Eval('trabSituacion'),'no'),Equal(Eval('trabSituacion'),'bus'),
				Equal(Eval('trabSituacion'),'jub'),
				Equal(Eval('trabSituacion'),'pens')
			)
		})
	trabHoras = fields.Integer('Horas Totales',
		states = {'invisible': 

		Or(Equal(Eval('trabSituacion'),'no'),Equal(Eval('trabSituacion'),'bus'),
				Equal(Eval('trabSituacion'),'jub'),
				Equal(Eval('trabSituacion'),'pens')
			),

			'required':
					Not(
						Or( 
							Equal(Eval('trabSituacion'),'no'),
							Equal(Eval('trabSituacion'),'bus'),
							Equal(Eval('trabSituacion'),'jub'),
							Equal(Eval('trabSituacion'),'pens')
						)
					)

		})
	trabHorasPrin = fields.Integer('Horas Trabajo Principal',
		states = {'invisible': 

				Or(Equal(Eval('trabSituacion'),'no'),Equal(Eval('trabSituacion'),'bus'),
				Equal(Eval('trabSituacion'),'jub'),
				Equal(Eval('trabSituacion'),'pens')
			),

			'required':
					Not(
						Or( 
							Equal(Eval('trabSituacion'),'no'),
							Equal(Eval('trabSituacion'),'bus'),
							Equal(Eval('trabSituacion'),'jub'),
							Equal(Eval('trabSituacion'),'pens')
						)
					)
		})
	trabInicio = fields.Integer('Edad de inicio de trabajo',
		states = {'invisible': 

		Or(Equal(Eval('trabSituacion'),'no'),Equal(Eval('trabSituacion'),'bus'),
				Equal(Eval('trabSituacion'),'jub'),
				Equal(Eval('trabSituacion'),'pens')
			),

		'required':
					Not(
						Or( 
							Equal(Eval('trabSituacion'),'no'),
							Equal(Eval('trabSituacion'),'bus'),
							Equal(Eval('trabSituacion'),'jub'),
							Equal(Eval('trabSituacion'),'pens')
						)
					)
		})
	trabInfantil = fields.Boolean('Trabajo infantil',
		states = {'invisible': 

		Or(Equal(Eval('trabSituacion'),'no'),Equal(Eval('trabSituacion'),'bus'),
				Equal(Eval('trabSituacion'),'jub'),
				Equal(Eval('trabSituacion'),'pens')
			)
		})
	trabJuvenil = fields.Boolean('Trabajo juvenil',
		states = {'invisible': 

		Or(Equal(Eval('trabSituacion'),'no'),Equal(Eval('trabSituacion'),'bus'),
				Equal(Eval('trabSituacion'),'jub'),
				Equal(Eval('trabSituacion'),'pens')
			)
		})
	trabLegal = fields.Boolean('Trabajo legalizado',
		states = {'invisible': 

		Or(Equal(Eval('trabSituacion'),'no'),Equal(Eval('trabSituacion'),'bus'),
				Equal(Eval('trabSituacion'),'jub'),
				Equal(Eval('trabSituacion'),'pens')
			)
		})
	trabInsalubre = fields.Boolean('Trabajo insalubre',
		states = {'invisible': 

		Or(Equal(Eval('trabSituacion'),'no'),Equal(Eval('trabSituacion'),'bus'),
				Equal(Eval('trabSituacion'),'jub'),
				Equal(Eval('trabSituacion'),'pens')
			)
		})
	trabTipoRel = fields.Selection([('pub',u'Empleado Público'),('priv','Empleado Privado'),('indep','Empleado Independiente'),('otro','Otro')],u'Tipo de Relación',
		states = {'invisible': 

		Or(Equal(Eval('trabSituacion'),'no'),Equal(Eval('trabSituacion'),'bus'),
				Equal(Eval('trabSituacion'),'jub'),
				Equal(Eval('trabSituacion'),'pens')
			),
		'required':
					Not(
						Or( 
							Equal(Eval('trabSituacion'),'no'),
							Equal(Eval('trabSituacion'),'bus'),
							Equal(Eval('trabSituacion'),'jub'),
							Equal(Eval('trabSituacion'),'pens')
						)
					)
		})
	trabObs = fields.Text('Observaciones',
		states = {'invisible': 

		Or(Equal(Eval('trabSituacion'),'no'),Equal(Eval('trabSituacion'),'bus'),
				Equal(Eval('trabSituacion'),'jub'),
				Equal(Eval('trabSituacion'),'pens')
			)
		})

	trabPadre = fields.Selection([('trab','Trabaja'),('bus','Busca por primera vez'),('no','No trabaja'),('pas',u'Pasantía'),('pens','Pensionista'),('jub','Jubilado')],u'Situación Laboral del Padre')
	trabMadre = fields.Selection([('trab','Trabaja'),('bus','Busca por primera vez'),('no','No trabaja'),('pas',u'Pasantía'),('pens','Pensionista'),('jub','Jubilado')],u'Situación Laboral de la Madre')
	trabPareja = fields.Selection([('trab','Trabaja'),('bus','Busca por primera vez'),('no','No trabaja'),('pas',u'Pasantía'),('pens','Pensionista'),('jub','Jubilado')],u'Situación Laboral de la Pareja')

#	formulario = fields.One2One('cefiro.auxformvivtrabajo','formvivtrabid','formid','Formulario')

FormularioViviendaTrabajo()

class AuxFormVivTrabajo(ModelSQL):
	'AuxFormVivTrabajo'
	_name = 'cefiro.auxformvivtrabajo'
	_description = __doc__
	
	formulario = fields.Many2One('cefiro.formulario','Formulario',select=1)
	formvt = fields.Many2One('cefiro.formvt','Formvt',select=1)

	def __init__(self):

		super(AuxFormVivTrabajo, self).__init__()

		self._sql_constraints += [
			('origin_unique', 'UNIQUE(formulario)','Origin must be unique'),
			('target_unique', 'UNIQUE(formvt)','Target must be unique'),
		]

AuxFormVivTrabajo()