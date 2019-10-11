from matplotlib.ticker import FuncFormatter
from flask import Flask, escape, request, render_template, flash, redirect, url_for, send_file
from app import app
from app.forms import LoginForm
from app.models import Developer, HousingComplex, House, Object
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
	user = {'username': 'Miguel'}
	posts = [
		{
			'author': {'username': 'John'},
			'body': 'Beautiful day in Portland!'
		},
		{
			'author': {'username': 'Susan2'},
			'body': 'The Avengers movie was so cool!'
		}
	]
	return render_template('index.html', title='Home', user=user, posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))
		return redirect(url_for('index'))
	return render_template('login.html', title='Sign In', form=form)

@app.route('/real_estate_base/')
def real_estate_base():
	# return 'DEVELOPER_ID%s' %developer_id
	developer = Developer.query.all()

	developer_id = request.args.get('dev')
	developer_id = int(developer_id) if developer_id is not None else 0

	housing_complex_id = request.args.get('hc')
	housing_complex_id = int(housing_complex_id) if housing_complex_id is not None else 0

	house_id = request.args.get('h')
	house_id = int(house_id) if house_id is not None else 0

	if developer_id == 0:
		housing_complex = HousingComplex.query.all()
		house = House.query.filter_by().all()
		object = Object.query.filter_by().limit(100).all()
	elif housing_complex_id == 0:
		housing_complex = HousingComplex.query.filter_by(developer_id=developer_id).all()
		house = House.query.filter_by(developer_id=developer_id).all()
		object = Object.query.filter_by(developer_id=developer_id).limit(100).all()
	elif house_id == 0:
		housing_complex = HousingComplex.query.filter_by(developer_id=developer_id).all()
		house = House.query.filter_by(housing_complex_id=housing_complex_id).all()
		object = Object.query.filter_by(housing_complex_id=housing_complex_id).limit(100).all()
	elif house_id != 0:
		housing_complex = HousingComplex.query.filter_by(developer_id=developer_id).all()
		house = House.query.filter_by(housing_complex_id=housing_complex_id).all()
		object = Object.query.filter_by(house_id=house_id).limit(100).all()

	return render_template('real_estate_base.html', title='Real Estate Base',
		developer = developer, 
		housing_complex = housing_complex, 
		house = house,
		object = object
		)

@app.route('/fig')

def fig():
	developer_id = request.args.get('dev')
	developer_id = int(developer_id) if developer_id is not None else 0

	housing_complex_id = request.args.get('hc')
	housing_complex_id = int(housing_complex_id) if housing_complex_id is not None else 0

	house_id = request.args.get('h')
	house_id = int(house_id) if house_id is not None else 0
	
	fig, ax = plt.subplots(figsize=(10, 6))

	conn = 'sqlite:///app.db'
	if developer_id == 0:
		# df = pd.read_sql('select d.id, d.name, min(o.price) min_price, max(o.price) max_price, count(o.id) objects from object o join developer d on o.developer_id=d.id group by d.id', conn)
		df = pd.read_sql('select o.room, o.square, o.price from object o order by random() limit 5000', conn)
		df['price'] = pd.to_numeric(df['price'])
		df['square'] = pd.to_numeric(df['square'])

		g = sns.scatterplot(x='square', y='price', data=df)
		plt.tight_layout()

		formatter = FuncFormatter(millions)
		g.yaxis.set_major_formatter(formatter)
	elif housing_complex_id == 0:
		df = pd.read_sql('select hc.id, hc.name, o.price from object o join housing_complex hc on o.housing_complex_id=hc.id where o.developer_id = ' + str(developer_id), conn)
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
		df = pd.read_sql('select * from object where house_id = ' + str(house_id), conn)

	# ax.hist(np.random.rand(Ntotal), 20)

	img = io.BytesIO()
	fig.savefig(img)
	img.seek(0)
	return send_file(img, mimetype='image/png')


def millions(x, pos):
    'The two args are the value and tick position'
    return '%1.0fM' % (x/1e6)

@app.route('/about')
def about():
	return 'The about page'



