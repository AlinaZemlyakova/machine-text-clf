from flask import Flask, render_template, request
from analyzer import Analyzer

from flask_mysqldb import MySQL

analyzer = Analyzer('checkpoints/bert_model_0_1.pt')

from flask import Flask
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '1234567890'
app.config['MYSQL_DATABASE_DB'] = 'nlg_label'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

conn = mysql.connect()
cur =conn.cursor()

cur.execute(''' INSERT INTO nlg_label.main (text, label) VALUES('qqq222', 'correct222')''')
conn.commit()

@app.route('/')
def tryit():
    return render_template('tryit.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/predict_label', methods=['POST'])
def predict_label():
    text = request.form['text']
    print(text)
    pred_label = analyzer.predict_label(text)
    print(pred_label)
    return render_template('tryit.html', context={'label': pred_label})

def insert_into_db():
  text = request.form['text']
  cur.execute(''' INSERT INTO nlg_label ('text') VALUES(%s)''',(text))
  mysql.connection.commit()

def insert_label():
    if "correct" in request.form:
        cur.execute(''' INSERT INTO nlg_label ('label') VALUES('correct')''')
    elif "incorrect" in request.form:
        cur.execute(''' INSERT INTO nlg_label ('label') VALUES('correct')''')
    return render_template('tryit.html')

if __name__ == '__main__':
    app.run()