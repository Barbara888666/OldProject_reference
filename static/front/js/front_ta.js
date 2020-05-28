$(function () {
    $("#follow-btn").click(function (event) {
        event.preventDefault();
        var loginTag = $("#login-tag").attr("data-is-login");
        if(!loginTag){
            alert.alertInfoToast("请登陆后再关注！")
            window.location = '/signin/';
        }else{
            var user_id = $("#top-ta").attr("data-da");
            zlajax.post({
                'url': '/afollow/',
                'data':{
                    'user_id': user_id
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