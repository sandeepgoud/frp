from flask import render_template, request, session, g, abort, flash, url_for, redirect
from flask import make_response, jsonify

from .. import app, lastuser
from .. import models
from ..models import db
from ..forms import ProductForm


@app.errorhandler(404)
def http_404(error):
    if 'text/html' in request.headers.get("Accept", ""):
        return render_template('404.html', 
                               error = error, error_description = "", error_uri = "")
    else:
        return make_response(jsonify({'error' : str(error)}), 404)



@app.route("/")
def index():
    products = models.Product.query.order_by(models.Product.id.desc())
    return render_template('index.html', 
                           products = products)
    
    
@app.route("/product/add", methods=['GET', 'POST'])
@lastuser.requires_login
def product_add():
    form = ProductForm()
    if request.method == "POST":
        if form.validate_on_submit():
            name = form.name.data
            description = form.description.data
            user = g.user
            product = models.Product(name, description, user)
            db.session.add(product)
            db.session.commit()
            flash("%s added to catalogue"%form.name.data)
            return redirect("/")
    return render_template("create_product.html", form = form)


@app.route('/login')
@lastuser.login_handler
def login():
    return {'scope': 'id email'}

@app.route('/login/redirect')
@lastuser.auth_handler
def lastuserauth():
    # Save the user object
    db.session.commit()
    print dir(request.form)
    return redirect("/")


@app.route('/logout')
@lastuser.logout_handler
def logout():
    flash("You are now logged out", category='info')
    return "/"
    

@lastuser.auth_error_handler
def lastuser_error(error, error_description=None, error_uri=None):
    if error == 'access_denied':
        flash("You denied the request to login", category='error')
        return redirect("/")
    print error
    print error_description
    print error_uri
    return render_template("autherror.html",
        error=error,
        error_description=error_description,
        error_uri=error_uri)