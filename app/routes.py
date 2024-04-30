from flask import render_template
from flask import redirect, request, url_for
from flask import flash
from .forms import LoginForm, LogoutForm, HomeForm, RegisterForm, DeleteAccountForm, AdminForm, AddBook
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Book
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
        flash("You are already logged in!")
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
# @myapp_obj.route("/book", methods=['GET', 'POST'])
# def addbook():
#     if not current_user.is_authenticated: 
#         flash("You aren't logged in yet!")
#         return redirect('/')
#     form = AddBook()
#     if form.validate_on_submit():
#         if Book.query.filter_by(bookname=form.bookname.data).first() is None:
#             newBook = Book(bookname = form.bookname.data, bookauthor=form.bookauthor.data)
#             db.session.add(newBook)
#             db.session.commit()
#             flash("Book Added!")
#             return redirect("/admin_book")
#         else:
#             flash("That book already added! Try again with a different name.")
#             return redirect("/admin_book")
#     return render_template('admin_book.html', form = form)
@myapp_obj.route("/modifyUser/<int:id>")
def modifyUser(id): #get email id of the email that is choosen to be deleted
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
    #no need to render when deleting book
    return render_template('deleteBook.html', form = form)
@myapp_obj.route("/book/<int:id>", methods=['GET', 'POST'])
def BookNew(id):
    item = Book.query.get(id)
    item.completed = not item.completed
    db.session.commit()
    return redirect('/book')
@myapp_obj.route("/delBook/<int:id>")
def delBook(id): #get email id of the email that is choosen to be deleted
    if not current_user.is_authenticated:
        flash("You aren't logged in yet!")
        return redirect('/')
    else: 
         book = Book.query.get(id)
         db.session.delete(book)
         db.session.commit()
         flash('Book deleted')
         return redirect("/book")
    #no need to render when deleting book
    return render_template('deleteBook.html', form = form)
    
@myapp_obj.route("/book", methods=['GET', 'POST'])
def book():
    if not current_user.is_authenticated: 
        flash("You aren't logged in yet!")
        return redirect('/')
    noItems = False
    bookItems = Book.query.all()
    if bookItems is None: noItems = True
    return render_template('book.html', items = bookItems, emptyList = noItems)

@myapp_obj.route("/admin_book", methods=['GET', 'POST'])
def admin_book():
    if not current_user.is_authenticated: 
        flash("You aren't logged in yet!")
        return redirect('/')
    noItems = False
    bookItems = Book.query.all()
    if bookItems is None: noItems = True
    return render_template('admin_book.html', items = bookItems, emptyList = noItems)

@myapp_obj.route("/bookAdd", methods=['GET', 'POST'])
def bookAdd():
    if not current_user.is_authenticated: 
        flash("You aren't logged in yet!")
        return redirect('/')
    form = AddBook()
    if form.validate_on_submit():
        book = Book(title=form.title.data, author=form.author.data, username = current_user.username, completed = 0)
        db.session.add(book)
        db.session.commit()
        return redirect('/admin_book')
    return render_template('bookAdd.html', form = form)
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
