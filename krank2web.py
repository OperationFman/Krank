from flask import Flask, render_template, url_for
import random

app = Flask(__name__)

@app.route('/')
def do_index():
    return render_template('index.html',
                            page_title='Krank Webapp')

@app.route('/options')
def do_food_roulette():
    return render_template('options.html',
                            page_title='Krank Food',
                            the_generated='Food Roulette')

@app.route('/fxconverter')
def do_fx_converter():
    return render_template('fxconversion.html',
                            page_title='Krank Currency')

@app.route('/generate')
def do_generate():
    foo = ['sample 1', 'sample 2', 'sample 3', 'sample 4', 'sample 5', 'sample 6', 'sample 7', 'sample 8']
    fum = random.choice(foo)
    generate_output = fum
    return render_template('options.html',
                            page_title='Krank Generator',
                            the_generated=generate_output)

@app.route('/list')
def do_list():
    return render_template('list.html',
                            page_title='Krank List')

@app.route('/additem')
def do_add_item():
    return render_template('list.html',
                            page_title='Krank List')

@app.route('/toggleitem')
def do_toggle_item():
    return render_template('list.html',
                            page_title='Krank List')

@app.route('/deleteitem')
def do_delete_item():
    return render_template('list.html',
                            page_title='Krank List')

@app.route('/convert')
def do_conversion():
    return render_template('fxconversion.html', page_title='Krank Currency')

@app.route('/conversionlog')
def show_log():
    return render_template('conversionlog.html', page_title='Krank Conversion Log')

if __name__ == '__main__':
    app.run(debug=True, host='172.16.80.97')
