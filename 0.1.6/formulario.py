# -*- coding: utf-8 -*-
from trytond.model import ModelView, ModelSQL, ModelSingleton, fields

from dateutil.relativedelta import relativedelta
from datetime import datetime, date
from trytond.pool import Pool
from trytond.res import User

from cefiro import *


class Formulario(ModelSQL,ModelView):
	'Formulario'
	_name = 'cefiro.formulario'
	_description = __doc__
	_rec_name = 'fecha'
#	name = fields.Char('Nombre del paciente')

	#Paciente Asociado y datos autocompletados. Implementar esto. Tema de las edades (el paciente tiene una edad actual, y va yendo a consultas con distintas edades).
	paciente = fields.Many2One('cefiro.paciente','Paciente')

	#Tipo de consulta
	fecha = fields.Date('Fecha de consulta inicial',required=True)
	tipoConsulta = fields.Selection([('esp',u'Consulta espontánea'),('tra',u'Traído'),('ori',u'Consulta por orientación'),('der','Derivado')],'Tipo de Consulta')
	derivador = fields.Selection([('med',u'Especialidad Médica'),('psiq','Psiquiatra'),('edu',u'Institución Educativa'),('otra','Otra')],'Derivado por')
	derivEspec = fields.Char('Especifique')

	#Motivo de consulta
	motivoPaciente1 = fields.Char(u'Motivo según el paciente (1)')
	motivoPaciente1Cod = fields.Char(u'Código')
	motivoPaciente2 = fields.Char(u'Motivo según el paciente (2)')
	motivoPaciente2Cod = fields.Char(u'Código')
	motivoPaciente3 = fields.Char(u'Motivo según el paciente (3)')
	motivoPaciente3Cod = fields.Char(u'Código')

	motivoAcompa1 = fields.Char(u'Motivo según el Acompañante (1)')
	motivoAcompa1Cod = fields.Char(u'Código')
	motivoAcompa2 = fields.Char(u'Motivo según el Acompañante (2)')
	motivoAcompa2Cod = fields.Char(u'Código')
	motivoAcompa3 = fields.Char(u'Motivo según el Acompañante (3)')
	motivoAcompa3Cod = fields.Char(u'Código')

	motivoPsico1 = fields.Char(u'Motivo según el Psicólogo (1)')
	motivoPsico1Cod = fields.Char(u'Código')
	motivoPsico2 = fields.Char(u'Motivo según el Psicólogo (2)')
	motivoPsico2Cod = fields.Char(u'Código')
	motivoPsico3 = fields.Char(u'Motivo según el Psicólogo (3)')
	motivoPsico3Cod = fields.Char(u'Código')

	motivoComplementaria = fields.Text(u'Descripción Comlpementaria')

	#Datos personales extra
	lugarNacimiento = fields.Char('Lugar de Nacimiento')

	#Vivienda y Trabajo
	tipoVivienda = fields.Selection([('casa','la casa'),('calle','la calle'),('inst',u'institución protectora'),('car','privado de libertad')],'Vive en')
	#convive = fields.One2Many() Hay que hacer uno para familiares posibles. Por ahora va un Selection.
	convive = fields.Selection([('solo','Vive solo'),('madre','Madre'),('padre','Padre'),('madra','Madrastra'),('padra','Padrastro'),('her','Hermano'),('pare','Pareja'),('hijo','Hijo'),('otros','Otros')],u'Con quién convive')
	situacionCony = fields.Selection([('sol',u'Soltero/a'),('casado',u'Casado/a (incluye separado/a sin divorcio)'),('divor',u'Divorciado/a'),('viudo',u'Viudo/a'),('ulibre',u'Unión libre'),('slibre',u'Separado de unión libre')],'Estado Conyugal')

	vivHabitaTot = fields.Integer('Habitaciones totales')
	vivHabitaDor = fields.Integer('Dormitorios')
	vivBanos = fields.Integer(u'Cantidad de Baños')
	vivBanoComp = fields.Boolean(u'Baño compartido')
	vivBanoTipo = fields.Selection([('red','Red general'),('fosa',u'Fosa séptica o pozo negro'),('otro',u'Otro (hueco en suelo, superficie)')],u'Tipo de instalación sanitaria')

	trabSituacion = fields.Selection([('trab','Trabaja'),('bus','Busca por primera vez'),('no','No trabaja'),('pas',u'Pasantía'),('pens','Pensionista'),('jub','Jubilado')],u'Situación Laboral')
	trabMulti = fields.Boolean('Multiempleo')
	trabHoras = fields.Integer('Horas Totales')
	trabHorasPrin = fields.Integer('Horas Trabajo Principal')
	trabInicio = fields.Integer('Edad de inicio de trabajo')
	trabInfantil = fields.Boolean('Trabajo infantil')
	trabJuvenil = fields.Boolean('Trabajo juvenil')
	trabLegal = fields.Boolean('Trabajo legalizado')
	trabInsalubre = fields.Boolean('Trabajo insalubre')
	trabTipoRel = fields.Selection([('pub',u'Empleado Público'),('priv','Empleado Privado'),('indep','Empleado Independiente'),('otro','Otro')],u'Tipo de Relación')
	trabObs = fields.Text('Observaciones')

	trabPadre = fields.Selection([('trab','Trabaja'),('bus','Busca por primera vez'),('no','No trabaja'),('pas',u'Pasantía'),('pens','Pensionista'),('jub','Jubilado')],u'Situación Laboral del Padre')
	trabMadre = fields.Selection([('trab','Trabaja'),('bus','Busca por primera vez'),('no','No trabaja'),('pas',u'Pasantía'),('pens','Pensionista'),('jub','Jubilado')],u'Situación Laboral de la Madre')
	trabPareja = fields.Selection([('trab','Trabaja'),('bus','Busca por primera vez'),('no','No trabaja'),('pas',u'Pasantía'),('pens','Pensionista'),('jub','Jubilado')],u'Situación Laboral de la Pareja')
	

	#Educación
	eduFormalNivel = fields.Selection([('no','No escolarizado'),('priInc','Primaria Incompleta'),('pri','Primaria Completa'),('secInc','Secundaria Incompleta'),('sec','Secundaria Completa'),('tercInc','Terciaria Incompleta'),('terc','Terciaria Completa'),('uniInc','Universitaria Incompleta'),('uni','Universitaria Completa')],u'Nivel de Educación Formal')
	eduFormalNivelMax = fields.Integer(u'Máximo año aprobado (en caso de no haber completado lo último que estudió)')

	eduCentrosPrimaria = fields.Char(u'Centros en los que estudió')
	eduPubliPrimaria = fields.Selection([('publi',u'Pública'),('priv','Privada')],u'Tipo de institución')
	eduDifPrimaria = fields.Boolean(u'Presentó dificultades de aprendizaje')
	eduDifTipoPrimaria = fields.Char(u'Tipo de dificultad que presentó')
	eduRepePrimaria = fields.Integer(u'Cantidad de años repetidos (si no hay dejar vacío)')
	eduRepeCausaPrimaria = fields.Char(u'Causa de la repetición de años')
	eduDeserPrimaria = fields.Boolean(u'Deserción o Exclusión')
	
	eduCentrosSecundaria = fields.Char(u'Centros en los que estudió')
	eduPubliSecundaria = fields.Selection([('publi',u'Pública'),('priv','Privada')],u'Tipo de institución')
	eduDifSecundaria = fields.Boolean(u'Presentó dificultades de aprendizaje')
	eduDifTipoSecundaria = fields.Char(u'Tipo de dificultad que presentó')
	eduRepeSecundaria = fields.Integer(u'Cantidad de años repetidos (si no hay dejar vacío)')
	eduRepeCausaSecundaria = fields.Char(u'Causa de la repetición de años')
	eduDeserSecundaria = fields.Boolean(u'Deserción o Exclusión')

	eduCentrosTerciaria = fields.Char(u'Centros en los que estudió')
	eduPubliTerciaria = fields.Selection([('publi',u'Pública'),('priv','Privada')],u'Tipo de institución')

	eduCentrosUniv = fields.Char(u'Centros en los que estudió')
	eduPubliUniv = fields.Selection([('publi',u'Pública'),('priv','Privada')],u'Tipo de institución')

	eduNoForCurso1 = fields.Char('Curso')
	eduNoForCentro1 = fields.Char('Centro')
	eduNoForPubli1 = fields.Selection([('publi',u'Pública'),('priv','Privada')],u'Tipo de institución')
	eduNoForAsis1 = fields.Selection([('actual','Asiste'),('pasado',u'Asistió')],'Momento')

	eduNoForCurso2 = fields.Char('Curso')
	eduNoForCentro2 = fields.Char('Centro')
	eduNoForPubli2 = fields.Selection([('publi',u'Pública'),('priv','Privada')],u'Tipo de institución')
	eduNoForAsis2 = fields.Selection([('actual','Asiste'),('pasado',u'Asistió')],'Momento')

	eduNoForCurso3 = fields.Char('Curso')
	eduNoForCentro3 = fields.Char('Centro')
	eduNoForPubli3 = fields.Selection([('publi',u'Pública'),('priv','Privada')],u'Tipo de institución')
	eduNoForAsis3 = fields.Selection([('actual','Asiste'),('pasado',u'Asistió')],'Momento')

	eduPadre = fields.Selection([('no','No escolarizado'),('priInc','Primaria Incompleta'),('pri','Primaria Completa'),('secInc','Secundaria Incompleta'),('sec','Secundaria Completa'),('tercInc','Terciaria Incompleta'),('terc','Terciaria Completa'),('uniInc','Universitaria Incompleta'),('uni','Universitaria Completa')],u'Nivel de Educación Formal del Padre')

	eduMadre = fields.Selection([('no','No escolarizado'),('priInc','Primaria Incompleta'),('pri','Primaria Completa'),('secInc','Secundaria Incompleta'),('sec','Secundaria Completa'),('tercInc','Terciaria Incompleta'),('terc','Terciaria Completa'),('uniInc','Universitaria Incompleta'),('uni','Universitaria Completa')],u'Nivel de Educación Formal de la Madre')

	eduPareja = fields.Selection([('no','No escolarizado'),('priInc','Primaria Incompleta'),('pri','Primaria Completa'),('secInc','Secundaria Incompleta'),('sec','Secundaria Completa'),('tercInc','Terciaria Incompleta'),('terc','Terciaria Completa'),('uniInc','Universitaria Incompleta'),('uni','Universitaria Completa')],u'Nivel de Educación Formal de la Pareja')


	#Antecedentes
	antPedagogica = fields.Selection([('conc',u'Concluida'),('aba','Abandonada'),('cur','En Curso')],u'Intervención Pedagógica')
	antPedagogicaPocas = fields.Boolean('Menos de 3 consultas')
	antPedagogicaMeses = fields.Integer(u'Duración en meses')
	antPedagogicaMedicacion = fields.Boolean(u'Medicación')
	antPedagogicaMedTipo = fields.Selection([('ansiolitico',u'Ansiolíticos'),('antidepre','Antidepresivos'),('neurolep',u'Neurolépticos'),('otro','Otros')],u'Tipo de Medicación')
	antPedagogicaObs = fields.Char(u'Motivo y Obs.')

	antMedica = fields.Selection([('conc',u'Concluida'),('aba','Abandonada'),('cur','En Curso')],u'Intervención Médica')
	antMedicaPocas = fields.Boolean('Menos de 3 consultas')
	antMedicaMeses = fields.Integer(u'Duración en meses')
	antMedicaMedicacion = fields.Boolean(u'Medicación')
	antMedicaMedTipo = fields.Selection([('ansiolitico',u'Ansiolíticos'),('antidepre','Antidepresivos'),('neurolep',u'Neurolépticos'),('otro','Otros')],u'Tipo de Medicación')
	antMedicaObs = fields.Char(u'Motivo y Obs.')

	antPsicologica = fields.Selection([('conc',u'Concluida'),('aba','Abandonada'),('cur','En Curso')],u'Intervención Psicológica')
	antPsicologicaPocas = fields.Boolean('Menos de 3 consultas')
	antPsicologicaMeses = fields.Integer(u'Duración en meses')
	antPsicologicaMedicacion = fields.Boolean(u'Medicación')
	antPsicologicaMedTipo = fields.Selection([('ansiolitico',u'Ansiolíticos'),('antidepre','Antidepresivos'),('neurolep',u'Neurolépticos'),('otro','Otros')],u'Tipo de Medicación')
	antPsicologicaObs = fields.Char(u'Motivo y Obs.')

	antPsiquiatrica = fields.Selection([('conc',u'Concluida'),('aba','Abandonada'),('cur','En Curso')],u'Intervención Psiquiátrica')
	antPsiquiatricaPocas = fields.Boolean('Menos de 3 consultas')
	antPsiquiatricaMeses = fields.Integer(u'Duración en meses')
	antPsiquiatricaMedicacion = fields.Boolean(u'Medicación')
	antPsiquiatricaMedTipo = fields.Selection([('ansiolitico',u'Ansiolíticos'),('antidepre','Antidepresivos'),('neurolep',u'Neurolépticos'),('otro','Otros')],u'Tipo de Medicación')
	antPsiquiatricaObs = fields.Char(u'Motivo y Obs.')

	antPsiqInter = fields.Selection([('conc',u'Concluida'),('aba','Abandonada'),('cur','En Curso')],u'Internación Psiquiátrica')
	antPsiqInterPocas = fields.Boolean('Menos de 3 consultas')
	antPsiqInterMeses = fields.Integer(u'Duración en meses')
	antPsiqInterMedicacion = fields.Boolean(u'Medicación')
	antPsiqInterMedTipo = fields.Selection([('ansiolitico',u'Ansiolíticos'),('antidepre','Antidepresivos'),('neurolep',u'Neurolépticos'),('otro','Otros')],u'Tipo de Medicación')
	antPsiqInterObs = fields.Char(u'Motivo y Obs.')

	antIntOtra = fields.Selection([('conc',u'Concluida'),('aba','Abandonada'),('cur','En Curso')],u'Otra')
	antIntOtraPocas = fields.Boolean('Menos de 3 consultas')
	antIntOtraMeses = fields.Integer(u'Duración en meses')
	antIntOtraMedicacion = fields.Boolean(u'Medicación')
	antIntOtraMedTipo = fields.Selection([('ansiolitico',u'Ansiolíticos'),('antidepre','Antidepresivos'),('neurolep',u'Neurolépticos'),('otro','Otros')],u'Tipo de Medicación')
	antIntOtraObs = fields.Char(u'Motivo y Obs.')


	antDisca = fields.Boolean(u'Tiene algún tipo de discapacidad')
	antDiscaTipo = fields.Char('Tipo')	
	antAyudaTec = fields.Boolean(u'Utiliza algún tipo de ayuda técnica')
	antAyudaTecLentes = fields.Boolean(u'Lentes')
	antAyudaTecBaston = fields.Boolean(u'Bastón')
	antAyudaTecAudifono = fields.Boolean(u'Audífono')
	antAyudaTecOtro = fields.Boolean(u'Otro')
	antAyudaTecObs = fields.Char('Obs.')

	antPrestacion = fields.Boolean(u'Beneficiario de prestación por discapacidad')
	antPrestPension = fields.Boolean(u'Pensión no contributiva')
	antPrestJubil = fields.Boolean(u'Jubilación por incapacidad')
	antPrestAsigDoble = fields.Boolean(u'Asignación doble')
	antPrestAyuda = fields.Boolean(u'Ayuda especial')
	antPrestEquidad = fields.Boolean(u'Plan de equidad')
	
	antCeguera = fields.Boolean(u'Ceguera y/o dism. de visión')
	antSordera = fields.Boolean(u'Sordera / hipoacusia')
	antMotriz = fields.Boolean(u'Ceguera y/o dism. de visión')
	antDependencia = fields.Boolean(u'Dependencia de otra persona')

	antAsma = fields.Boolean(u'Asma')
	antEpilepsia = fields.Boolean(u'Epilepsia')
	antDiabetes = fields.Boolean(u'Diabetes')
	antTiroides = fields.Boolean(u'Enf. Tiroidea')
	antCancer = fields.Boolean(u'Cáncer')
	antVIH = fields.Boolean(u'VIH/SIDA')
	antOsteo = fields.Boolean(u'Pat. Osteoarticular')
	antCardio = fields.Boolean(u'Enf. Cardiovascular')

	antAccidente1Edad = fields.Integer('Edad')
	antAccidente1Tipo = fields.Char('Tipo')
	antAccidente2Edad = fields.Integer('Edad')
	antAccidente2Tipo = fields.Char('Tipo')
	antCirugia1Edad = fields.Integer('Edad')
	antCirugia1Tipo = fields.Char('Tipo')
	antCirugia2Edad = fields.Integer('Edad')
	antCirugia2Tipo = fields.Char('Tipo')

	antAutoeliminCant = fields.Integer(u'Cantidad de intentos de autoeliminación')
	antAutoelim1Edad = fields.Integer('Edad')
	antAutoelim1Tipo = fields.Char('Tipo')
	antAutoelim2Edad = fields.Integer('Edad')
	antAutoelim2Tipo = fields.Char('Tipo')


	#Violencia y Uso de Sustancias
	tvioDanoPsico = u'¿Su pareja o alguien importante para usted le ha causado daño emocional o psicológico en forma repetida?\n (Por ej.: por medio de alguna de las siguientes situaciones: insultos, maltrato a sus hijos, hacerlo/a\n sentir avergonzado/a o humillado/a desprecio por las tareas que usted realiza, destrucción de objetos\n de amigos o parientes, otras.)'
	vioDanoPsico = fields.Selection([('si',u'Sí'),('no','No'),('nc','No desea contestar')],tvioDanoPsico)
	vioDanoPsicoQuien = fields.Char(u'¿Quién/es lo hizo/cieron?')
	vioDanoPsicoNino = fields.Boolean(u'Niño/a')
	vioDanoPsicoAdoles = fields.Boolean(u'Adolescente')
	vioDanoPsicoJoven = fields.Boolean(u'Joven')
	vioDanoPsicoAdulto = fields.Boolean(u'Adulto/a')
	vioDanoPsicoMayor = fields.Boolean(u'Mayor de 65')
	vioDanoPsicoEmbarazo = fields.Boolean(u'Embarazo/postparto')
	vioDanoPsicoActual = fields.Selection([('si',u'Sí'),('no','No'),('nc','No desea contestar')],u'¿Sucede actualmente?')

	tvioDanoFisico = u'¿Su pareja o alguien importante para usted le ha causado daño físico grave al menos una vez, o le ha hecho agresiones menores en forma reiterada?\n (Por ej.: empujones, golpe de puños, quemaduras, zamarreos, mordeduras, ahorcamiento, pellizcos, palizas, golpes con objetos,\n tirón de pelo, patadas, daño con armas, cachetadas, otra forma.)'
	vioDanoFisico = fields.Selection([('si',u'Sí'),('no','No'),('nc','No desea contestar')],tvioDanoFisico)
	vioDanoFisicoQuien = fields.Char(u'¿Quién/es lo hizo/cieron?')
	vioDanoFisicoNino = fields.Boolean(u'Niño/a')
	vioDanoFisicoAdoles = fields.Boolean(u'Adolescente')
	vioDanoFisicoJoven = fields.Boolean(u'Joven')
	vioDanoFisicoAdulto = fields.Boolean(u'Adulto/a')
	vioDanoFisicoMayor = fields.Boolean(u'Mayor de 65')
	vioDanoFisicoEmbarazo = fields.Boolean(u'Embarazo/postparto')
	vioDanoFisicoActual = fields.Selection([('si',u'Sí'),('no','No'),('nc','No desea contestar')],u'¿Sucede actualmente?')


	tvioDanoSexual = u'¿Cuando usted era niño/a recuerda haber sido tocado/a de manera inapropiada por alguien o haber tenido relaciones o contacto sexual?'
	vioDanoSexual = fields.Selection([('si',u'Sí'),('no','No'),('nc','No desea contestar')],tvioDanoSexual)
	vioDanoSexualQuien = fields.Char(u'¿Quién/es lo hizo/cieron?')


	tvioViola = u'¿Alguna vez en su vida ha sido obligado/a a tener relaciones o contacto sexual?\n (Por ej.: empleo de la fuerza física, de intimidación o amenaza para mantener relaciones sexuales no deseadas.)'
	vioViola = fields.Selection([('si',u'Sí'),('no','No'),('nc','No desea contestar')],tvioViola)
	vioViolaQuien = fields.Char(u'¿Quién/es lo hizo/cieron?')
	vioViolaNino = fields.Boolean(u'Niño/a')
	vioViolaAdoles = fields.Boolean(u'Adolescente')
	vioViolaJoven = fields.Boolean(u'Joven')
	vioViolaAdulto = fields.Boolean(u'Adulto/a')
	vioViolaMayor = fields.Boolean(u'Mayor de 65')
	vioViolaEmbarazo = fields.Boolean(u'Embarazo/postparto')
	vioViolaActual = fields.Selection([('si',u'Sí'),('no','No'),('nc','No desea contestar')],u'¿Sucede actualmente?')


	vioPensamiento = fields.Selection([('si',u'Sí'),('no','No'),('nc','No desea contestar')],u'Hoy, en su casa, ¿piensa usted que podría sufrir alguna de las situaciones antes nombradas?')


	tsustAlcohol = u'Durante los últimos 30 días, ¿con qué frecuencia usted bebió al menos 4 medidas de cualquier\n clase de bebida con alcohol en un mismo día?'
	sustAlcohol = fields.Selection([('nunca','Nunca'),('unames','Una vez al mes'),('dosmes','2 o 3 veces al mes'),('unasemana','Una vez a la semana'),('dossemana',u'2 dóas a la semana o más')],tsustAlcohol)
	tsustCigarro = u'Durante los últimos 30 días, ¿con qué frecuencia usted fumó cigarrillos, tabaco o pipa?'
	sustCigarro = fields.Selection([('nunca','Nunca'),('unames','Una vez al mes'),('dosmes','2 o 3 veces al mes'),('unasemana','Una vez a la semana'),('dossemana',u'2 dóas a la semana o más')],tsustCigarro)
	tsustMedicamento = u'Durante los últimos 30 días, ¿con qué frecuencia usted usó algunos de los siguientes medicamentos \n POR SU CUENTA (esto es sin una receta de su médico o en cantidades mayores a las recetadas)?\n Medicamentos para el dolor como tramadol o morfina, estimulantes como ritalina, tranquilizantes como Lexotán.'
	sustMedicamento = fields.Selection([('nunca','Nunca'),('unames','Una vez al mes'),('dosmes','2 o 3 veces al mes'),('unasemana','Una vez a la semana'),('dossemana',u'2 dóas a la semana o más')],tsustMedicamento)
	tsustDroga = u'Durante los últimos 30 días, ¿con qué frecuencia usted usó algunas de las siguientes sustancias:\n Marihuana, Cocaína, Pasta Base, Crack, Estimulantes como éxtasis, Halucinógenos como hongos o LSD,\n Heroína, Inhalantes como pegamento?'
	sustDroga = fields.Selection([('nunca','Nunca'),('unames','Una vez al mes'),('dosmes','2 o 3 veces al mes'),('unasemana','Una vez a la semana'),('dossemana',u'2 dóas a la semana o más')],tsustDroga)

Formulario()

