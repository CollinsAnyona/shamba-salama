from app.extensions import db
from app.posts.models import Category
from app.products.models import Product
from app.users.models import User, Expert

def create_default_categories():
    # Check if categories already exist
    if not Category.query.first():  # If no categories exist, add default ones
        categories = [
            Category(
                name="General Discussion",
                description="A place for general, discussions or questions.",
            ),
            Category(
                name="Introduction to Hydroponics",
                description="For beginners to learn about hydroponics.",
            ),
            Category(
                name="Hydroponic Systems",
                description="Discussing different hydroponic systems like NFT, DWC, and aeroponics.",
            ),
            Category(
                name="Nutrient Management",
                description="Learn how to manage nutrients in hydroponic farming.",
            ),
            Category(
                name="Hydroponic Crops",
                description="Discuss the types of crops that thrive in hydroponics.",
            ),
            Category(
                name="Technology in Hydroponics",
                description="Exploring technologies that aid hydroponic farming.",
            ),
            Category(
                name="Sustainability in Hydroponics",
                description="Discussing how hydroponics contributes to sustainable farming.",
            ),
            Category(
                name="Hydroponic Business Ideas",
                description="Discussing business opportunities in hydroponic farming.",
            ),
        ]
        db.session.add_all(categories)
        db.session.commit()


def create_default_products():
    # Check if any products already exist in the database
    if not Product.query.first():  # If no products exist, add the default ones
        default_products = [
            Product(
                name="Hydroponic Kit",
                price=1000,
                description="A complete kit for hydroponic farming.",
                image_url="kit.jpeg",
            ),
            Product(
                name="LED Grow Light",
                price=800,
                description="High-quality LED lights for optimal plant growth.",
                image_url="led.jpg",
            ),
            Product(
                name="pH Meter",
                price=500,
                description="Measure the pH levels in your hydroponic system.",
                image_url="ph.jpg",
            ),
            Product(
                name="Nutrient Solution",
                price=400,
                description="Essential nutrients for hydroponic plants.",
                image_url="solution.png",
            ),
            Product(
                name="Lettuce Seed",
                price=100,
                description="Very good lettuce seed.",
                image_url="lettuce.jpg",
            ),
        ]
        db.session.add_all(default_products)
        db.session.commit()


def create_default_experts():
    # Check if any experts already exist in the database
    if not Expert.query.first():  # If no experts exist, add the default ones
        default_experts = [
            Expert(
                name="Mr. James Opondo",
                profile_picture="/static/img/jane.jpg",
                specialization="Sustainable Agriculture",
                bio="Mr. Opondo specializes in sustainable farming practices and has been helping farmers for over a decade.",
            ),
            Expert(
                name="Erick Kimani",
                profile_picture="/static/img/mark.jpg",
                specialization="Hydroponics",
                bio="Erick is an expert in hydroponic farming systems, focusing on improving water use efficiency in agriculture.",
            ),
            Expert(
                name="Dr. Jackline Omamo",
                profile_picture="/static/img/emily.jpg",
                specialization="Horticulture",
                bio="Dr. Omamo is a horticulturist with expertise in plant cultivation and advanced growing techniques.",
            ),
        ]
        # Add experts to the session and commit
        db.session.add_all(default_experts)
        db.session.commit()


def create_default_expert_users():
    # Define the default expert users
    default_experts = [
        {
            "username": "James Opondo",
            "email": "james@gmail.com",
            "password": "password123",
            "role": "expert",
            "gender": "Male",
            "profile_image_url": "james.jpg",
        },
        {
            "username": "Erick Kimani",
            "email": "erick@gmail.com",
            "password": "password123",
            "role": "expert",
            "gender": "Male",
            "profile_image_url": "mark.jpg",
        },
        {
            "username": "Jackline Omamo",
            "email": "jackline@gmail.com",
            "password": "password123",
            "role": "expert",
            "gender": "Female",
            "profile_image_url": "emily.jpg",
        },
    ]

    # Add each expert to the database if they don't already exist
    for expert in default_experts:
        user = User.query.filter_by(username=expert["username"]).first()
        if user is None:
            user = User(
                username=expert["username"],
                email=expert["email"],
                role=expert["role"],
                gender=expert["gender"],
                profile_image_url=expert["profile_image_url"],
            )
            user.set_password(expert["password"])  # Hash and set the password
            db.session.add(user)

    # Commit the new users to the database
    db.session.commit()

def create_default_farmer_users():
    default_farmers = [
        {
            "username": "Akinyi Otieno",
            "email": "akinyi@gmail.com",
            "password": "farm123",
            "role": "farmer",
            "gender": "Female",
            "profile_image_url": "female_farmer.jpg",
        },
        {
            "username": "Kiptoo Langat",
            "email": "kiptoo@gmail.com",
            "password": "farm123",
            "role": "farmer",
            "gender": "Male",
            "profile_image_url": "male_farmer.jpg",
        },
    ]

    for farmer in default_farmers:
        user = User.query.filter_by(username=farmer["username"]).first()
        if user is None:
            user = User(
                username=farmer["username"],
                email=farmer["email"],
                role=farmer["role"],
                gender=farmer["gender"],
                profile_image_url=farmer["profile_image_url"],
            )
            user.set_password(farmer["password"])
            db.session.add(user)

    db.session.commit()

