from flask import Flask, render_template, request
from analyzer import Analyzer

from flask_mysqldb import MySQL

app = Flask(__name__, template_folder='templates')

analyzer = Analyzer('checkpoints/bert_model_0_1.pt')

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234567890'
app.config['MYSQL_DB'] = 'flask'
 
mysql = MySQL(app)

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

cur = mysql.connection.cursor()

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