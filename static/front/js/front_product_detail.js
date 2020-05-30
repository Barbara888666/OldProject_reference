$(function () {
    $("#comment-btn").click(function (event) {
        event.preventDefault();
        var loginTag = $("#login-tag").attr("data-is-login");
        if(!loginTag){
            alert.alertInfoToast("请登陆后再评论！")
            window.location = '/signin/';
        }else{
            var product_id = $("#product-information").attr("data-da");
            var contentIput = $("input[name='comment-content']");

            var content =contentIput.val();
            zlajax.post({
                'url': '/acomment/',
                'data':{
                    'content': content,
                    'product_id': product_id
                },
                'success': function (data) {
                    if(data['code'] == 200){//都是这样 都有的
                        window.location.reload();
                    }else{
                        alert.alertInfo(data['message']);
                    }
                }
            });
        }
    });
});

$(function () {
    $("#like-btn").click(function (event) {
        event.preventDefault();
        var loginTag = $("#login-tag").attr("data-is-login");
        if(!loginTag){
            alert.alertInfoToast("请登陆后再点赞！")
            window.location = '/signin/';
        }else{
            var product_id = $("#product-information").attr("data-da");
            zlajax.post({
                'url': '/alike/',
                'data':{
                    'product_id': product_id
                },
                'success': function (data) {
                    if(data['code'] == 200){
                        window.location.reload();
                    }else{
                        alert.alertInfo(data['message']);
                    }
                }
            });
        }
    });
});

$(function () {
    $("#delete-comment-btn").click(function (event) {
        event.preventDefault();
        var loginTag = $("#login-tag").attr("data-is-login");
        if(!loginTag){
            alert.alertInfoToast("请登陆后再点赞！")
            window.location = '/signin/';
        }else{
            var comment_id = $("#comment-info-group").attr("data-da");
            alert.alertConfirm({
            "msg":"您确定要删除这个评论吗？",
            'confirmCallback': function () {
                zlajax.post({
                    'url': '/dcomment/',
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
        }
    });
});

$(function () {
    $("#have-like-btn").click(function (event) {
        event.preventDefault();
        var loginTag = $("#login-tag").attr("data-is-login");
        if(!loginTag){
            alert.alertInfoToast("请登陆后再点赞！")
            window.location = '/signin/';
        }else{
            var like_id = $("#product-information").attr("data-like");
            console.log(like_id)
            zlajax.post({
                'url': '/dlike/',
                'data':{
                    'like_id': like_id
                },
                'success': function (data) {
                    if(data['code'] == 200){
                        window.location.reload();
                    }else{
                        alert.alertInfo(data['message']);
                    }
                }
            });
        }
    });
});