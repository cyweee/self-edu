import os

def get_db_path():
    home_dir = os.path.expanduser("~")
    app_dir = os.path.join(home_dir, ".self_edu_app")
    os.makedirs(app_dir, exist_ok=True)
    return os.path.join(app_dir, "data.db")
