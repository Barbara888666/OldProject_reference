from flask import Blueprint,render_template
from db.search import searchitem,searchitemimgs
from util import getitemimgpath
detail=Blueprint('detail',__name__)
@detail.route('/detail/<int:itemid>')
def details(itemid):
    item=searchitem(str(itemid))
    itemimgs=searchitemimgs(itemid)
    t=None
    if itemimgs[0][0]!='None':
        t=getitemimgpath(itemid,itemimgs[0][0])

    return render_template('detail.html',items=item,itemimgs=itemimgs)
#商品名字，商品分类，商品描述，卖家