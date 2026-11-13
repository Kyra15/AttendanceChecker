from flask import Flask, render_template, request
import OCR_utility


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', title='Attendance Checker')

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        # handle form submission and apply ocr
        pass
    else:
        pass

if __name__ == '__main__':
    app.run(debug=True)
