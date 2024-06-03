from flask_login import LoginManager


login_manager = LoginManager()

@login_manager.user_loader
def load_user(id : int):
    from backend.models import User
    user = User.query.get(int(id))
    return user # 返回用户对象
