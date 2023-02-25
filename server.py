from flask_app import app
#from flask_app2.controllers import burgers
from flask_app.controllers import pypies, pyusers
# ...server.py
#app = Flask(__name__)
if __name__=="__main__":
    app.run(debug=True)