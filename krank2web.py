from flask import Flask, render_template, url_for, request, redirect
import random
import csv
from currency_converter import CurrencyConverter

app = Flask(__name__)
c = CurrencyConverter()

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
    try:
        with open('fxlog.txt', 'r') as file:
            last_fx = file.read()
        print(last_fx)
        return render_template('fxconversion.html',
                                page_title='Krank Currency',
                                the_last_currency=last_fx)
    except:
        return render_template('fxconversion.html', page_title='Uhoh',
                                                    the_last_currency='',
                                                    error_message='An error occured! Check Currency or Inputs')

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
    """grabs each added item, appends to a list, increments backwards sending to html"""
    contents = []
    with open("options.csv") as f:
        for row in f:
            contents.append(row.split(',')[0])
    converted_contents = []
    for element in contents:
        converted_contents.append(element.strip())
    return render_template('list.html',
                            page_title='Krank List',
                            the_data=converted_contents[::-1] )

@app.route('/deleteitem', methods=['GET', 'POST'])
def do_delete_item():
    """grabs all data, adds to list, overwrite csv with everything except item to delete. If fails, reloads page"""
    try:
        contents = []
        with open("options.csv") as f:
            for row in f:
                contents.append(row.split(',')[0])
        converted_contents = []
        for element in contents:
            converted_contents.append(element.strip())
        to_delete = str(request.form['item'])
        converted_contents.remove(to_delete)
        with open('options.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for row in converted_contents:
                writer.writerow([row])
        return redirect('/list')
    except:
        return redirect('/list')

@app.route('/additem', methods=['GET', 'POST'])
def do_add_item():
    """appends data submitted to csv file"""
    with open('options.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([request.form['item']])
    return redirect('/list')

@app.route('/convert', methods=['GET', 'POST'])
def do_conversion():
    """convert currency from one field against entered currency, reload form with placeholder data as result"""
    try:
        fx_type = request.form['fcurrencytype']
        fx_type = fx_type.upper()
        with open('fxlog.txt', 'w') as file:
            file.write(fx_type)
        fx_amount = request.form['FXcurrencyamount']
        aud_amount = request.form['AUDcurrencyamount']
        #Entered FX Currency to Convert to AUD
        if not fx_amount == '':
            conversion = c.convert(fx_amount, fx_type, 'AUD')
            conversion_result = str("{:.2f}".format(conversion))
            return render_template('fxconversion.html', page_title='Krank Currency',
                                                        aud_field=conversion_result,
                                                        fx_field=fx_amount,
                                                        the_last_currency=fx_type)
        #Entered AUD to Convert to FX
        if not aud_amount == '':
            conversion = c.convert(aud_amount, 'AUD', fx_type)
            conversion_result = str("{:.2f}".format(conversion))
            return render_template('fxconversion.html', page_title='Krank Currency',
                                                        aud_field=aud_amount,
                                                        fx_field=conversion_result,

        #No currency added, clears everything
        if not aud_amount == '' and not fx_amount == '':
            return render_template('fxconversion.html', page_title='Krank Currency',
                                                        aud_field='',
                                                        fx_field='',
                                                        the_last_currency='')
    except:
        return render_template('fxconversion.html', page_title='Uhoh',
                                                    the_last_currency='',
                                                    error_message='An error occured! Check Currency or Inputs')
if __name__ == '__main__':
    app.run(debug=True)
