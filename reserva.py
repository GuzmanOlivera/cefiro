# -*- coding: utf-8 -*-
from trytond.model import ModelView, ModelSQL, ModelSingleton, fields

from dateutil.relativedelta import *#relativedelta
from datetime import * #datetime, date
from trytond.pool import Pool
from trytond.res import User
from trytond.pyson import Eval, If, DateTime
from cefiro import *


class Reserva(ModelSQL,ModelView):
	'Reserva'
	_name = 'cefiro.reserva'
	name = fields.Char(u'Descripción de la reserva')

	libres = []
	dtini = [] #fechas de inicio de consulta (datetime)
	dtfin = [] #fechas de fin de consulta (datetime)

	psicologos = fields.Many2Many('cefiro.reservapsic','reserva','psicologo',u'Psicólogos',required=True)
	estudiantes = fields.Many2Many('cefiro.reservaest','reserva','estudiante','Estudiantes')

	fechaini = fields.Date('Fecha de inicio',required=True)
	fechaFin = fields.Date('Fecha de fin',required=True)
	diaSemana = fields.Selection([('0','Lunes'),('1','Martes')],'Dia de la semana',required=True)
	horaIni = fields.Time('Hora de inicio',required=True)
	horaFin = fields.Time('Hora de fin',required=True)

	consulLibres = fields.Function(fields.One2Many('cefiro.consultorio',None,'Consultorios libres',on_change_with=['fechaini','fechaFin','diaSemana','horaIni','horaFin']),'get_libres')

	consultorio = fields.Many2One('cefiro.consultorio','Consultorio',required=True,domain=[('id','in',Eval('consulLibres'))])

	confirmacion = fields.Function(fields.Char('Consultas reservadas'),'mensajeRes','reservador') #Esta funcion es llamada cuando se guarda la reserva, y vi que era bueno :)

	def mensajeRes(self,ids,name):
		return u'¡Reserva exitosa!'

	def reservador(self,ids,name,value):
		obj_consulta = Pool().get('cefiro.consulta')

		for reser in self.browse(ids):
			for i in range(len(reser.dtini)):
				obj_consulta.create({'horaini':reser.dtini[i],'horaFin':reser.dtfin[i],'consultorio':reser.consultorio,'psicologos':[]})
		return res


#Una funcion muy linda, que da una lista de tiempos iniciales y finales (datetime) para un rango de fechas, día de la semana y horarios.
#Devuelve dos listas con horarios iniciales y finales
	def tiempos(self,d1,d2,diaBuscado,horaini,horafin):
		ti = []
		tf= []
		buscados=[]
		d=d1
		#Primero busco el primer dia buscado del periodo
		while d.weekday()!= diaBuscado:
			d=d+timedelta(1)
	
		#Ahora listo todos los dias buscados del periodo
		while d<=d2:
			buscados.append(d)
			d=d+timedelta(7)
			ti.append(datetime.combine(d,horaini))
			tf.append(datetime.combine(d,horafin))
		return [ti,tf]
#-----------------Fin tiempos---------------------------

	def get_libres(self,ids,name):
		res = {}
		objConsul = Pool().get('cefiro.consultorio')
		for elem in self.browse(ids):
			res[elem.id] = elem.libres
		return res


	def on_change_with_consulLibres(self,values):
		res=[]
		d1 = values.get('fechaini')
		d2 = values.get('fechaFin')
		diaBuscado = values.get('diaSemana')
		hini = values.get('horaIni')
		hfin = values.get('horaFin')

		#if d==str(i1.weekday()):
		#	return [1]

		#Chequeo que la entrada sea correcta
		if (((d1==None) or (d2==None) or (diaBuscado==None)) or (type(hini)!=time) or (type(hfin)!=time)):
			return [1]#res
		else:
			if((d2 < d1) or ((d1==d2) and (horafin < horaini))):
				return [2]#res

		#Consigo los límites de tiempos que necesito
		diaBuscInt=int(diaBuscado)
		[tini,tfin] = self.tiempos(d1,d2,diaBuscInt,hini,hfin)

		self.dtini = tini
		self.dtfin = tfin

		objConsultorio = Pool().get('cefiro.consultorio')
		objConsulta = Pool().get('cefiro.consulta')
		consultoriosTotId = objConsultorio.search([])
		for cons in objConsultorio.browse(consultoriosTotId):
			estaVacio = True
			consultasIDs = cons.consultas
			
			listaDic = objConsulta.read(consultasIDs)
			for dic in listaDic:
				i2=dic.get('fechaini')
				f2=dic.get('fechaFin')
				for ind in range(len(tini)):
					i1=tini[ind]
					f1=tfin[ind]
					if not((f2<i1) or (f1<i2)):
						estaVacio = False
			if estaVacio:
				res.append(cons.id)

		self.libres = res		

		return res

Reserva()


class ReservaPsic(ModelSQL):
	'ReservaPsic'
	_name = 'cefiro.reservapsic'
	_description = __doc__
	reserva = fields.Many2One('cefiro.reserva','Reserva de horarios',select=1)
	psicologo = fields.Many2One('cefiro.psicologo','Psicologo',select=1)

ReservaPsic()

class ReservaEst(ModelSQL):
	'ReservaEst'
	_name = 'cefiro.reservaest'
	_description = __doc__
	reserva = fields.Many2One('cefiro.reserva','Reserva de horarios',select=1)
	estudiante = fields.Many2One('cefiro.estudiante','Estudiante',select=1)

ReservaEst()