from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
# For the profile avatar gravatar.com
# Since the avatar belongs to the user, the logic is implemented here
from hashlib import md5

# For users following other users, create a realtionship table user - users, which is many to
# many
followers = db.Table('followers',
                     db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('followed_id', db.Integer, db.ForeignKey('user.id')))

# Create the user table as a class
class User(UserMixin, db.Model):  # Inherits from db.Model base class for all models in SQLALCHEMY
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref = 'author', lazy='dynamic')
    # Post is the raltion in the many side, backref is a field added to many class that points to one,
    # lazy how is the DB query issued

    # Add more info to user profile page. Include description and last active
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    # Add the relationship info
    followed = db.relationship(
        'User',
        secondary=followers, # To configure the association table of the relationship (done above)
        primaryjoin=(followers.c.follower_id == id), # condition that links left side (the follower
        # which we assume we are in) with the association table
        secondaryjoin=(followers.c.followed_id == id), # same thing except the right side of the realtionship
        backref=db.backref('followers', lazy='dynamic'), # from the left this is accessed with followed
        # so from the right this will be followers, dynamic says to only run query when requested
        lazy='dynamic' # same as the one above except it applied to user on left instead of right
    )

    def __repr__(self):
        return '<User {}>'.format(self.username)

    # Password hashing, given an inputted password generate a password hash
    # Don't need a pip install since werkzeug is a native flask application
    def set_pwd(self, password):
        self.password_hash = generate_password_hash(password)

    # Given a password check whether it associates with the corresponding hashed password
    def check_pwd(self, password):
        return check_password_hash(self.password_hash, password)

    # For flas-login to work User must implement following functions
    # is_autheticated, is_active, is_anonymous, get_id()
    # Since these are tedious to implement use mixin class to do it for you

    # Implement the avatar logic
    def avatar(self, size):
        # This method will return the url to gavatar to grab the avatar
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    # Allow users to follow and unfollow each other
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user) # append and remove are part of the
            # relationship object method's

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0
        # filter is a bit more flexible than fileter by

    # Get the posts of all the people that you follow
    def followed_posts(self):
        followed =  Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
            followers.c.follower_id == self.id)
        # Plus your own posts
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())




# This load_user function is used by Flask-Login to remember the user navigating through different pages
# It uses the id of the user which is passed as a string by Flask-Login (that's why use a cast to int)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


# Create the post table as a class, it has a foreign key to user 1 user can have many posts
# but a post has a single user
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(280))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)
