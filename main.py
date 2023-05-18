'''
Main script of the website.

'''
#imports
from flask import *
from flask_cors import CORS

app=Flask(__name__)
CORS(app)
app.secret_key="123"


#The '/' entrypoint
@app.route("/")
def home():
	return render_template("index.html")

with app.app_context():
	#importing different views for the website.
	from views import *



if __name__=="__main__":
	app.run(debug=True)
