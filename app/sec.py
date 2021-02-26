from flask_appbuilder.security.sqla.manager import SecurityManager
from flask_appbuilder.security.views import UserInfoEditView, AuthDBView


from .models import WehaUser
from .sec_forms import WehaUserInfoEdit
from .sec_views import WehaUserDBModelView


class WehaUserInfoEditView(UserInfoEditView):
    form = WehaUserInfoEdit


class WehaAuthDBView(AuthDBView):
    login_template = "weha_login_db.html"

class WehaSecurityManager(SecurityManager):
    user_model = WehaUser
    userdbmodelview = WehaUserDBModelView
    authdbview = WehaAuthDBView
    #userinfoeditview = WehaUserInfoEditView
