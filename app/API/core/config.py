from flask import Flask

app = Flask(__name__, template_folder='web/templates')

if __name__ == '__main__':
    app.run(debug=True)