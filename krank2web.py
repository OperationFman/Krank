from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def do_index():
    return render_template('index.html',
                            page_title='Krank Webapp')

@app.route('/options')
def do_food_roulette():
    return render_template('options.html',
                            page_title='Krank Food')

@app.route('/fxconverter')
def do_fx_convert():
    return render_template('fxconversion.html',
                            page_title='Krank Currency')

if __name__ == '__main__':
    app.run(debug=True)
