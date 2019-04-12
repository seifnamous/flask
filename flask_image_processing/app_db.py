from flask import Flask, render_template, redirect
import os, sys
import cv2
import numpy as np
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL(app)

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'sifo'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'Image'


@app.route('/view')

def display_names():
	list_image = os.listdir('static/assets')
	list_image = [file for file in list_image]
	to_print = ""
	for img in list_image:
		if img.endswith('.jpg'):
			to_print = to_print + " | " + img
	return render_template('view.html', to_print = to_print)

@app.route('/view/<name_image>')
def filter_image(name_image):

	try:
	
		path = '/home/namous/ai/simplon/manel/flask_img/static/assets/{}.jpg'.format(name_image)
		img_loaded = cv2.imread(path, cv2.IMREAD_UNCHANGED)
		 
		# Resize 
		scale_percent = 60 
		w = 150
		h = 150
		dim = (w, h)
		img_resized = cv2.resize(img_loaded, dim, interpolation = cv2.INTER_AREA)
			 
		# Color processing
		F1 = 1/ 20 * np.array([ [1, 1, 1], [1, 1, 1], [1, 1, 1]])
		img_filtered=cv2.filter2D(img_resized,-1,kernel=F1)
		path = '/home/namous/ai/simplon/manel/flask_img/static/train/{}.jpg'.format(name_image)
		cv2.imwrite(path, img_filtered)

		# Update table in data base
		cur = mysql.get_db().cursor()
		name_db = name_image + '.jpg'
		treated_db = 'yes'
		cur.execute("""UPDATE image SET width=%s, height=%s, treated=%s WHERE name=%s""" ,(w,h,treated_db, name_db))
		mysql.get_db().commit()
		cur.close()

		return "Done!"

	except:

		return redirect("http://127.0.0.1:5000/view")


@app.route('/page/images')
def display_filtered_image():
	list_image = os.listdir('static/assets')
	list_filtered_image = os.listdir('static/train')

	return render_template('image.html', list_image = list_image, list_filtered_image = list_filtered_image)


if __name__ == '__main__':
	app.run(debug = True)