from flask_app import app
from flask_app.controllers import customers, housekeepers, index, jobs, applications

if __name__ == "__main__":
    app.run(debug=True)