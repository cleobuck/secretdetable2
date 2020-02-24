import os
from werkzeug.utils import secure_filename


from flask_cors import CORS, cross_origin
from flask import Flask, flash, render_template, request, redirect, url_for, jsonify
app = Flask(__name__)
cors = CORS(app, resources={r"/backend/*": {"origins": "http://localhost:3000"}, r"/static/*": {"origins": "http://localhost:3000"}, r"/galleryApi/*": {"origins": "http://localhost:3000"},})



from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Post, Gallery




#Connect to Database and create database session
engine = create_engine(os.environ.get("DATABASE_URI"))
Base.metadata.bind = engine


DBSession = sessionmaker(bind=engine)
session = DBSession()


UPLOAD_FOLDER = "static"
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#############################################
########## FLASK INTERFACE ##################
#############################################

###### BLOG ######

@app.route('/')
@app.route('/posts')
def showPosts():
   posts = session.query(Post).all()
   return render_template("posts.html", posts=posts)



#This will let us Create a new post and save it in our database
@app.route('/posts/new/',methods=['GET','POST'])
def newPost():
   if request.method == 'POST':

       # file upload 
       BLOG_FOLDER = "blog"
       f = request.files['file']

       if not os.path.isdir(UPLOAD_FOLDER):
            os.mkdir(UPLOAD_FOLDER)

       filename = secure_filename(f.filename)
       destination="/".join([UPLOAD_FOLDER, BLOG_FOLDER, filename])
       f.save(destination)

       # database 
       newPost = Post(title = request.form['title'], content = request.form['content'], image="http://localhost:5000/" + destination)
       session.add(newPost)
       session.commit()
       return redirect(url_for('showPosts'))
   else:
       return render_template('newPost.html')


#This will let us Update our posts and save it in our database
@app.route("/posts/<int:post_id>/edit/", methods = ['GET', 'POST'])
def editPost(post_id):
   editedPost = session.query(Post).filter_by(id=post_id).one()
   if request.method == 'POST':
       if request.form['name']:
           editedPost.title = request.form['name']
           return redirect(url_for('showPosts'))
   else:
       return render_template('editPost.html', post = editedPost)

#This will let us Delete our post
@app.route('/posts/<int:post_id>/delete/', methods = ['GET','POST'])
def deletePost(post_id):
   postToDelete = session.query(Post).filter_by(id=post_id).one()
   if request.method == 'POST':
       session.delete(postToDelete)
       session.commit()
       return redirect(url_for('showPosts', post_id=post_id))
   else:
       return render_template('deletePost.html',post = postToDelete)

#### Gallery ####

@app.route('/gallery')
def showImages(): 
    
    images = session.query(Gallery).all()
    return render_template("gallery.html", images=images)

@app.route('/gallery/new', methods=['POST', 'GET'])
def addImage():
    if request.method == "POST":

        # file upload 
        GALLERY_FOLDER = "gallery"
        f = request.files['file']


        if not os.path.isdir(UPLOAD_FOLDER):
            os.mkdir(UPLOAD_FOLDER)

       
        filename = secure_filename(f.filename)
        destination="/".join([UPLOAD_FOLDER, GALLERY_FOLDER, filename])
        f.save(destination)

        # database

        newImage = Gallery(title= request.form['title'], url= destination)
        session.add(newImage)
        session.commit()
        return redirect(url_for('showImages'))
    
    else:
        return render_template('newImage.html')




 ###########################
 ########### API ###########
 ###########################

### BLOG ###

def get_posts():
    posts = session.query(Post).all()
    return jsonify(posts = [b.serialize for b in posts])

def get_post(post_id):
    posts = session.query(Post).filter_by(id = post_id).one()
    return jsonify(posts=posts.serialize)

def createBlogPost(title, content):
    addedPost = Post(title=title, content=content)
    session.add(addedPost)
    session.commit()
    return jsonify(Post=addedPost.serialize)

def updatePost(id, title, content):
    updatedPost = session.query(Post).filter_by(id=id).one()
    if not title:
        updatedPost.title = title
    if not content:
        updatedPost.content = content

    session.add(updatedPost)
    session.commit()
    return "Updated a Post with id %s" % id

def deletePost(id):
    postToDelete = session.query(Post).filter_by(id = id).one()
    session.delete(postToDelete)
    session.commit()
    return 'Removed post with id %s' % id

# routes

@app.route('/backend', methods=['GET', 'POST'])
def postsFunction():
    if request.method=="GET":
        return get_posts()

    elif request.method == "POST":
        title = request.args.get('title', '')
        content = request.args.get('title', '')
        return createBlogPost(title, content)

@app.route('/backend', methods=['GET', 'PUT', 'DELETE']) 
def postFunctionId(id):
    if request.method == "GET":
        return get_post(id)

    elif request.method == "PUT":
        title = request.args.get('title', '')
        content = request.args.get('content', '')
        return updatePost(id, title, content)
    
    elif request.method == "DELETE":
        return deletePost(id)


## gallery ### 

def get_gallery():
    gallery = session.query(Gallery).all()
    return jsonify(gallery = [b.serialize for b in gallery])

# route 

@app.route('/galleryApi', methods=['GET', 'POST'])
def galleryFunction():
    if request.method == "GET":
        return get_gallery()
    
    elif request.method == "POST":
        title = request.args.get('title', '')
       

if __name__ == '__main__':
   app.debug = True
   app.run(host='0.0.0.0', port=5000, use_reloader=False)

