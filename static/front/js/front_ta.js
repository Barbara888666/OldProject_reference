$(function () {
    $("#follow-btn").click(function (event) {
        event.preventDefault();
        var loginTag = $("#login-tag").attr("data-is-login");
        if(!loginTag){
            alert.alertInfoToast("Please login then follow！")
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

$(function () {
    $("#have-follow-btn").click(function (event) {
        event.preventDefault();
        var loginTag = $("#login-tag").attr("data-is-login");
        if(!loginTag){
            alert.alertInfoToast("Please login then follow！")
            window.location = '/signin/';
        }else{
            var follow_id = $("#top-ta").attr("data-follow");
            alert.alertConfirm({
            "msg":"Are you sure unfollow?",
            'confirmCallback': function () {
                zlajax.post({
                    'url': '/dfollow/',
                    'data':{
                        'follow_id': follow_id
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
