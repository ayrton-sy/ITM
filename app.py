from flask import Flask, render_template, request, redirect, session
import database as db
import authentication
import logging

app = Flask(__name__)

app.secret_key = b'Z&A8|(WW$2CtJg'

logging.basicConfig(level=logging.DEBUG)
app.logger.setLevel(logging.INFO)

# @app.route('/')
# def helloWorld():
#     return'<h1>Hello!</h1>' 

navbar = """
<a href='/'>Home</a> | <a href='/products'>Products</a> |
<a href='/branches'>Branches</a> | <a href='/aboutus'>About
Us</a>
<p/>
"""
@app.route('/')
def index():    
    return render_template('index.html', page="Index")

@app.route('/products')
def products():
    code = request.args.get('code', '')
    product_list = db.get_products()
    return render_template('products.html', page="Products", product_list=product_list)

@app.route('/productdetails')
def productdetails():
    code = request.args.get('code', '')
    product = db.get_product(int(code))
    return render_template('productdetails.html', code=code,product=product)

@app.route('/branches')
def branches():
    code = request.args.get('code', '')
    branch_list = db.get_branches()
    return render_template('branches.html', page="Branches", branch_list=branch_list)

@app.route('/branchdetails')
def branchdetails():
    code = request.args.get('code', '')
    branch = db.get_branch(int(code))
    return render_template('branchdetails.html', code=code,branch=branch)

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html', page="About Us")

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/auth', methods = ['POST'])
def auth():
    username = request.form.get('username')
    password = request.form.get('password')
    is_successful, user = authentication.login(username, password)
    app.logger.info('%s', is_successful)
    if(is_successful):
        session["user"] = user
        return redirect('/')
    else:
        return render_template('login.html', error=True)

@app.route('/logout')
def logout():
    session.pop("user",None)
    session.pop("cart",None)
    return redirect('/')

@app.route('/addtocart')
def addtocart():
    code = request.args.get('code', '')
    product = db.get_product(int(code))
    item=dict()
    # A click to add a product translates to a
    # quantity of 1 for now

    item["code"] = 1
    item["qty"] = 1
    item["name"] = product["name"]
    item["subtotal"] = product["price"]*item["qty"]

    if(session.get("cart") is None):
        session["cart"]={}

    cart = session["cart"]
    cart[code]=item
    session["cart"]=cart
    return redirect('/cart')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/updateqty')
def updateqty():
    stype = request.args.get("stype")
    code = request.args.get('code', '')
    product = db.get_product(int(code))

    cart = session["cart"]
    print(cart)
    if stype == "+":
        cart[code]['qty'] += 1
        cart[code]['subtotal'] = product["price"]*cart[code]["qty"]
    else:
        if cart[code]["qty"] > 1:
            cart[code]["qty"] -= 1
            cart[code]['subtotal'] = product["price"]*cart[code]["qty"]
    session["cart"] = cart

    return redirect('/cart')

@app.route('/removeitem')
def removeitem():
    code = request.args.get('code', '')
    print(code)
    cart = session["cart"]
    del cart[code]
    session["cart"] = cart
    return redirect('/cart')