from flask import Flask, render_template, url_for, request
import random
from DBContentManager import UseDatabase

app = Flask(__name__)
app.config['dbconfig'] = {'host': '127.0.0.1', 'user': 'Franklin', 'password': 'osakapass', 'database': 'krank', }


@app.route('/')
@app.route('/Home')
@app.route('/Entry')
def open_index():
    """Simple homepage that links to services"""
    return render_template('index.html',
                            page_title='Krank Webapp')

@app.route('/options')
def open_food_roulette():
    """Simple page the renders a form to generate options or add/remove them"""
    return render_template('options.html',
                            page_title='Krank Food',
                            the_generated='Food Roulette')

@app.route('/fxconverter')
def open_fx_converter():
    """Simple web form for currency conversion, routing and history"""
    return render_template('fxconversion.html',
                            page_title='Krank Currency')

@app.route('/generate')
def do_generate():
    """Raondomly selects an item from the optionsdb and cuts the end characters off"""
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """select item from optionsdb"""
        cursor.execute(_SQL)
        contents = cursor.fetchall()
    item = random.choice(contents)
    stringeditem = str(item)
    generate_output = stringeditem[2:-3]
    return render_template('options.html',
                            page_title='Krank Generator',
                            the_generated=generate_output)

@app.route('/list')
def do_list():
    return render_template('list.html',
                            page_title='Krank List')

@app.route('/additem', methods=['GET', 'POST'])
def do_add_item():
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """insert into optionsdb (item, toggle) (%s, %s)"""
        cursor.execute(_SQL, request.form['item'], 'True' )
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
    app.run(debug=True, host='172.16.80.140')
