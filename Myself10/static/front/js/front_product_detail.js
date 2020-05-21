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