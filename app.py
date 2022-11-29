import email
from click import password_option
from flask import Flask, render_template, url_for, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, login_user, LoginManager, logout_user, UserMixin
import os


from userform import Login_form, Register_Form, Post_Form, Comment_Form

app = Flask(__name__)
script_dir = os.path.abspath(os.path.dirname(__file__))
dbfile = os.path.join(script_dir, "articles.sqlite3")
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SECRET_KEY'] = 'averylongandnondescriptsecritkey' #TODO: !!!MAKE A NEW SECRET KEY, DON'T HAVE ONE!!!
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{dbfile}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.login_manager = LoginManager()
app.login_manager.login_view = 'get_login'
@app.login_manager.user_loader
def load_user(uid):
    return User.query.get(int(uid))

class User(UserMixin, db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode, nullable=False)
    email = db.Column(db.Unicode, nullable=False)
    password = db.Column(db.Unicode, nullable=False)

class Post(db.Model):
    __tablename__ = 'Posts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_name = db.Column(db.Unicode, nullable=False)
    user_id = db.Column(db.Unicode, db.ForeignKey('Users.id'))
    recipe = db.Column(db.Unicode, nullable=False)

class Comment(db.Model):
    __tablename__ = 'Comments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Unicode, db.ForeignKey('Posts.id'))
    user_id = db.Column(db.Unicode, db.ForeignKey('Users.id'))
    text = db.Column(db.Unicode, nullable=False)
    rating = db.Column(db.Unicode, nullable=False)
    
with app.app_context():
    db.drop_all()
    db.create_all()

@app.route("/")
def index(): #TODO: HOMEPAGE
    return redirect(url_for("explore_page"))   

@app.get("/login/")
def get_login(): #TODO: LOGIN PAGE (SAVES PREVIOUS VISITED ADDRESS WITH session)
    form = Login_form()
    return render_template("login.html", form=form)

@app.post("/login/")
def post_login(): #TODO: LOGIN PAGE (SAVES PREVIOUS VISITED ADDRESS WITH session)
    form = Login_form()
    if form.validate():
        temp_username = form.username.data
        temp_password = form.password.data
        db_user = User.query.filter_by(username=temp_username).first()
        if (db_user) and (db_user.password == temp_password):
            #TODO: Finalize login stage
            login_user(db_user)
            return redirect(url_for('index'))
        else:
            flash("Username or password was not correct")
        return redirect(url_for('get_login'))
    else:
        for field,error in form.errors.items():
            flash(f"{field}: {error}")
        return redirect(url_for('get_login'))
        
@app.get("/register/")
def get_register():
    form = Register_Form()
    return render_template("register.html", form=form)

@app.post("/register/")
def post_register(): #TODO: REGISTER PAGE
    form = Register_Form()
    check_name = User.query.filter_by(username=form.username.data).first()
    #check_email = User.query.filter_by(email=form.email.data).first()

    if not form.validate():
        for field,error in form.errors.items():
            flash(f"{field} - {error}")
        return redirect(url_for("get_register"))
    
    if check_name:
        flash("Username: " + form.username.data + " has already been taken.")
        return redirect(url_for("get_register"))

    # if check_email:       #LET ME KNOW IF THIS IS SOMETHING WE WANT TO DO.
    #    flash("Email: " + form.email.data + " already has an account.")
    #    return redirect(url_for("get_register"))

    username = form.username.data
    email = form.email.data
    password = form.password.data
    new_user = User(username=username, email=email, password=password) 
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('index'))
   
@app.get("/post/")
@login_required
def get_post():
    form = Post_Form()
    return render_template("post.html", form=form)
    
@app.post("/post/")
@login_required
def post_post():
    form = Post_Form()
    
    if not form.validate():
        for field,error in form.errors.items():
            flash(f"{field} - {error}")
        return redirect(url_for("get_post"))
    
    post_name = form.post_name.data
    #user_id = session["username"]
    recipe = form.recipe.data
    #user_id placeholder
    new_post = Post(post_name=post_name, user_id = 1, recipe=recipe)
    db.session.add(new_post)
    db.session.commit()
    return redirect(url_for("explore_page"))

@app.get("/comment/")
@login_required
def get_comment():
    form = Comment_Form()
    return render_template("comment.html", form=form)

@app.post("/comment/")
@login_required
def post_required():
    form = Comment_Form()

    if not form.validate():
        for field,error in form.errors.items():
            flash(f"{field} - {error}")
        return redirect(url_for("get_comment"))

    #post id here
    #user id here
    text = form.text.data
    rating = form.rating.data
    new_comment = Comment(post_id=1, user_id=1, text=text, rating=rating)
    db.session.add(new_comment)
    db.session.commit()

@app.route("/profile/<int:userid>/")
def profile_view(userid):  #TODO: VIEWING A PERSON'S PROFILE PAGE WITH ALL OF THEIR RECIPE POSTS
    pass

@app.route("/explore/")
@app.route("/explore/<int:postid>/")
def explore_page(postid=0):
    if (postid == 0): #TODO: If there is no postid, then display the page with AJAX
        #TODO ADD AJAX, FOR MIDPOINT WE WILL JUST DISPLAY STUFF HERE
        all_posts = Post.query.order_by(Post.id).all()
        return render_template("homepage.html", posts=all_posts)
    #TODO: Then display the actual post itself in full-view mode
    pass

@app.route("/logout/")
@login_required
def logout_page():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("get_login"))