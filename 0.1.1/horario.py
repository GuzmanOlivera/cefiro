# -*- coding: utf-8 -*-
from trytond.model import ModelView, ModelSQL, ModelSingleton, fields

from cefiro import *

class Horario(ModelSQL,ModelView):
	'Horario'
	_name = 'cefiro.horario'
	_description = __doc__
	name = fields.Char('nombre')

	diaDeSemana = fields.Selection([('lun','Lunes'),('mar','Martes'),('mier',u'Miércoles'),('jue','Jueves'),('vie','Viernes'),('sab',u'Sábado'),('dom','Domingo')],u'Día')
	hora = fields.Time('Hora')

Horario()





