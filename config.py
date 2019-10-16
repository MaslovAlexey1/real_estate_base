import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
		'sqlite:///' + os.path.join(basedir, 'app.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	# The absolute path of the directory containing images for users to download
	CLIENT_IMAGES = os.path.join(basedir, '/static/client/img')

	DICT = {'object_type': 
				{
					-1: -1, 
					1: 'Квартира', 
					2: 'Апартамент',
					3: 'Машино-место',
					4: 'Кладовка', 
					5: 'Нежилое', 
					6: 'Кв/ап'
				},
            'decoration': 
				{
					-1: -1,
					0: '0 - Нет',
					1: '1 - Есть',
					3: '3 - Неизвестно'
				},
            'is_studio':
        		{
					-1: -1,
					1: 'Студия'
				},
            'house_class':
        		{
					-1: -1,
					1: 'комфорт',
					2: 'премиум',
					3: 'де-люкс',
					4: 'бизнес',
					5: 'эконом',
					6: 'эконом (панель)'
				},
            'agreement':
          		{
					-1: -1,
					1: 'ДДУ',
					2: 'ДКП',
					3: 'ПДКП',
					4: 'ЖСК',
					5: 'Аукцион'
                },
            'stage':
          		{
					-1: -1,
					1: 'сдан_ГК',
					2: 'идёт отделка',
					3: 'котлован',
					4: 'верхние этажи',
					5: 'нижние этажи',
					6: 'Заморожен'
                },
            'zone':
          		{
					-1: -1,
					1: '1) внутри СК',
					2: '2) от СК до ~ТТК',
					3: '3) от ~ТТК до МКАД',
					4: '4) Москва за МКАД',
					5: '5) Н. Москва ближ.',
					6: '6) Н. Москва дальн.',
					7: '7) МО ближ.',
					8: '8) МО ср.',
					9: '9) МО дальн.'
                }
			}
