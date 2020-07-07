from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm, EditProfileForm, EmptyForm, PostForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post
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
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required # Also sets the initial url (which was not accessible) as next = in the URL request
def index(): # View function name is index so url_for('index')
    # Form validation for posting stuff
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Posted!')
        return redirect(url_for('index')) # Using redirects is standard practice so user doesn't
    # resubmit the same form if they press refresh  Post/Redirect/Get pattern


    # A dummy user for now
    # user = {'name': 'Giancarlo'},
    # Some dummy posts
    # posts = [
    #     {
    #         'author' : {'name' : 'Jon'},
    #         'body' : 'It is a nice day'
    #     },
    #     {
    #         'author' : {'name' : 'Doe'},
    #         'body' : 'I humbly agree'
    #     }
    # ]

    # The real deal posts
    posts = current_user.followed_posts().all()

    '''
    The paginate method can be called on any query object from Flask-SQLAlchemy. It takes three arguments:

    the page number, starting from 1
    the number of items per page
    an error flag. If True, when an out of range page is requested a 404 error will be automatically returned to the client. If False, an empty list will be returned for out of range pages.

The return value from paginate is a Pagination object. The items attribute of this object contains the list of items in the requested page
    '''

    # Add pagination where only have a fixed number of posts per page
    page = request.args.get('page', 1, type=int) # will be reading th apge number from url (get)
    posts = current_user.followed_posts().paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    # Notice how added posts.items
    '''
    Paginate has 4 other methods that are useful for links:
    
    has_next: True if there is at least one more page after the current one
    has_prev: True if there is at least one more page before the current one
    next_num: page number for the next page
    prev_num: page number for the previous page

    '''
    # To send the next and previous links
    next_url = url_for('index', page=posts.next_num) \
        if posts.has_next else None # What url_for does with parameter that it doesnt recognize?
    # it automatically puts them as queries in the url! so here ?page=posts.next_num has been added to url
    prev_url = url_for('index', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title='Home', form=form,
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)

    # return render_template('index.html', title='Home', form=form,
    #                        posts=posts.items)

    # Takes in a template file name and a variable list of args
    # It then returns the template (in this case index.html) but with all the placeholders replaced
    # return render_template('index.html', title='Front', posts=posts, form=form)


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

    #  fake list of posts
    # posts = [
    #     {'author' : user, 'body' : 'Test post 1' },
    #     {'author' : user, 'body' : 'Test post 2'}
    # ]
    # Use actual posts
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False
    )
    next_url = url_for('user', username=user.username, page=posts.next_num) \
        if posts.has_next else None # Included the extra username = because need to point back to  same user
    prev_url = url_for('user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None
    # Pass an empty form object for the follow/unfollow buttons
    form = EmptyForm()

    return render_template('user.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url, form=form)


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


# To be able to see all the users
@app.route('/explore')
@login_required
def explore():
    # Added pagination functionality
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('explore', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template("index.html", title='Explore', posts=posts.items,
                          next_url=next_url, prev_url=prev_url)
    # return render_template("index.html", title='Explore', posts=posts.items)

    # posts = Post.query.order_by(Post.timestamp.desc()).all()
    # return render_template('index.html', title='Explore', posts=posts)
    # Didn't need to create a new html page because the form will simply not show up
    # Nice



