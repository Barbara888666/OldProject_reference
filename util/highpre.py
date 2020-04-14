from flask import Blueprint,render_template
highpre=Blueprint('highpre',__name__)
@highpre.route('/highpre')
def highpres():
    return render_template('high_predibility_seller.html')
#搜索网站通知列表