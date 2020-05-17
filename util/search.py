from flask import Blueprint,render_template,request
from flask_pagination import Pagination
from db.search import searchitems
search=Blueprint('search',__name__)
# @search.route('/search',classmethod=('GET','POST'))
# def searchtest():
#     #由后端传送文件的示范
#     file="/images/test.jpg"
#     return render_template('search_web_page.html',file=file)
@search.route('/search')
def searchtest():
    return render_template('search_web_page.html')
@search.route('/testsearch/')
def searchs():
    items=searchitems('test')[0]
    print(items)
    return render_template('testsearch.html',itemname=items[1],name=items[2])
#搜索分类列表及分类物品
#物品列表：物品id，物品图片，物品名，卖家名字，卖家信誉度，物品介绍信息
#更换排序（名字，卖家信誉度，买家喜爱度（可取舍该功能）
