from flask import Flask, render_template
import OCR


app = Flask(__name__)


@app.route('/')
def welcome():
   return "Hello! Let us learn about importance of Exercise!"

if(__name__ == "__main__"):
   app.run(debug=True, port=4200)

