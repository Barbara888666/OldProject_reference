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
    # 1. visitor（CHANGE PERSONAL INFORMATION）
    visitor = CMSRole(name='Visitor',desc='personal')
    visitor.permissions = CMSPermission.PERSONAL
    # 2. operator（CHANGE PERSONAL INFORMATION，FRONT DATA）
    operator = CMSRole(name='Front',desc='personal,front data')
    operator.permissions = CMSPermission.PERSONAL|CMSPermission.PRODUCT|\
                           CMSPermission.COMMENT|CMSPermission.FRONTUSER|\
                           CMSPermission.BOARD
    # 3. Manager（MORE IS CMS USER）
    manager = CMSRole(name='Manager',desc='personal,front data,CMSuser')
    manager.permissions = CMSPermission.PERSONAL|\
                        CMSPermission.PRODUCT|CMSPermission.CMSUSER|\
                        CMSPermission.COMMENT|CMSPermission.FRONTUSER|\
                        CMSPermission.BOARD
    # 4. boss（ALL PERMISSION）
    boss = CMSRole(name='Boss',desc='All permissions')
    boss.permissions = CMSPermission.ALL_PERMISSION

    db.session.add_all([visitor,operator,manager,boss])
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