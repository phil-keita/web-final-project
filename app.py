import email
from click import password_option
from flask import Flask, jsonify, render_template, url_for, redirect, flash, session, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from flask_login import login_required, login_user, LoginManager, logout_user, UserMixin, current_user
import os


from userform import Login_form, Register_Form, Post_Form, Comment_Form, PrePostForm, IngrediantForm

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
    def tojson(self):
        return {
            "id": self.id,
            "username": self.username
        }

class Post(db.Model):
    __tablename__ = 'Posts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_name = db.Column(db.Unicode, nullable=False)
    user_id = db.Column(db.Unicode, db.ForeignKey('Users.id'))
    units = db.Column(db.Unicode, nullable=False)
    ingredients = db.Column(db.Unicode, nullable=False)
    recipe = db.Column(db.Unicode, nullable=False)
    def tojson(self):
        post_comments = Comment.query.filter_by(post_id=self.id).all()
        total = 0
        if (len(post_comments) != 0):
            for i in post_comments:
                total += i.rating
            total = float(total)/float(len(post_comments))
        return {
            "id": self.id,
            "post_name": self.post_name,
            "user_id": self.user_id,
            "ingredients": self.ingredients,
            "recipe": self.recipe,
            "userinfo": User.query.get(self.user_id).tojson(),
            "rating": total,
            "numcomments": len(post_comments)
        }

class Comment(db.Model):
    __tablename__ = 'Comments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Unicode, db.ForeignKey('Posts.id'))
    user_id = db.Column(db.Unicode, db.ForeignKey('Users.id'))
    text = db.Column(db.Unicode, nullable=False)
    rating = db.Column(db.Unicode, nullable=False)
    def tojson(self):
        return {
            "id": self.id,
            "post_id": self.post_id,
            "user_id": self.user_id,
            "text": self.text,
            "rating": self.rating,
            "postinfo": (Post.query.get(self.post_id)).tojson()
        }

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
        if bool(db_user) and (db_user.username == temp_username) and (db_user.password == temp_password):
            #TODO: Finalize login stage
            login_user(db_user)
            session["userid"] = db_user.id 
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
    session['is_submitted'] = "False"
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

    return redirect(url_for('get_login'))

@app.get("/ingredients/")
@login_required
def get_pre_post():
    form = PrePostForm()
    return render_template("prepost.html", form=form)


@app.post("/ingredients/")
@login_required
def post_pre_post():
    form = PrePostForm()
    if not form.validate():
        for field,error in form.errors.items():
            flash(f"{field} - {error}")
        return redirect(url_for("get_pre_post"))
    
    ingredients = form.num_ingredients.data
    units = form.units.data
    session['num_ingredients'] = ingredients
    session['units'] = units
    session['is_submitted'] = "True"

    return redirect(url_for("get_post"))


@app.get("/post/")
@login_required
def get_post():
    if(session['is_submitted'] == "True"):
        session['is_submitted'] = "False"
        form = Post_Form()
        num = session['num_ingredients']
        units = session['units']

        fields = []
        u_fields = []
        names = []
        quantities = []
        im_units = []
        m_units = []
        for x in range(0, num):
            ingredient = IngrediantForm()
            ingredient.name.label = f"Ingredient {x+1}"
            ingredient.name.name = f"Ingredient {x+1}"
            ingredient.quantity.name = f"Quantity {x+1}"
            ingredient.im_units.name = f"im_units {x+1}"
            ingredient.m_units.name = f"m_units {x+1}"
            fields.append(ingredient)
            names.append(ingredient.name.name)
            quantities.append(ingredient.quantity.name)
            m_units.append(ingredient.m_units.name)
            im_units.append(ingredient.im_units.name)




    # Try this, maybe?
        form.ingredients = fields
        form.units = u_fields
        session['ingredients'] = names
        session['quantities'] = quantities
        session['metric'] = m_units
        session['imperial'] = im_units

    # if (pre_form.is_submitted() == False):
        # return redirect(url_for("get_pre_post"))
        return render_template("post.html", form=form, num=num, units=units, ingredient=ingredient)
    else:
        return redirect(url_for("get_pre_post"))
    
@app.post("/post/")
@login_required
def post_post():
    form = Post_Form()
    
    if not form.validate():
        for field,error in form.errors.items():
            flash(f"{field} - {error}")
        return redirect(url_for("get_post"))
   
    session_names = session['ingredients']
    session_quan = session['quantities']
    session_metric = session['metric']
    session_imperial = session['imperial']
    
    print(session_names)
    print(session_quan)
    
    for i in range(len(session_names)):
        name = request.form.get(session_names[i])
        quantity = request.form.get(session_quan[i])
                

    
    post_name = form.post_name.data
    #user_id = session["username"]
    recipe = form.recipe.data
    #user_id placeholder
    units = session['units']
    ingredients= ""
    # x = form.ingredients
    for i in range(len(session_names)):
        name = request.form.get(session_names[i])
        quantity = request.form.get(session_quan[i])
        if (session['units'] == "Metric"):
            units = request.form.get(session_metric[i])
        else:
            units = request.form.get(session_imperial[i])
        ingredients += str(name) + ", " + str(quantity) + ", " + str(units) + "\n"


    new_post = Post(post_name=post_name, user_id = 1, units=units, ingredients=ingredients , recipe=recipe)
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

@app.route("/profile/")
@login_required
def user_profile():
    usernum = session.get("userid")
    return redirect(f"/profile/{usernum}")

@app.route("/profile/<int:userid>/")
def profile_view(userid):  # VIEWING A PERSON'S PROFILE PAGE WITH ALL OF THEIR RECIPE POSTS
    profile_user = User.query.filter_by(id=userid).first()
    return render_template("profile.html", user=profile_user)

@app.route("/profile/<int:userid>/posts/")  # VIEWING ALL POSTS OF THE USER
def profile_posts(userid):
    profile_user = User.query.filter_by(id=userid).first()
    return render_template("allposts.html", user=profile_user)

@app.route("/profile/<int:userid>/comments/") # VIEWING ALL COMMENTS OF THE USER
def profile_comments(userid):
    profile_user = User.query.filter_by(id=userid).first()
    return render_template("allcomments.html", user=profile_user)

@app.route("/profile/<int:userid>/jsondump/") # JSON FOR AJAX
def user_json_dump(userid):
    post_info = Post.query.filter_by(user_id=userid).order_by(desc(Post.id)).all()
    postArray = []
    comment_info = Comment.query.filter_by(user_id=userid).order_by(desc(Comment.id)).all()
    commentArray = []
    for i in post_info:
        postArray.append(i.tojson())

    for i in comment_info:
        commentArray.append(i.tojson())

    return {
        "posts":postArray,
        "comments":commentArray
    }

@app.route("/explore/")
@app.route("/explore/<int:postid>/")
def explore_page(postid=0):
    logged_in = False
    if 'userid' in session.keys():
        logged_in = True
    if (postid == 0): #TODO: If there is no postid, then display the page with AJAX
        #TODO ADD AJAX, FOR MIDPOINT WE WILL JUST DISPLAY STUFF HERE
        all_posts = Post.query.order_by(Post.id).all()
        return render_template("homepage.html", posts=all_posts, logged_in=logged_in)
    #TODO: Then display the actual post itself in full-view mode
    selected_post = Post.query.get(postid)
    original_poster = User.query.get(selected_post.user_id)
    if (selected_post != None):
        return render_template("view_post.html", post=selected_post.tojson(), user=original_poster.tojson())
    return "This post does not exist.", 404

@app.route("/explore/postjsondump/")
def explore_json():
    all_posts = Post.query.order_by(desc(Post.id)).all()
    return [i.tojson for i in all_posts]

@app.route("/logout/")
@login_required
def logout_page():
    del session["userid"]
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("get_login"))