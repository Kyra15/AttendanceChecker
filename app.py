from flask import Flask, render_template
import OCR


app = Flask(__name__)

@app.route('/')
def index():
    user = {'username': 'Kyra'}
    return render_template('index.html', title='Attendance Checker', user=user)

if __name__ == '__main__':
    app.run(debug=True)
