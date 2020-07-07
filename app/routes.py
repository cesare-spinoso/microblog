from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm, EditProfileForm, EmptyForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse
from datetime import datetime

# To keep track of the last seen time, could add a field for each
# of the routes but you can see why this would not be fun (i.e. for every new
# access to a page update last_see to current time). Instead you can
# use a flask feature to do something before any request is sent
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit() # using current_user flask-login
        # does the db.add for you



# Python decorator, when URL request is / or /index then follow the function below
@app.route('/')
@app.route('/index')
@login_required # Also sets the initial url (which was not accessible) as next = in the URL request
def index(): # View function name is index so url_for('index')
    # A dummy user for now
    # user = {'name': 'Giancarlo'},
    # Some dummy posts
    posts = [
        {
            'author' : {'name' : 'Jon'},
            'body' : 'It is a nice day'
        },
        {
            'author' : {'name' : 'Doe'},
            'body' : 'I humbly agree'
        }
    ]

    # Takes in a template file name and a variable list of args
    # It then returns the template (in this case index.html) but with all the placeholders replaced
    return render_template('index.html', title='Front', posts=posts)


@app.route('/login', methods=['GET', 'POST'])  # This view function accepts GET and POST requests (default was only GET)
def login():
    # In the weird case where the currenlty logged in user access the Login page again
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    # ALL the form processing work done here (validate on submit)
    # If there is a GET request it is skipped and goes to the render template
    # When there is a POST request sent (resulting from a submit on POST) if all validation is good passes otherwise
    # also renders back (with error messages)
    if form.validate_on_submit():
        # Flash shows message to user --> Need to implement a way to SHOW the flash message, done in base.html
        # flash('Login requested for user {}'.format(form.username.data))
        # Replacing with real login functionality
        # Find user with the username credentials (since username is unique)
        user = User.query.filter_by(username = form.username.data).first()
        # If uses is None (No entry) or password does not match redirect to index
        if user is None or not user.check_pwd(form.password.data):
            flash('Invalid password or email. Please try again!')
            return redirect(url_for('login'))
        # Otherwise, log in the user
        login_user(user, remember=form.remember_me.data) # Current user is now set to that user
        # If tried to access a restricted page and successfully logged in, redirect it back to that page
        next_page = request.args.get('next') # request is what is in the GEt and .args puts it in a dictionary
        # format so can get \next
        if not next_page or url_parse(next_page).netloc != '': # url_parse is used to check if next = contains
            # a URL path that is not relative to the website, i.e. it could be an absolute URL to another
            # page which is malicious
            next_page = url_for('index')
        # Redirect instructs the client web browser to go to another page
        return redirect(next_page)
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    # Expose this as a conditional on the index page (in base navbar)
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_pwd(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("You have registered to this amazing microblog! Good luck :)")
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

# To create a user profile view function
 # Dynamic view function which takes
    # <username> as input (returns username as text)
@app.route('/user/<username>')
@login_required # accessible only to logged in users
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    # first_or_404() works exactly like first() except that when there
    # is nothing to output it results in a 404 error that's sent back to the clikent

    # saves the time of actually checking if valid username and
    # just throws a 404 error

    # fake list of posts
    posts = [
        {'author' : user, 'body' : 'Test post 1' },
        {'author' : user, 'body' : 'Test post 2'}
    ]

    # Pass an empty form object for the follow/unfollow buttons
    form = EmptyForm()

    return render_template('user.html',title='User', user=user, posts=posts, form=form)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username) # Because now the application is checking what the
    # original username is (this is using the __init__ constructor)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)

# Follow and unfollow routes
@app.route('/follow/<username>',methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot follow yourself!!')
            return redirect(url_for('user',username=username))
        current_user.follow(user)
        db.session.commit()
        flash('You are now following {}!'.format(username))
        return redirect(url_for('user', username=username))
    # The only way this failse is if there isnt a CSRF token
    else:
        return redirect(url_for('index'))


@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash('You are not following {}.'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))



