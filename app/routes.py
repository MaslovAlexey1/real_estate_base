from sqlalchemy.orm import sessionmaker
from sqlalchemy import text, create_engine
from matplotlib.ticker import FuncFormatter
from flask import Flask, escape, request, render_template, flash, redirect, url_for, send_file
from app import app
from app.forms import LoginForm
from app.models import Developer, HousingComplex, House, Object, RegionCity, DistrictDirection, Atd
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
from io import StringIO
import io
import seaborn as sns
sns.set()

@app.route('/')
@app.route('/index')
def index():
	developer = Developer.query.all()

	return render_template('index.html',
                        developer=developer
                        )


@app.route('/developer/')
@app.route('/developer/<developer_id>')
def developer(developer_id=-1):
	if developer_id == -1 :
		developer = Developer.query.all()
		return render_template('index.html', developer=developer
                         )

	developer = Developer.query.get(developer_id)

	housing_complex = HousingComplex.query.filter_by(developer_id=developer_id)

	return render_template('developer.html',
							developer = developer,
                        	housing_complex=housing_complex
	)


@app.route('/housing_complex/')
@app.route('/housing_complex/<housing_complex_id>')
def housing_complex(housing_complex_id=-1):
	if housing_complex_id == -1:
		region_city = RegionCity.query.all()
		district_direction = DistrictDirection.query.all()
		atd = Atd.query.all()

		zone = request.args.get('zone')
		zone = int(zone) if zone is not None else -1
		zone = app.config['DICT']['zone'][zone]

		region_city_id = request.args.get('rcity')
		region_city_id = int(region_city_id) if region_city_id is not None else -1

		district_direction_id = request.args.get('dd')
		district_direction_id = int(
			district_direction_id) if district_direction_id is not None else -1

		atd_id = request.args.get('atd')
		atd_id = int(atd_id) if atd_id is not None else -1

		if zone != -1:
			housing_complex = HousingComplex.query.filter_by(zone=zone)
		elif region_city_id != -1:
			housing_complex = HousingComplex.query.filter_by(region_city_id=region_city_id)
		elif district_direction_id != -1:
			housing_complex = HousingComplex.query.filter_by(district_direction_id=district_direction_id)
		elif atd_id != -1:
			housing_complex = HousingComplex.query.filter_by(atd_id=atd_id)
		else:
			housing_complex = HousingComplex.query.limit(100)

		
		return render_template('housing_complex_filter.html',
                         housing_complex=housing_complex,
                         region_city=region_city,
                         district_direction=district_direction,
                         atd=atd
                         )
	else:
		housing_complex = HousingComplex.query.get(housing_complex_id)
		house = House.query.filter_by(housing_complex_id=housing_complex_id)
		developer = Developer.query.get(housing_complex.developer_id)
		return render_template('housing_complex.html',
						developer = developer,
                        housing_complex=housing_complex,
                        house=house
                        )


@app.route('/house/')
@app.route('/house/<house_id>')
def house(house_id=-1):
	if house_id == -1:
		house = House.query.limit(100)
		return render_template('house_filter.html',
                         house=house
                         )
	else:
		house = House.query.get(house_id)

		object = Object.query.filter_by(house_id=house_id)

		housing_complex = HousingComplex.query.get(house.housing_complex_id)
		developer = Developer.query.get(housing_complex.developer_id)

		return render_template('house.html',
							developer=developer,
							housing_complex=housing_complex,
							house=house,
							object=object
							)

@app.route('/real_estate_base/analytics/')
def real_estate_base():
	conn = 'sqlite:///app.db'
	developer = Developer.query.all()
	region_city = RegionCity.query.all()
	district_direction = DistrictDirection.query.all()
	atd = Atd.query.all()

	developer_id = request.args.get('dev')
	developer_id = int(developer_id) if developer_id is not None else 0

	housing_complex_id = request.args.get('hc')
	housing_complex_id = int(housing_complex_id) if housing_complex_id is not None else 0

	house_id = request.args.get('h')
	house_id = int(house_id) if house_id is not None else 0

	object_type = request.args.get('ot')
	object_type = int(object_type) if object_type is not None else -1
	object_type = app.config['DICT']['object_type'][object_type]
	
	room = request.args.get('r')
	room = int(room) if room is not None else -1

	decoration = request.args.get('dec')
	decoration = int(decoration) if decoration is not None else -1
	decoration = app.config['DICT']['decoration'][decoration]


	price_min = request.args.get('price_min')
	price_min = int(price_min) if price_min is not None else -1
	price_max = request.args.get('price_max')
	price_max = int(price_max) if price_max is not None else -1

	square_min = request.args.get('square_min')
	square_min = int(square_min) if square_min is not None else -1
	square_max = request.args.get('square_max')
	square_max = int(square_max) if square_max is not None else -1

	is_studio = request.args.get('is_studio')
	is_studio = int(is_studio) if is_studio is not None else -1
	is_studio = app.config['DICT']['is_studio'][is_studio]

	house_class = request.args.get('hclass')
	house_class = int(house_class) if house_class is not None else -1
	house_class = app.config['DICT']['house_class'][house_class]

	agreement = request.args.get('agr')
	agreement = int(agreement) if agreement is not None else -1
	agreement = app.config['DICT']['agreement'][agreement]

	stage = request.args.get('stage')
	stage = int(stage) if stage is not None else -1
	stage = app.config['DICT']['stage'][stage]

	zone = request.args.get('zone')
	zone = int(zone) if zone is not None else -1
	zone = app.config['DICT']['zone'][zone]

	region_city_id = request.args.get('rcity')
	region_city_id = int(region_city_id) if region_city_id is not None else -1
	
	district_direction_id = request.args.get('dd')
	district_direction_id = int(district_direction_id) if district_direction_id is not None else -1

	atd_id = request.args.get('atd')
	atd_id = int(atd_id) if atd_id is not None else -1

	sql_select = 'select o.id, o.developer_id, o.room, o.square, o.price, \
	o.price_meter, o.floor, o.floor_number, o.house_number, o.section_number, \
	o.type_studio, o.type, o.decoration, o.price_discont, o.housing_complex_id, o.house_id, h.name house_name, \
	h.house_class, h.agreement house_agreement, h.date_complete, h.stage, \
	h.address, hc.name hc_name, hc.region_city, hc.zone, hc.lat, hc.lng, d.name dev_name \
	from object o '
	sql_join_house = ' join house h on o.house_id = h.id '
	sql_join_housing_complex = ' join housing_complex hc on o.housing_complex_id = hc.id '
	sql_join_dev = ' join developer d on o.developer_id = d.id  '
	sql_where_1_1 = ' where 1=1 '
	sql_room = ' and o.room = ' + str(room) if room >= 0 else ''
	sql_object_type = ' and o.type = "' + str(object_type) + '"' if object_type != -1 else ''
	sql_decoration = ' and o.decoration = "' + str(decoration) + '"' if decoration != -1 else ''
	sql_price_min = ' and o.price >= ' + str(price_min) if price_min != -1 else ''
	sql_price_max = ' and o.price <= ' + str(price_max) if price_max != -1 else ''
	sql_square_min = ' and o.square >= ' + str(square_min) if square_min != -1 else ''
	sql_square_max = ' and o.square <= ' + str(square_max) if square_max != -1 else ''
	sql_is_studio = ' and o.type_studio = "' + str(is_studio) + '"' if is_studio != -1 else ''
	sql_dev_hc_h = ' '
	sql_hclass = ' and h.house_class = "' + str(house_class) + '"' if house_class != -1 else ''
	sql_agreement = ' and h.agreement = "' + str(agreement) + '"' if agreement != -1 else ''
	sql_stage = ' and h.stage = "' + str(stage) + '"' if stage != -1 else ''
	sql_zone = ' and hc.zone = "' + str(zone) + '"' if zone != -1 else ''
	sql_region_city = ' and hc.region_city_id = ' + str(region_city_id) if region_city_id != -1 else ''
	sql_district_direction = ' and hc.district_direction_id = ' + str(district_direction_id) if district_direction_id != -1 else ''
	sql_atd = ' and hc.atd_id = ' + str(atd_id) if atd_id != -1 else ''
	sql_limit = ' limit 20 '
	sql_order = ' '

	if developer_id == 0:
		housing_complex = HousingComplex.query.all()
		house = House.query.filter_by().all()
		sql_order = ' order by random() ' 
	elif housing_complex_id == 0:
		housing_complex = HousingComplex.query.filter_by(developer_id=developer_id).all()
		house = House.query.filter_by(developer_id=developer_id).all()
		sql_dev_hc_h = ' and o.developer_id=' + str(developer_id)
	elif house_id == 0:
		housing_complex = HousingComplex.query.filter_by(developer_id=developer_id).all()
		house = House.query.filter_by(housing_complex_id=housing_complex_id).all()
		sql_dev_hc_h = ' and o.housing_complex_id=' + str(housing_complex_id)
	elif house_id != 0:
		housing_complex = HousingComplex.query.filter_by(developer_id=developer_id).all()
		house = House.query.filter_by(housing_complex_id=housing_complex_id).all()
		sql_dev_hc_h = ' and o.house_id=' + str(house_id)

	sql_query = sql_select + sql_join_house + sql_join_housing_complex + sql_join_dev + sql_where_1_1 + sql_object_type + sql_room + sql_decoration + \
	            sql_price_min + sql_price_max + sql_square_min + sql_square_max + sql_is_studio + sql_dev_hc_h + \
				sql_hclass + sql_agreement + sql_stage + sql_zone + sql_region_city + sql_district_direction + sql_atd + sql_order + sql_limit

	Session = sessionmaker()
	engine = create_engine(conn)
	Session.configure(bind=engine)
	session = Session()
	object = session.execute(sql_query)


	return render_template('analytics.html', title='Real Estate Base',
		developer = developer,
		housing_complex = housing_complex,
		house = house,
		object = object,
		region_city = region_city,
		district_direction=district_direction,
		atd = atd
		)


@app.route('/square_price_scatter/')
def square_price_scatter():
	developer_id = request.args.get('dev')
	developer_id = int(developer_id) if developer_id is not None else 0

	housing_complex_id = request.args.get('hc')
	housing_complex_id = int(housing_complex_id) if housing_complex_id is not None else 0

	house_id = request.args.get('h')
	house_id = int(house_id) if house_id is not None else 0
	
	object_type = request.args.get('ot')
	object_type = int(object_type) if object_type is not None else -1
	object_type = app.config['DICT']['object_type'][object_type]

	room = request.args.get('r')
	room = int(room) if room is not None else -1

	decoration = request.args.get('dec')
	decoration = int(decoration) if decoration is not None else -1
	decoration = app.config['DICT']['decoration'][decoration]

	price_min = request.args.get('price_min')
	price_min = int(price_min) if price_min is not None else -1
	price_max = request.args.get('price_max')
	price_max = int(price_max) if price_max is not None else -1

	square_min = request.args.get('square_min')
	square_min = int(square_min) if square_min is not None else -1
	square_max = request.args.get('square_max')
	square_max = int(square_max) if square_max is not None else -1

	is_studio = request.args.get('is_studio')
	is_studio = int(is_studio) if is_studio is not None else -1
	is_studio = app.config['DICT']['is_studio'][is_studio]

	house_class = request.args.get('hclass')
	house_class = int(house_class) if house_class is not None else -1
	house_class = app.config['DICT']['house_class'][house_class]

	agreement = request.args.get('agr')
	agreement = int(agreement) if agreement is not None else -1
	agreement = app.config['DICT']['agreement'][agreement]

	stage = request.args.get('stage')
	stage = int(stage) if stage is not None else -1
	stage = app.config['DICT']['stage'][stage]

	zone = request.args.get('zone')
	zone = int(zone) if zone is not None else -1
	zone = app.config['DICT']['zone'][zone]

	region_city_id = request.args.get('rcity')
	region_city_id = int(region_city_id) if region_city_id is not None else -1

	district_direction_id = request.args.get('dd')
	district_direction_id = int(district_direction_id) if district_direction_id is not None else -1

	atd_id = request.args.get('atd')
	atd_id = int(atd_id) if atd_id is not None else -1

	fig, ax = plt.subplots(figsize=(10, 6))
	sql_select = 'select o.room, o.square, o.price, o.type from object o '
	sql_join_house = ' join house h on o.house_id = h.id '
	sql_join_housing_complex = ' join housing_complex hc on o.housing_complex_id = hc.id '
	sql_where_1_1 = ' where 1=1 '
	sql_room = ' and o.room = ' + str(room) if room >= 0 else ''
	sql_object_type = ' and o.type = "' + str(object_type) + '"' if object_type != -1 else ''
	sql_decoration = ' and o.decoration = "' + str(decoration) + '"' if decoration != -1 else ''
	sql_price_min = ' and o.price >= ' + str(price_min) if price_min != -1 else ''
	sql_price_max = ' and o.price <= ' + str(price_max) if price_max != -1 else ''
	sql_square_min = ' and o.square >= ' + str(square_min) if square_min != -1 else ''
	sql_square_max = ' and o.square <= ' + str(square_max) if square_max != -1 else ''
	sql_is_studio = ' and o.type_studio = "' + str(is_studio) + '"' if is_studio != -1 else ''
	sql_dev_hc_h = ' '
	sql_hclass = ' and h.house_class = "' + str(house_class) + '"' if house_class != -1 else ''
	sql_agreement = ' and h.agreement = "' + str(agreement) + '"' if agreement != -1 else ''
	sql_stage = ' and h.stage = "' + str(stage) + '"' if stage != -1 else ''
	sql_zone = ' and hc.zone = "' + str(zone) + '"' if zone != -1 else ''
	sql_region_city = ' and hc.region_city_id = ' + str(region_city_id) if region_city_id != -1 else ''
	sql_district_direction = ' and hc.district_direction_id = ' + str(district_direction_id) if district_direction_id != -1 else ''
	sql_atd = ' and hc.atd_id = ' + str(atd_id) if atd_id != -1 else ''
	sql_order = ' '
	sql_limit = ' '

	if developer_id == 0:
		sql_order = ' order by random() '
		sql_limit = ' limit 1000 '
	elif housing_complex_id == 0:
		sql_dev_hc_h = ' and o.developer_id = ' + str(developer_id)
	elif house_id == 0:
		sql_dev_hc_h = ' and o.housing_complex_id = ' + str(housing_complex_id)
	elif house_id != 0:
		sql_dev_hc_h = ' and o.house_id = ' + str(house_id)

	conn = 'sqlite:///app.db'
	df = pd.read_sql(sql_select + sql_join_house + sql_join_housing_complex + sql_where_1_1 + sql_object_type + sql_decoration + sql_room +
	                 sql_price_min + sql_price_max + sql_square_min + sql_square_max + sql_is_studio + sql_dev_hc_h + 
					 sql_hclass + sql_agreement + sql_stage + sql_zone + sql_region_city + sql_district_direction + sql_atd + sql_order + sql_limit, conn)
	
	df['price'] = pd.to_numeric(df['price'])
	df['square'] = pd.to_numeric(df['square'])

	g = sns.scatterplot(x='square', y='price', hue='room', style='type', s=100, alpha=0.8,
	                    data=df, palette="Set2", legend='full')
	plt.xlim(0, None)
	plt.tight_layout()

	formatter = FuncFormatter(millions)
	g.yaxis.set_major_formatter(formatter)

	img = io.BytesIO()
	fig.savefig(img)
	img.seek(0)
	return send_file(img, mimetype='image/png')


@app.route('/price_boxplot')
def price_boxplot():
	developer_id = request.args.get('dev')
	developer_id = int(developer_id) if developer_id is not None else 0

	housing_complex_id = request.args.get('hc')
	housing_complex_id = int(
		housing_complex_id) if housing_complex_id is not None else 0

	house_id = request.args.get('h')
	house_id = int(house_id) if house_id is not None else 0

	fig, ax = plt.subplots(figsize=(10, 6))

	conn = 'sqlite:///app.db'
	if developer_id == 0:
		# df = pd.read_sql('select d.id, d.name, min(o.price) min_price, max(o.price) max_price, count(o.id) objects from object o join developer d on o.developer_id=d.id group by d.id', conn)
		df = pd.read_sql(
			'select o.room, o.square, o.price from object o order by random() limit 5000', conn)
		df['price'] = pd.to_numeric(df['price'])
		df['square'] = pd.to_numeric(df['square'])

		g = sns.scatterplot(x='square', y='price', data=df)
		plt.tight_layout()

		formatter = FuncFormatter(millions)
		g.yaxis.set_major_formatter(formatter)
	elif housing_complex_id == 0:
		df = pd.read_sql(
			'select hc.id, hc.name, o.price from object o join housing_complex hc on o.housing_complex_id=hc.id where o.developer_id = ' + str(developer_id), conn)
		df['price'] = pd.to_numeric(df['price'])
		g = sns.boxplot(y='price', x='name', data=df)
		g.set_xticklabels(g.get_xticklabels(), rotation=45,
		                  horizontalalignment='right')
		plt.tight_layout()

		g.set_xlabel('')
		g.set_ylabel('')

		formatter = FuncFormatter(millions)
		g.yaxis.set_major_formatter(formatter)
	elif house_id == 0:
		df = pd.read_sql(
			'select h.id, h.name, o.price from object o join house h on o.house_id=h.id where o.housing_complex_id = ' + str(housing_complex_id), conn)
		df['price'] = pd.to_numeric(df['price'])
		g = sns.boxplot(y='price', x='name', data=df)
		g.set_xticklabels(g.get_xticklabels(), rotation=45,
		                  horizontalalignment='right')
		plt.tight_layout()

		g.set_xlabel('')
		g.set_ylabel('')

		formatter = FuncFormatter(millions)
		g.yaxis.set_major_formatter(formatter)
	elif house_id != 0:
		df = pd.read_sql(
			'select * from object where house_id = ' + str(house_id), conn)

	# ax.hist(np.random.rand(Ntotal), 20)

	img = io.BytesIO()
	fig.savefig(img)
	img.seek(0)
	return send_file(img, mimetype='image/png')

def millions(x, pos):
    'The two args are the value and tick position'
    return '%1.1fM' % (x/1e6)

@app.route('/about')
def about():
	return 'The about page'


@app.route('/favicon.ico')
def favicon():
	return favicon.ico



