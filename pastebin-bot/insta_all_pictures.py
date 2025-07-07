from instaloader import Instaloader, Profile
import threading
import shutil
import os
from dotenv import load_dotenv

load_dotenv()


profile_instance = Instaloader()


def login(profile):
    name = os.getenv("username")
    passw = os.getenv("password")
    profile.login(name, passw)


def fetch_posts(user):
    login(profile_instance)

    try:
        prof = Profile.from_username(profile_instance.context, user)
        print(prof)
        posts = prof.get_posts()
    except:
        raise FileNotFoundError

    for post in posts:
        try:
            task = threading.Thread(
                target=profile_instance.download_post,
                args=(
                    post,
                    user,
                ),
            )
            task.start()
        except:
            print("Skipping due to status code 401")


def profile_delete(username):
    shutil.rmtree(f"{username}")
