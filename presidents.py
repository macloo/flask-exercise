from flask import Flask, render_template

app = Flask(__name__)



@app.route('/')
def index():
    return '<h1>Welcome to the presidential Flask example!</h1>'

# your code here




# keep this as is
if __name__ == '__main__':
    app.run(debug=True)
