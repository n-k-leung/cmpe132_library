from flask import render_template
from flask import redirect, request, url_for
from flask import flash
from .forms import LoginForm, LogoutForm, HomeForm, RegisterForm, DeleteAccountForm, AdminForm, AddBook, AddTech
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Book, Tech
from app import myapp_obj
from flask_login import current_user
from flask_login import login_user
from flask_login import logout_user
from flask_login import login_required
from . import db
    
@myapp_obj.route("/", methods=['GET', 'POST'])
@myapp_obj.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: 
        # flash("You are already logged in!")
        return redirect('/index')
    form = LoginForm()
    # if form inputs are valid
    if form.register.data:
       return redirect('/register') 
    # if clicked on register button
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            #print saying not registered and empty sign in fields
            flash('That username is not registered!')
            flash('To register, click the Register button below.')
            return redirect('/')
        elif not user.check_password(form.password.data):
            flash('Incorrect password!')
            return redirect('/')
        elif user.email != form.email.data:
            flash('That email does not match the username!')
            flash('To register a new account, click the Register button below.')
            return redirect('/')
        else:
            login_user(user)
            return redirect('/index')
    return render_template('login.html', form=form)

@myapp_obj.route("/index", methods=['GET', 'POST'])
def index():
    if not current_user.is_authenticated: 
        flash("You aren't logged in yet!")
        return redirect('/')
    if current_user.act_role == 'admin':
        return redirect('/admin')
    form = HomeForm()
    return render_template('index.html', form = form)
@myapp_obj.route("/admin", methods=['GET', 'POST'])
def admin():
    if not current_user.is_authenticated: 
        flash("You aren't logged in yet!")
        return redirect('/')
    form = AdminForm()
    notvalids = User.query.filter_by(approve=1)
    users = User.query.filter_by(approve=0)
    return render_template('admin.html', form = form, users = users,notvalids=notvalids)
@myapp_obj.route("/ApproveUser/<int:id>")
def ApproveUser(id): #get user id of the user that is choosen to be deleted
    if not current_user.is_authenticated:
        flash("You aren't logged in yet!")
        return redirect('/')
    else: 
         user = User.query.get(id)
         user.act_role = user.reg_role
         user.approve=0
         db.session.commit()
         flash('User approved')
         return redirect("/index")
    #no need to render when changing user role
    return render_template('deleteBook.html', form = form)
@myapp_obj.route("/GuestUser/<int:id>")
def GuestUser(id): #get user id of the user that is choosen to be deleted
    if not current_user.is_authenticated:
        flash("You aren't logged in yet!")
        return redirect('/')
    else: 
         user = User.query.get(id)
         user.act_role = 'guest'
         user.approve=1
         db.session.commit()
         flash('User changed to guest')
         return redirect("/index")
    #no need to render when changing user role
    return render_template('deleteBook.html', form = form)
@myapp_obj.route("/delUser/<int:id>")
def delUser(id): #get user id of the user that is choosen to be deleted
    if not current_user.is_authenticated:
        flash("You aren't logged in yet!")
        return redirect('/')
    else: 
         user = User.query.get(id)
         db.session.delete(user)
         db.session.commit()
         flash('User deleted')
         return redirect("/index")
    #no need to render when deleting user
    return render_template('deleteBook.html', form = form)
@myapp_obj.route("/reserveBook/<int:id>", methods=['GET', 'POST'])
def reserveBook(id):
    item = Book.query.get(id)
    item.reserve=0
    db.session.commit()
    if current_user.act_role == 'admin'| current_user.act_role == 'staff':
        return redirect("/admin_book")
    else:
        return redirect("/book")
@myapp_obj.route("/unreserveBook/<int:id>", methods=['GET', 'POST'])
def unreserveBook(id):
    item = Book.query.get(id)
    item.reserve=1
    db.session.commit()
    return redirect('/admin_book')
@myapp_obj.route("/delBook/<int:id>")
def delBook(id): #get book id of the book that is choosen to be deleted
    if not current_user.is_authenticated:
        flash("You aren't logged in yet!")
        return redirect('/')
    else: 
         book = Book.query.get(id)
         db.session.delete(book)
         db.session.commit()
         flash('Book deleted')
         return redirect("/admin_book")
    #no need to render when deleting book
    return render_template('deleteBook.html', form = form)
    
@myapp_obj.route("/book", methods=['GET', 'POST'])
def book():
    if not current_user.is_authenticated: 
        flash("You aren't logged in yet!")
        return redirect('/')
    notReserved = Book.query.filter_by(reserve=1)
    isReserved = Book.query.filter_by(reserve=0)
    return render_template('book.html', notReserved = notReserved, isReserved=isReserved)

@myapp_obj.route("/admin_book", methods=['GET', 'POST'])
def admin_book():
    if not current_user.is_authenticated: 
        flash("You aren't logged in yet!")
        return redirect('/')
    notReserved = Book.query.filter_by(reserve=1)
    isReserved = Book.query.filter_by(reserve=0)
    return render_template('admin_book.html', notReserved = notReserved, isReserved=isReserved)

@myapp_obj.route("/bookAdd", methods=['GET', 'POST'])
def bookAdd():
    if not current_user.is_authenticated: 
        flash("You aren't logged in yet!")
        return redirect('/')
    form = AddBook()
    if form.validate_on_submit():
        book = Book(title=form.title.data, author=form.author.data, username = current_user.username, reserve = 1)
        db.session.add(book)
        db.session.commit()
        return redirect('/admin_book')
    return render_template('bookAdd.html', form = form)
# tech
@myapp_obj.route("/reserveTech/<int:id>", methods=['GET', 'POST'])
def reserveTech(id):
    item = Tech.query.get(id)
    item.reserve=0
    db.session.commit()
    if current_user.act_role == 'admin'|current_user.act_role == 'staff':
        return redirect("/admin_tech")
    else:
        return redirect("/tech")
@myapp_obj.route("/unreserveTech/<int:id>", methods=['GET', 'POST'])
def unreserveTech(id):
    item = Tech.query.get(id)
    item.reserve=1
    db.session.commit()
    return redirect('/admin_tech')
@myapp_obj.route("/delTech/<int:id>")
def delTech(id): #get tech id of the book that is choosen to be deleted
    if not current_user.is_authenticated:
        flash("You aren't logged in yet!")
        return redirect('/')
    else: 
         tech = Tech.query.get(id)
         db.session.delete(tech)
         db.session.commit()
         flash('Tech deleted')
         return redirect("/admin_tech")
    
@myapp_obj.route("/tech", methods=['GET', 'POST'])
def tech():
    if not current_user.is_authenticated: 
        flash("You aren't logged in yet!")
        return redirect('/')
    notReserved = Tech.query.filter_by(reserve=1)
    isReserved = Tech.query.filter_by(reserve=0)
    return render_template('tech.html', notReserved = notReserved, isReserved=isReserved)

@myapp_obj.route("/admin_tech", methods=['GET', 'POST'])
def admin_tech():
    if not current_user.is_authenticated: 
        flash("You aren't logged in yet!")
        return redirect('/')
    notReserved = Tech.query.filter_by(reserve=1)
    isReserved = Tech.query.filter_by(reserve=0)
    return render_template('admin_tech.html', notReserved = notReserved, isReserved=isReserved)

@myapp_obj.route("/techAdd", methods=['GET', 'POST'])
def techAdd():
    if not current_user.is_authenticated: 
        flash("You aren't logged in yet!")
        return redirect('/')
    form = AddTech()
    if form.validate_on_submit():
        tech = Tech(name=form.name.data, info=form.info.data, time=form.time.data, username = current_user.username, reserve = 1)
        db.session.add(tech)
        db.session.commit()
        return redirect('/admin_tech')
    return render_template('techAdd.html', form = form)
# logout button should only appear when logged in
@myapp_obj.route("/logout", methods=['POST', 'GET'])
def logout():
    if not current_user.is_authenticated: 
        flash("You're already logged out!")
        return redirect('/')
    form = LogoutForm()
    if form.validate_on_submit():
        logout_user()
        return redirect("/")
    return render_template('logout.html', title = 'Logout Confirmation', form = form)
@myapp_obj.route("/delete", methods=['POST', 'GET'])
def delete():
    if not current_user.is_authenticated: 
        flash("Please log in to the account you want to delete!")
        return redirect('/')
    form = DeleteAccountForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=current_user.username).first()
        if user.check_password(form.password.data): # wrong password
            bookItems = Book.query.filter_by(username = current_user.username)
            logout_user()
            db.session.delete(user)
            for item in bookItems:
                db.session.delete(item)
            db.session.commit()
            flash("Your account has been successfully deleted.")
            return redirect("/")
        else:
            flash("Please enter your correct password and try again!")
            return redirect("/delete")
    return render_template('delete.html', title = 'Logout Confirmation', form = form)
@myapp_obj.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated: 
        flash("You are already logged in!")
        return redirect('/index')
    # create form
    form = RegisterForm()
    # if form inputs are valid
    #if clicked sign in button
    if form.sign.data:
       return redirect('/')
    checkUsername = User.query.filter_by(username=form.username.data).first()
    if checkUsername is not None: # if user already registered, then redirect back to sign in page
       flash('That username already exists')
       return redirect ('/register')
    checkUsername = User.query.filter_by(email=form.email.data).first()
    if checkUsername is not None: # if user already registered, then redirect back to sign in page
       flash('That email already exists')
       return redirect ('/register')
    if form.validate_on_submit():
            #check if registered role is valid or not
            if form.reg_role.data != 'admin' and form.reg_role.data != 'student' and form.reg_role.data != 'professor' and form.reg_role.data != 'staff' and form.reg_role.data != 'guest': #add other roles too cause wasn't working before
                flash("Invalid role!")
                return redirect ('/register')
            # new = User(username = form.username.data, email = form.email.data, reg_role = form.reg_role.data)
            #initializing all registered users as guest
            #approve = 1 initally so all users registered need to be approved
            new = User(username = form.username.data, email = form.email.data, reg_role = form.reg_role.data, act_role = 'guest', approve =1)
            #uncomment below to have test book initalized
            # book = Book(title="title1", author='book1', username = form.username.data, completed = 0)
            new.set_password(form.password.data)
            db.session.add(new)
            # db.session.add(book)
            db.session.commit()
        # login_user(user)
            flash("Account created!")
            return redirect('/')
    return render_template('register.html', form=form)
