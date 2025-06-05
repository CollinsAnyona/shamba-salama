from app.extensions import db
from .models import Post, Reply, Category
from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user
from datetime import datetime
from . import posts_bp


@posts_bp.route("/forums", methods=["GET", "POST"])
def forums():
    categories = Category.query.all()
    return render_template("forums.html", categories=categories)

@posts_bp.route("/expert-forums", methods=["GET", "POST"])
def expert_forums():
    categories = Category.query.all()
    return render_template("expert-forums.html", categories=categories)


@posts_bp.route("/expert-category/<int:category_id>")
def expert_view_category(category_id):
    category = Category.query.get(category_id)
    if category:
        posts = Post.query.filter_by(category_id=category_id).all()
        return render_template(
            "expert-category-post.html",
            category=category,
            posts=posts,
            category_id=category_id,
        )
    else:
        flash("Category not found.", "danger")
        return redirect(url_for("bookings.bookings"))


@posts_bp.route("/category/<int:category_id>")
def view_category(category_id):
    category = Category.query.get(category_id)
    if category:
        posts = Post.query.filter_by(category_id=category_id).all()
        return render_template(
            "category-post.html",
            category=category,
            posts=posts,
            category_id=category_id,
        )
    else:
        flash("Category not found.", "danger")
        return redirect(url_for("main.home"))


@posts_bp.route("/category/<int:category_id>/posts", methods=["GET", "POST"])
def category_posts(category_id):
    category = Category.query.get_or_404(category_id)
    posts = Post.query.filter_by(category_id=category_id).all()

    # Handling the creation of a new post
    if (
        request.method == "POST"
        and "title" in request.form
        and "content" in request.form
    ):
        title = request.form["title"]
        content = request.form["content"]

        # Handle user ID: if the user is logged in, use their ID; else, handle anonymous posts
        user_id = current_user.id if current_user.is_authenticated else None

        # Log the data for debugging
        posts_bp.logger.debug(
            f"Creating post with title: {title}, content: {content}, user_id: {user_id}, category_id: {category.id}"
        )

        new_post = Post(
            title=title, content=content, category_id=category.id, user_id=user_id
        )
        db.session.add(new_post)
        db.session.commit()

        flash("Post created successfully!", "success")
        return redirect(url_for("posts.category_posts", category_id=category.id))

    return render_template("category-post.html", category=category, posts=posts)

@posts_bp.route("/expert-category/<int:category_id>/posts", methods=["GET", "POST"])
def expert_category_posts(category_id):
    category = Category.query.get_or_404(category_id)
    posts = Post.query.filter_by(category_id=category_id).all()

    # Handling the creation of a new post
    if (
        request.method == "POST"
        and "title" in request.form
        and "content" in request.form
    ):
        title = request.form["title"]
        content = request.form["content"]

        # Handle user ID: if the user is logged in, use their ID; else, handle anonymous posts
        user_id = current_user.id if current_user.is_authenticated else None

        # Log the data for debugging
        posts_bp.logger.debug(
            f"Creating post with title: {title}, content: {content}, user_id: {user_id}, category_id: {category.id}"
        )

        new_post = Post(
            title=title, content=content, category_id=category.id, user_id=user_id
        )
        db.session.add(new_post)
        db.session.commit()

        flash("Post created successfully!", "success")
        return redirect(url_for("posts.expert_category_posts", category_id=category.id))

    return render_template("expert-category-post.html", category=category, posts=posts)

@posts_bp.route("/expert-view_post/<int:post_id>")
def expert_view_post(post_id):
    # Get the post by ID
    post = Post.query.get_or_404(post_id)

    # Get all replies for this post
    replies = Reply.query.filter_by(post_id=post_id).all()

    return render_template("expert-view_post.html", post=post, replies=replies)



@posts_bp.route("/expert-reply_to_post", methods=["POST"])
def expert_reply_to_post():
    content = request.form["reply_content"]
    post_id = request.form["post_id"]
    reply_author = request.form.get(
        "reply_author"
    )  # Get the value of the reply_author field

    # Check if the user wants to post anonymously or as themselves
    if current_user.is_authenticated:
        user_id = current_user.id  # Regular user posting
    else:
        user_id = None  # Anonymous if not logged in

    # Create the reply
    reply = Reply(
        content=content, created_at=datetime.utcnow(), user_id=user_id, post_id=post_id
    )
    db.session.add(reply)
    db.session.commit()

    return redirect(url_for("posts.expert_view_post", post_id=post_id))





@posts_bp.route("/view_post/<int:post_id>")
def view_post(post_id):
    # Get the post by ID
    post = Post.query.get_or_404(post_id)

    # Get all replies for this post
    replies = Reply.query.filter_by(post_id=post_id).all()

    return render_template("view_post.html", post=post, replies=replies)





@posts_bp.route("/reply_to_post", methods=["POST"])
def reply_to_post():
    content = request.form["reply_content"]
    post_id = request.form["post_id"]
    reply_author = request.form.get(
        "reply_author"
    )  # Get the value of the reply_author field

    # Check if the user wants to post anonymously or as themselves
    if current_user.is_authenticated:
        user_id = current_user.id  # Regular user posting
    else:
        user_id = None  # Anonymous if not logged in

    # Create the reply
    reply = Reply(
        content=content, created_at=datetime.utcnow(), user_id=user_id, post_id=post_id
    )
    db.session.add(reply)
    db.session.commit()

    return redirect(url_for("posts.view_post", post_id=post_id))

