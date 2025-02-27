#import modules
from flask import Flask, render_template, request, flash, url_for, redirect
import mysql.connector
from mysql.connector import errorcode
import pygal


#create a flask app object and set app variables
app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRECT_KEY"] = 'your secret key'
app.secret_key = 'your secret key'

#create a connection object to the module2 database
def get_db_connection():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            port="6603",
            database="sakila"
        )
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your username or password.")
            exit()
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist.")
            exit()
        else:
            print(err)
            print("ERROR: Service not available")
            exit()

    return mydb

def get_years():
    mydb = get_db_connection()
    cusor = mydb.cursor(dictionary=True)
    query = 'select distinct year(payment_date) as "year" from payment  order by year(payment_date);'
    cusor.execute(query)
    years = cusor.fetchall()
    return years

def graph(labels, values):
    chart_title = "The Chart Title"
    chart_object = pygal.Bar(x_label_rotation=45, height=300)
    chart_object._title = chart_title
    chart_object.x_labels = labels
    chart_object.add("title", values)

    return chart_object.render_data_uri()

#create a route to the navigation page
@app.route('/', methods=('GET', 'POST'))
def navigation():
    #Determine which method the page was requested with
    if request.method == 'POST':
        #get the form data
        option = request.form.get('option')

        #determine which view to send the application to
        if option == 'navigation':
            #redirect to the url for navigation
            return redirect(url_for('navigation'))
        elif option == 'customers':
            #redirect to the url for customers
            return redirect(url_for('customers'))
        elif option == 'rentals':
            #redirect to the url for rentals
            return redirect(url_for('rentals'))
        elif option == 'inventory':
            #redirect to the url for inventory
            return redirect(url_for('inventory'))
        
    return render_template('navigation.html')



#get the customer data
@app.route('/customers', methods=('GET',))
def customers():
    years = get_years()

    return render_template('customers.html',years = years)

#post the customer data
@app.route('/customers', methods=('POST',))
def customers_post():
    #get the form data 
    option = request.form.get('option')

    years = get_years()
    year = request.form.get('year')

    mydb = get_db_connection()
    cursor = mydb.cursor(dictionary=True)

    if (option == "Rental Sales"):
        query = '''
                select * from customerRentalSales
                where year = %s;'''
        
        cursor.execute(query, (year,))
        rental_result = cursor.fetchall()

        customer = []
        totalSales = []
        for record in rental_result:
            customer.append(record['customer'])
            totalSales.append(record['TotalSales'])
        
        chart = graph(customer, totalSales)
        return render_template('customers.html', rental_result=rental_result, years=years, chart=chart)
    elif (option == "Movie Rentals"):
        query = '''
                select * from customerMovieRentals
                where year = %s;'''
        
        cursor.execute(query, (year,))
        movie_result = cursor.fetchall()

        customer = []
        totalSales = []
        for record in movie_result:
            customer.append(record['customer'])
            totalSales.append(record['TotalRentals'])
        
        chart = graph(customer, totalSales)
        return render_template('customers.html', movie_result=movie_result, years=years, chart=chart)

#get the rental data
@app.route('/rentals', methods=('GET',))
def rentals():
    years = get_years()


    return render_template('rentals.html', years=years)

#post the rental data
@app.route('/rentals', methods=('POST',))
def rentals_post():
    #get the form data
    option = request.form.get('option')

    years = get_years()
    year = request.form.get('year')


    mydb = get_db_connection()
    cursor = mydb.cursor(dictionary=True)

    if (option == "Monthly Sales"):
        query = '''
                select * from monthlyRentalSales
                where year = %s;
                '''
        cursor.execute(query, (year,))
        result = cursor.fetchall()

        year = []
        month = []
        month_num = []
        total_payments = []
        for record in result:
            year.append(record['year'])
            month.append(record['month'])
            month_num.append(record['month_num'])
            total_payments.append(record['TotalPayments'])
        
        chart = graph(month, total_payments)
        return render_template('rentals.html', result=result, years=years, chart=chart)
    elif (option == "Sales By Category"):
        query = '''
                select * from categoryTotals
                where year = %s;
                '''
        cursor.execute(query, (year,))
        category_result = cursor.fetchall()

        year = []
        name = []
        total_payments = []
        for record in category_result:
            year.append(record['year'])
            name.append(record['name'])
            total_payments.append(record['TotalPayments'])
        
        chart = graph(name, total_payments)
        return render_template('rentals.html', category_result=category_result, years=years, chart=chart)
    elif (option == "Sales By City"):
        query = '''
                select * from StoreCityTotals
                where year = %s;
                '''
        cursor.execute(query, (year,))
        city_result = cursor.fetchall()

        year = []
        city = []
        total_payments = []
        for record in city_result:
            year.append(record['year'])
            city.append(record['city'])
            total_payments.append(record['TotalPayments'])
        
        chart = graph(city, total_payments)
        return render_template('rentals.html', city_result=city_result, years=years, chart=chart)




#get the inventory data
@app.route('/inventory', methods=('GET',))
def inventory():
    
    return render_template('inventory.html')

#post the inventory data
@app.route('/inventory', methods=('POST',))
def inventory_post():
    #get the form data
    option = request.form.get('option')


    mydb = get_db_connection()
    cursor = mydb.cursor(dictionary=True)

    if (option == "Movies By Category"):
        query = '''
                select * from moviesPerCategory
                '''
        cursor.execute(query)
        category_result = cursor.fetchall()

        name = []
        numMovies = []
        for record in category_result:
            name.append(record['name'])
            numMovies.append(record['numMovies'])
        
        chart = graph(name, numMovies)
        return render_template('inventory.html', category_result=category_result, chart=chart)
    elif (option == "Movies In Stock"):
        query = '''
                select * from moviesPerCategoryInStock
                '''
        cursor.execute(query)
        stock_result = cursor.fetchall()

        name = []
        InStock = []
        for record in stock_result:
            name.append(record['name'])
            InStock.append(record['InStock'])
        
        chart = graph(name, InStock)
        return render_template('inventory.html', stock_result=stock_result, chart=chart)
    






#run the application
app.run(port=5003, debug=True)

