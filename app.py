from flask import send_file, Flask, request
app = Flask(__name__)
from weather import weather

# Sample: http://127.0.0.1:5000/weather?city=Davis&state=CA&reportHours=12&key=a38755057259545e
@app.route('/weather')
def get_image():

    city = request.args.get('city')
    state = request.args.get('state')
    reportHours = int(request.args.get('reportHours'))
    key = request.args.get('key')

    filePath = weather(state = state, city = city, reportHours = reportHours, key = key).createGraph()
    return send_file(filePath, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
