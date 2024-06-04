# pip install flask pytest pytest-flask


from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({'message': 'Hello, world!'})

@app.route('/about')
def about():
    return 'About page'

if __name__ == '__main__':
    app.run(debug=True)


