#import statements go here 

from flask import Flask, request, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import Required,Email

import requests,json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.debug = True

@app.route('/')
def home():
    return "Hello, world!"
    
#create class to represent WTForm that inherits flask form
class itunesForm(FlaskForm):
    artist = StringField('Enter artist', validators=[Required()])
    api = IntegerField('Enter the number of results you want the API to return?', validators=[Required()])
    email = StringField('Enter your email', validators=[Required(),Email()])
    submit = SubmitField('Submit')

@app.route('/itunes-form')
def itunes_form():
    simpleForm = itunesForm()
    return render_template('itunes-form.html', form=simpleForm) # HINT : create itunes-form.html to represent the form defined in your class

@app.route('/itunes-result', methods = ['GET', 'POST'])
def itunes_result():
    form = itunesForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        params = {}
        params['term'] = form.artist.data
        params['limit'] = form.api.data
        response = requests.get('https://itunes.apple.com/search', params=params)
        results = json.loads(response.text)['results']
        return render_template('itunes-result.html', result_html = results)
    flash('All fields are required!')
    return redirect(url_for('itunes_form')) #this redirects you to itunes_form if there are errors

if __name__ == '__main__':
    app.run()
