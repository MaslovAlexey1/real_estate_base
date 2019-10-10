from flask import Flask, escape, request, render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm
from app.models import Developer, HousingComplex, House, Object

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
# @app.route('/real_estate_base/?dev=<developer_id>')
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



@app.route('/about')
def about():
	return 'The about page'
