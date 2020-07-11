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
    converted_contents = []
    for element in contents:
        converted_contents.append(element.strip())
    return render_template('list.html',
                            page_title='Krank List',
                            the_data=converted_contents[::-1] )

@app.route('/deleteitem', methods=['GET', 'POST'])
def do_delete_item():
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
    with open('options.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([request.form['item']])
    return redirect('/list')

@app.route('/convert', methods=['GET', 'POST'])
def do_conversion():
    fx_type = request.form['fcurrencytype']
    fx_amount = request.form['FXcurrencyamount']
    aud_amount = request.form['AUDcurrencyamount']
    #Entered FX Currency to Convert to AUD
    if not fx_amount == '':
        conversion = c.convert(fx_amount, fx_type, 'AUD')
        conversion_result = str("{:.2f}".format(conversion))
        return render_template('fxconversion.html', page_title='Krank Currency',
                                                    aud_field=conversion_result,
                                                    fx_field=fx_amount)
    #Entered AUD to Convert to FX
    if not aud_amount == '':
        conversion = c.convert(aud_amount, 'AUD', fx_type)
        conversion_result = str("{:.2f}".format(conversion))
        return render_template('fxconversion.html', page_title='Krank Currency',
                                                    aud_field=aud_amount,
                                                    fx_field=conversion_result)


@app.route('/conversionlog')
def show_log():
    return render_template('conversionlog.html', page_title='Krank Conversion Log')

if __name__ == '__main__':
    app.run(debug=True, host='172.16.80.69')
