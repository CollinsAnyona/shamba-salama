import os
from flask import request, session, redirect, url_for, flash, render_template, current_app
from .models import Product
from app.extensions import db
from . import products_bp
from werkzeug.utils import secure_filename

@products_bp.route("/market", methods=["GET", "POST"])
def market():
    '''
    Displays the product marketplace and handles adding items to the cart.

    GET: Renders a list of available products.
    POST: Adds selected product and quantity to the user's session-based cart.
    '''
    if request.method == "POST":
        product_id = int(request.form["product_id"])
        quantity = int(request.form["quantity"])

        # Initialize the cart if it doesn't exist
        if "cart" not in session:
            session["cart"] = []

        # Retrieve product from the database
        product = Product.query.get_or_404(product_id)

        # Add product and quantity to the cart
        session["cart"].append(
            {
                "product_id": product.id,
                "name": product.name,
                "price": product.price,
                "quantity": quantity,
            }
        )
        session.modified = True  # Ensure changes are saved to session

        flash(f"Added {quantity} of {product.name} to your cart!", "success")
        return redirect(url_for("products.market"))

    # Fetch all products from the database to display in the market
    products = Product.query.all()
    return render_template(
        "market.html", products=products, cart=session.get("cart", [])
    )

UPLOAD_FOLDER = os.path.join("app", "static", "img")  
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS   

@products_bp.route("/add_product", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        name = request.form["name"]
        price = float(request.form["price"])
        description = request.form["description"]
        image = request.files["image_file"]

        if image.filename == "":
            flash("No selected file", "danger")
            return redirect(request.url)

        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)

            # Save to static/img folder
            image_path = os.path.join(current_app.static_folder, "img", filename)
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            image.save(image_path)

            # Define image_url as filename (can be used in HTML)
            image_url = filename
        else:
            flash("Invalid image file format.", "error")
            return redirect(url_for("products.add_product"))

        # Create and save product
        new_product = Product(
            name=name, price=price, description=description, image_url=image_url
        )
        db.session.add(new_product)
        db.session.commit()

        flash("New product added successfully!", "success")
        return redirect(url_for("products.market"))

    return render_template("add_product.html")

@products_bp.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    '''
    Handles logic for adding a specific product to the cart.

    Validates product ID and quantity, and updates the session-based cart accordingly.
    '''
    # Retrieve the product ID and quantity from the form
    product_id = request.form.get("product_id")
    quantity = request.form.get("quantity", 1)

    # Convert quantity to an integer and check for valid values
    try:
        quantity = int(quantity)
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
    except ValueError:
        flash("Invalid quantity provided.", "error")
        return redirect(
            url_for("products.market")
        )  # Redirect to market page if there's an issue

    # Check if the product ID is valid and exists in the database
    product = Product.query.get(product_id)
    if product:
        # Ensure the 'cart' key exists in the session
        if "cart" not in session:
            session["cart"] = []

        # Check if the product is already in the cart
        existing_product = next(
            (item for item in session["cart"] if item["product_id"] == product.id), None
        )
        if existing_product:
            # If the product is already in the cart, just update the quantity
            existing_product["quantity"] += quantity
        else:
            # If the product is not in the cart, add it
            session["cart"].append(
                {
                    "product_id": product.id,
                    "name": product.name,
                    "price": product.price,
                    "quantity": quantity,
                    "total_price": product.price
                    * quantity,  # Adding total price directly to the cart
                }
            )

        session.modified = True  # Mark the session as modified
        flash("Product added to cart!", "success")
    else:
        flash("Product not found.", "error")

    return redirect(url_for("products.market"))  # Redirect to market page after adding to cart


@products_bp.route("/remove_from_cart", methods=["POST"])
def remove_from_cart():
    '''
    Removes a specified product from the cart.

    Takes the product ID from form data and updates the cart in the session.
    '''
    product_id = int(request.form["product_id"])

    # Remove the product from the cart by filtering out the item with the matching product_id
    session["cart"] = [
        item for item in session.get("cart", []) if item["product_id"] != product_id
    ]

    # Ensure changes are saved to the session
    session.modified = True

    flash("Product removed from cart!", "success")
    return redirect(url_for("products.cart"))


@products_bp.route("/cart")
def cart():
    '''
    Displays the current contents of the user's cart.

    Calculates and shows total price based on session data and product info.
    '''
    # Retrieve cart items from the session
    cart_items = session.get("cart", [])
    updated_cart = []

    # Retrieve product details for each item in the cart from the database
    total_price = 0
    for item in cart_items:
        product = Product.query.get(item["product_id"])
        if product:
            item_total = product.price * item["quantity"]
            total_price += item_total
            updated_cart.append(
                {
                    "product_id": product.id,
                    "name": product.name,
                    "price": product.price,
                    "quantity": item["quantity"],
                    "total_price": item_total,
                }
            )

    # Pass the updated cart and total price to the template
    return render_template("cart.html", cart=updated_cart, total_price=total_price)


@products_bp.route("/checkout", methods=["GET", "POST"])
def checkout():
    '''
    Handles the checkout process and payment form validation.

    GET: Renders the checkout page with current cart and total.
    POST: Validates payment details and user info, clears the cart, and confirms the order.
    '''
    # Retrieve cart items from session
    cart = session.get("cart", [])
    total_price = sum(item["price"] * item["quantity"] for item in cart)

    if request.method == "POST":
        # Get form data
        full_name = request.form.get("full_name")
        address = request.form.get("address")
        phone = request.form.get("phone")
        payment_method = request.form.get("payment_method")

        # Validate Mobile Money payment
        if payment_method == "mobile_money":
            mpesa_number = request.form.get("mpesa_number")
            if not mpesa_number:
                flash(
                    "Please enter your mobile number for Mobile Money payment.", "error"
                )
                return redirect(url_for("products.checkout"))

        # Validate Card payment
        elif payment_method == "card":
            card_number = request.form.get("card_number")
            card_cvv = request.form.get("card_cvv")
            expiry_date = request.form.get("expiry_date")
            if not card_number or not card_cvv or not expiry_date:
                flash(
                    "Please fill in all card details (Card Number, CVV, Expiry Date).",
                    "error",
                )
                return redirect(url_for("products.checkout"))

        # If payment details are valid, process the order
        flash("Your order has been successfully placed!", "success")

        # Save order details in a temporary dictionary
        order_details = {
            "full_name": full_name,
            "address": address,
            "phone": phone,
            "payment_method": payment_method,
            "cart_items": cart,
            "total_price": total_price,
        }

        # Clear the cart after successful checkout
        session.pop("cart", None)

        # Redirect to the order confirmation page
        return redirect(url_for("products.order_confirmation"))

    # Render the checkout page with the cart items and total price
    return render_template("checkout.html", cart=cart, total_price=total_price)


@products_bp.route("/order_confirmation", methods=["GET"])
def order_confirmation():
    '''
    Displays a confirmation message after successful checkout.
    '''
    return render_template("order_confirmation.html")

@products_bp.route("/delete_product/<int:product_id>", methods=["POST"])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash("Product deleted successfully!", "success")
    return redirect(url_for("products.market"))
