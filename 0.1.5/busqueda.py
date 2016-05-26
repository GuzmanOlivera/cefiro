# -*- coding: utf-8 -*-
from trytond.model import ModelView, ModelSQL, ModelSingleton, fields

from dateutil.relativedelta import relativedelta
from datetime import datetime, date
from trytond.pool import Pool
from trytond.res import User

class Busqueda(ModelSQL,ModelView):
	'Busqueda'
	_name = 'cefiro.busqueda'
	_description = __doc__

Busqueda()
