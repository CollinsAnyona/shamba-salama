from app.utils import (
    create_default_categories,
    create_default_products,
    create_default_experts,
    create_default_expert_users,
    create_default_farmer_users,
)


def create_default_data():
    create_default_categories()
    create_default_products()
    create_default_experts()
    create_default_expert_users()
    create_default_farmer_users()
