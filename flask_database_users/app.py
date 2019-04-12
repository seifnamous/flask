from flask import Flask, render_template, request
from flaskext.mysql import MySQL

app = Flask(__name__)

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'sifo'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'User'

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        details = request.form
        username_to_insert = details['uname']
        cur = mysql.get_db().cursor()
        cur.execute("INSERT INTO users(username) VALUES (%s)", username_to_insert)
        mysql.get_db().commit()
        cur.close()
        return 'success'
    return render_template('index.html')




@app.route('/list')

def display_users():
	cur = mysql.get_db().cursor()
	cur.execute('SELECT * FROM users')
	res=""
	
	for row in cur:
		for x in row:
			res = res + " | " + x
	mysql.get_db().commit() 
	cur.close()
	return "<html><body>" + res + "</body></html>"

if __name__ == '__main__':
    app.run()
