from flask import Flask, render_template, url_for, request, redirect
import random
import csv

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
    """Randomly selects items from a csv"""
    contents = []
    with open("options.csv") as f:
        for row in f:
            contents.append(row.split(',')[0])
    item = random.choice(contents)
    return render_template('options.html',
                            page_title='Krank Generator',
                            the_generated=item)

@app.route('/list')
def do_list():
    contents = []
    with open("options.csv") as f:
        for row in f:
            contents.append(row.split(',')[0])
    return render_template('list.html',
                            page_title='Krank List',
                            the_data=contents[::-1] )

@app.route('/deleteitem', methods=['GET', 'POST'])
def do_delete_item():
    return redirect('/list')




@app.route('/additem', methods=['GET', 'POST'])
def do_add_item():
    with open('options.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([request.form['item']])
    return redirect('/list')

@app.route('/convert')
def do_conversion():
    return render_template('fxconversion.html', page_title='Krank Currency')

@app.route('/conversionlog')
def show_log():
    return render_template('conversionlog.html', page_title='Krank Conversion Log')

if __name__ == '__main__':
    app.run(debug=True, host='172.16.80.92')
