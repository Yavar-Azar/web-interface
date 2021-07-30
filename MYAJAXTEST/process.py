from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/gbbuild')
def index():
	return render_template('form.html')

@app.route('/gbbuild/findplane', methods=['POST'])
def process():



	a = request.form['rotaxis']
	b = request.form['maxsigma']




	a=float(a)
	b=float(b)

	c=a*b
	if a and b:
		res = c

		return jsonify({'result' : res})

	return jsonify({'error' : 'Missing data!'})




@app.route('/gbbuild/makegb', methods=['POST'])
def sec_process():

	a = request.form['rotaxis']
	b = request.form['maxsigma']


	a=float(a)
	b=float(b)

	c=a*b**2+5
	if a and b:
		res = c

		return jsonify({'result' : res})

	return jsonify({'error' : 'Missing data!'})


if __name__ == '__main__':
	app.run(debug=True)