import email
from click import password_option
from flask import Flask, jsonify, render_template, url_for, redirect, flash, session, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from flask_login import login_required, login_user, LoginManager, logout_user, UserMixin, current_user
import os
from unitconvert import volumeunits, massunits



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
    converted_ingredients = db.Column(db.Unicode, nullable=False)
    recipe = db.Column(db.Unicode, nullable=False)
    # numlikes = db.Column(db.Integer, nullable=False)
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
            # "numlikes": self.numlikes,
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
    rating = db.Column(db.Integer, nullable=False)
    def tojson(self):
        return {
            "id": self.id,
            "post_id": self.post_id,
            "user_id": self.user_id,
            "text": self.text,
            "rating": self.rating,
            "postinfo": Post.query.get(self.post_id).tojson(),
            "userinfo": User.query.get(self.user_id).tojson()
        }

with app.app_context():
    db.drop_all()
    db.create_all()
    #Creatin users i can use when testing as well a couple posts
    philippe = User(username = "philippe_", email="phillewis16@gmail.com", password="Phillewis16")
    post1 = Post(post_name="Lasagna", user_id=1, units="Metric", ingredients="egg, 2, None ", converted_ingredients = "egg, None, 2 ", recipe = "Do THis \n then do this")
    post2 = Post(post_name="Yes", user_id=1, units="Metric", ingredients="egg, 2, None ", converted_ingredients = "egg, None, 2 ", recipe = "Do THis \n then do this")
    db.session.add_all((post1, post2, philippe))
    db.session.commit()

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
    session['user'] = username
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
   
    user = session['user']
    grab_user = User.query.filter_by(username=user).first()
    user_id = grab_user.id
    

    session_names = session['ingredients']
    session_quan = session['quantities']
    session_metric = session['metric']
    session_imperial = session['imperial']
    
    for i in range(len(session_names)):
        name = request.form.get(session_names[i])
        quantity = request.form.get(session_quan[i])
                

    
    post_name = form.post_name.data
    #user_id = session["username"]
    recipe = form.recipe.data
    #user_id placeholder
    units = session['units']
    ingredients= ""
    converted_ingredients =""
    # x = form.ingredients
    for i in range(len(session_names)):
        name = request.form.get(session_names[i])
        quantity = request.form.get(session_quan[i])
        if (session['units'] == "Metric"):
            measure = request.form.get(session_metric[i])
            converted = (convert_units("Metric", quantity, measure))
        else:
            measure = request.form.get(session_imperial[i])
            converted = (convert_units("Imperial", quantity, measure))
        ingredients += str(name) + ", " + str(quantity) + ", " + str(measure) + "\n"
        converted_ingredients += str(name) + ", " + str(converted) + "\n"
        
    
    


    new_post = Post(post_name=post_name, user_id = user_id, units=units, ingredients=ingredients, converted_ingredients=converted_ingredients, recipe=recipe)
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
    posts = Post.query.filter_by(user_id=userid).all()
    return render_template("allposts.html", user=profile_user, posts=posts)

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
        searchbar = request.args.get("search", default="", type=str)
        all_posts = Post.query.order_by(Post.id).all()

        return render_template("homepage.html", posts=all_posts, logged_in=logged_in, search=searchbar)
    #TODO: Then display the actual post itself in full-view mode
    selected_post = Post.query.get(postid)
    original_poster = User.query.get(selected_post.user_id)
    if (selected_post != None):
        return render_template("view_post.html", post=selected_post.tojson(), user=original_poster.tojson(), logbool=logged_in)
    return "This post does not exist.", 404

@app.post("/explore/<int:postid>/addcomment/")
@login_required
def add_new_comment(postid):
    # THIS IS WHERE THE JS WILL SEND A POST TO ADD A NEW COMMENT
    get_commentjson = request.get_json()
    # print(get_commentjson)
    new_comment = Comment(post_id=postid, text=get_commentjson.get("text"), rating=int(get_commentjson.get("rating")), user_id=session.get("userid"))
    db.session.add(new_comment)
    db.session.commit()
    return "Comment added successfully.", 201

@app.get("/explore/postjsondump/")
def explore_json():
    all_posts = Post.query.order_by(desc(Post.id)).all()
    return [i.tojson() for i in all_posts]

@app.route("/explore/<int:postid>/commentjsondump/")
def all_comment_json(postid):
    all_postcomments = Comment.query.filter_by(post_id=postid).order_by(desc(Comment.id)).all()
    return [i.tojson() for i in all_postcomments]

@app.route("/logout/")
@login_required
def logout_page():
    del session["userid"]
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("get_login"))

def convert_units(units, quantity, meausure):
    if units == "Metric":
        # for units in ingredients.split("\n"):
        if (meausure == "ml"):
                convert = round(volumeunits.VolumeUnit(int(quantity), 'ml', 'cup').doconvert(), 2)
                print(convert)
                return (str(convert) + ", " + "cup")
        if (meausure == "l"):
                convert = round(volumeunits.VolumeUnit(int(quantity), 'l', 'cup').doconvert(), 2)
                print(convert)
                return (str(convert) + ", " + "cup")
        if (meausure == "mg"):
                convert = round(massunits.MassUnit(int(quantity), 'mg', 'oz').doconvert(), 2)
                return (str(convert) + ", " + "oz")
        if (meausure == "g"): 
                convert = round(massunits.MassUnit(int(quantity), 'g', 'oz').doconvert(), 2)
                return (str(convert) + ", " + "oz")
        if (meausure == "kg"):
                convert = round(massunits.MassUnit(int(quantity), 'kg', 'lb').doconvert(), 2)
                return (str(convert) + ", " + "lb")
        if (meausure == "None"):
                return (meausure + ", " + quantity)
    if units == "Imperial":
        #TODO: Implement the imperial side (same as above just in reverse)
        if (meausure == "tsp"):
                convert = round(volumeunits.VolumeUnit(int(quantity), 'tsp', 'ml').doconvert(), 2)
                print(convert)
                return (str(convert) + ", " + "ml")
        if (meausure == "l"):
                convert = round(volumeunits.VolumeUnit(int(quantity), 'tbsp', 'ml').doconvert(), 2)
                print(convert)
                return (str(convert) + ", " + "ml")
        if (meausure == "mg"):
                convert = round(massunits.MassUnit(int(quantity), 'floz', 'ml').doconvert(), 2)
                return (str(convert) + ", " + "ml")
        if (meausure == "g"): 
                convert = round(massunits.MassUnit(int(quantity), 'cup', 'ml').doconvert(), 2)
                return (str(convert) + ", " + "ml")
        if (meausure == "kg"):
                convert = round(massunits.MassUnit(int(quantity), 'gal', 'l').doconvert(), 2)
                return (str(convert) + ", " + "l")
        if (meausure == "tsp"):
                convert = round(volumeunits.VolumeUnit(int(quantity), 'oz', 'g').doconvert(), 2)
                print(convert)
                return (str(convert) + ", " + "g")
        if (meausure == "l"):
                convert = round(volumeunits.VolumeUnit(int(quantity), 'lb', 'kg').doconvert(), 2)
                print(convert)
                return (str(convert) + ", " + "kg")
        if (meausure == "None"):
                return (meausure + ", " + quantity)
        pass
