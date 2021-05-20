from datetime import datetime
from flask import Flask, render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app, send_file
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from app import db
from app.main.forms import EditProfileForm, EmptyForm, PostForm
from app.models import User, Post
from app.main import bp
from flask import send_from_directory
import os



import boto3, botocore

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)


def upload_file_to_s3(file, acl="public-read"):
    filename = secure_filename(file.filename)
    try:
        s3.upload_fileobj(
            file,
            os.getenv("AWS_BUCKET_NAME"),
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )

    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        print("Something Happened: ", e)
        return e

    # after upload file to s3 bucket, return filename of the uploaded file
    return file.filename


@bp.route("/trigger", methods=["POST"])
def create():
    # check whether an input field with name 'user_file' exist
    if 'user_file' not in request.files:
        flash('No user_file key in request.files')
        return redirect(url_for('new'))

    # after confirm 'user_file' exist, get the file from input
    file = request.files['user_file']

    # check whether a file is selected
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('new'))

    # check whether the file extension is allowed (eg. png,jpeg,jpg,gif)
    if file and allowed_file(file.filename):
        output = upload_file_to_s3(file)

        # if upload success,will return file name of uploaded file
        if output:
            # write your code here
            # to save the file name in database

            flash("Success upload")
            print(output)
            return redirect(url_for('main.index'))

        # upload failed, redirect to upload page
        else:
            flash("Unable to upload, try again")
            return redirect(url_for('new'))

    # if file extension not allowed
    else:
        flash("File type not accepted,please try again.")
        return redirect(url_for('new'))



@bp.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(current_app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        print(form.image.data)
        if form.image.data == None:
            print(" Didnt get an image ")
            post = Post(body=form.post.data, img="None", title=form.title.data, author=current_user)
            db.session.add(post)
            db.session.commit()
            flash('Your post is now live!')
            return redirect(url_for('main.index'))
        else:
            print("Got an image")
            assets_dir = os.path.join(
                os.path.dirname(current_app.instance_path), 'app', 'static'
            )
            d = form.image.data
            docname = secure_filename(d.filename)
            # print(docname)
            # print(assets_dir)
            d.save(os.path.join(assets_dir, docname))
            post = Post(body=form.post.data, img=docname, title=form.title.data, author=current_user)
            db.session.add(post)
            db.session.commit()
            flash('Your post is now live!')
            return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.index', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title='Home', form=form,
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.explore', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title='Explore',
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    for post in user.posts:
        print(post.img)
        print(post.title)
        print(post.body)
    next_url = url_for('main.user', username=user.username,
                       page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main.user', username=user.username,
                       page=posts.prev_num) if posts.has_prev else None
    form = EmptyForm()
    return render_template('user.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url, form=form)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@bp.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('main.index'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('main.user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash('You are following {}!'.format(username))
        return redirect(url_for('main.user', username=username))
    else:
        return redirect(url_for('main.index'))


@bp.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('main.index'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('main.user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash('You are not following {}.'.format(username))
        return redirect(url_for('main.user', username=username))
    else:
        return redirect(url_for('main.index'))

@bp.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template('contact.html', title='Contact Us')