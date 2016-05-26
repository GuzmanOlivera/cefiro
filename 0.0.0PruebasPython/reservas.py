# -*- coding: utf-8 -*-
from dateutil.relativedelta import *
from datetime import *

ti = []
tf= []

diaBuscado = 4 #Viernes
horaini = time(16)
horafin = time(17,30)
d1 = date(1993,9,6)
d2 = date(1993,10,7)

def tiempos(d1,d2,diaBuscado,horaini,horafin):
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
	print buscados
	print ti
	print tf
	return ti,tf


tiempos(d1,d2,diaBuscado,horaini,horafin)

