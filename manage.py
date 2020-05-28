from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from myself import create_app
from exts import db
from apps.cms import models as cms_models
from apps.front import models as front_models
from apps.models import BannerModel,BoardModel

CMSUser = cms_models.CMSUser
CMSRole = cms_models.CMSRole
CMSPermission = cms_models.CMSPermission

FrontUser =front_models.FrontUser
Product=front_models.Product

app = create_app()

manager = Manager(app)

Migrate(app,db)
manager.add_command('db',MigrateCommand)

@manager.option('-u','--username',dest='username')
@manager.option('-p','--password',dest='password')
@manager.option('-e','--email',dest='email')
def create_cms_user(username,password,email):
    user = CMSUser(username=username,password=password,email=email)
    db.session.add(user)
    db.session.commit()
    print('CMS USER ADD SUCCESS！')
# python manage.py create_cms_user  -u root -p 12345678 -e 123@123.com



@manager.command
def create_role():
    # 1. 访问者（可以修改个人信息）
    visitor = CMSRole(name='Visitor',desc='Only view')
    visitor.permissions = CMSPermission.VISITOR

    # 2. 运营角色（修改个人个人信息，管理帖子，管理评论，管理前台用户）
    operator = CMSRole(name='Front',desc='INFORMATION,PRODUCTS,USERS')
    operator.permissions = CMSPermission.VISITOR|CMSPermission.POSTER|CMSPermission.COMMENTER|CMSPermission.FRONTUSER|CMSPermission.BOARDER

    # 3. 管理员（拥有绝大部分权限）
    admin = CMSRole(name='Manager',desc='All permissions')
    admin.permissions = CMSPermission.VISITOR|CMSPermission.POSTER|CMSPermission.CMSUSER|CMSPermission.COMMENTER|CMSPermission.FRONTUSER|CMSPermission.BOARDER

    # 4. 开发者
    developer = CMSRole(name='Boss',desc='Primary power')
    developer.permissions = CMSPermission.ALL_PERMISSION

    db.session.add_all([visitor,operator,admin,developer])
    db.session.commit()

@manager.option('-e','--email',dest='email')
@manager.option('-n','--name',dest='name')
def add_user_to_role(email,name):
    user = CMSUser.query.filter_by(email=email).first()
    if user:
        role = CMSRole.query.filter_by(name=name).first()
        if role:
            role.users.append(user)
            db.session.commit()
            print('User to be a Role Success！')
        else:
            print('No this Role：%s'%role)
    else:
        print('%s no register!'%email)

@manager.option('-s','--studentnumber',dest='studentnumber')
@manager.option('-t','--telephone',dest='telephone')
@manager.option('-u','--username',dest='username')
@manager.option('-p','--password',dest='password')
def create_front_user(studentnumber,telephone,username,password):
    user = FrontUser(studentnumber=studentnumber,telephone=telephone,username=username,password=password)
    db.session.add(user)
    db.session.commit()
    print('USER ADD SUCCESS！')

@manager.command
def create_test_product():
    for x in range (1,205):
        name = '商品%s'%x
        price = x
        board = BoardModel.query.first()
        user = FrontUser.query.first()
        product=Product(name=name,price=price)
        product.board=board
        product.user=user
        db.session.add(product)
        db.session.commit()
    print('恭喜！测试商品建立成功')

if __name__ == '__main__':
    manager.run()