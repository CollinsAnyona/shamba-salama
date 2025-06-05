import random

# Define the avatars for male and female
male_avatars = ["profilem1.jpg", "profilem2.png"]
female_avatars = ["profilew1.jpg", "profilew2.jpeg", "profilew3.jpeg"]


def assign_avatar(gender):
    """Assign a random avatar based on gender."""
    if gender == "Male":
        return random.choice(male_avatars)
    elif gender == "Female":
        return random.choice(female_avatars)
    else:
        return "default_avatar.jpg"  # Default avatar if gender is unspecified