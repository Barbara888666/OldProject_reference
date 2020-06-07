
$(function () {
    $("#delete-comment-btn").click(function (event) {
        var self = $(this);
        var tr = self.parent().parent();
        var comment_id = tr.attr("data-id");
        alert.alertConfirm({
            "msg":"Are you sure delete this comment?",
            'confirmCallback': function () {
                zlajax.post({
                    'url': '/cms/dcomment/',
                    'data':{
                        'comment_id': comment_id
                    },
                    'success': function (data) {
                        if(data['code'] == 200){
                            window.location.reload();
                        }else{
                            alert.alertInfo(data['message']);
                        }
                    }
                })
            }
        });
    });
});
