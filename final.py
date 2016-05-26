# -*- coding: utf-8 -*-
from trytond.model import ModelView, ModelSQL, ModelSingleton, fields

from dateutil.relativedelta import relativedelta
from datetime import datetime, date
from trytond.pool import Pool
from trytond.res import User

from cefiro import *

class Final(ModelSQL,ModelView):
	'Final'
	_name = 'cefiro.final'
	_description = __doc__
	_rec_name = 'fechaini'
	_history = True

#	name = fields.Char('Nombre')

	entreFam = fields.Boolean('Entrevistas con familiares')
	testMachover = fields.Boolean('Machover')
	testHTP = fields.Boolean('HTP')
	test8f = fields.Boolean('8 Figuras')
	testLluvia = fields.Boolean('Persona bajo la lluvia')
	testRorscharch = fields.Boolean('Rorscharch')
	testTAT = fields.Boolean('TAT')
	testPhilipson = fields.Boolean('Philipson')
	testWAISC = fields.Boolean('WAISC')
	testBender = fields.Boolean('Bender')
	testSCHL = fields.Boolean('SCHL')
	testSPC = fields.Boolean('SPC')

	interPsiq = fields.Boolean('Psiquiatra')
	interMed = fields.Boolean(u'Médico')
	interPiscop = fields.Boolean('Psicopedagogo')
	interFono = fields.Boolean(u'Fonoaudiólogo')
	interNutri = fields.Boolean(u'Nutrición')
	interEdu = fields.Boolean(u'Educativas')
	interJudi = fields.Boolean(u'Judiciales')
	interInstPsiq = fields.Boolean(u'Psiquiátricas')
	interOtras = fields.Boolean(u'Otras')

	interconPsiq = fields.Boolean('Psiquiatra')
	interconMed = fields.Boolean(u'Médico')
	interconPiscop = fields.Boolean('Psicopedagogo')
	interconFono = fields.Boolean(u'Fonoaudiólogo')
	interconNutri = fields.Boolean(u'Nutrición')

	deriFac = fields.Boolean(u'A servicio de Facultad de Psicología')
	deriOtro = fields.Boolean(u'A otros servicios')

	sintesis = fields.Text(u'Síntesis')

	fechaini = fields.Date(u'Inicio de Intervención')
	fechaFin = fields.Date(u'Cierre de Intervención')
	asisTot = fields.Integer(u'Número de asistencias')
	inasisTot = fields.Integer(u'Número de inasistencias')
	grupal = fields.Boolean('Historia Grupal')

	paciente = fields.Many2One('cefiro.paciente','Paciente')

Final()
