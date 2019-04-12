# Create API of ML model using flask

# Import libraries
import numpy as np
from flask import Flask, render_template,request
from wtforms import Form, validators, IntegerField
import pickle

app = Flask(__name__)

class ReusableForm(Form):
	years = IntegerField('Number of years:', validators=[validators.required()])

# Load the model
model = pickle.load(open('model.pkl','rb'))

@app.route('/',methods=['GET','POST'])
def pred():
	form = ReusableForm(request.form)
	
	if request.method == 'POST' and form.validate():
		
	
		nbr_years = int(request.form['years'])

	    	# Make prediction using model loaded from disk as per the data.
	
		prediction = model.predict([[np.array(nbr_years)]])

			    # Take the first value of prediction
		output = prediction[0]
		salary = round(output[0],0)
		
		return render_template('pred.html', salary=salary)
	else:
		return render_template('home.html', form=form)

if __name__ == '__main__':
	app.secret_key='secret123'
	app.run(debug=True)
    