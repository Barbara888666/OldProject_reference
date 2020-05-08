from flask import Blueprint,render_template,request,session,redirect
from db.search import searchuser
from util.utils.fileuploads import uploadavatar,uploadalbum
te=Blueprint('more',__name__)
@te.route('/testmain/')
def tests():
    if 'id' in session:
        t=searchuser(int(session['id']))
        img=uploadavatar('images/test.jpg', "id")
        album=uploadalbum('images/test.jpg','id')
        username=t[0][0]
        email=t[0][1]
        phone = t[0][2]
        return render_template('maintest.html',img=img,username=username,album=album,email=email,phone=phone)
    return redirect('/login')