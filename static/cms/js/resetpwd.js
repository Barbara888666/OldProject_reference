
$(function () {
    $("#submit").click(function (event) {
        // event.preventDefault
        event.preventDefault();

        var oldpwdE = $("input[name=oldpwd]");
        var newpwdE = $("input[name=newpwd]");
        var newpwd2E = $("input[name=newpwd2]");

        var oldpwd = oldpwdE.val();
        var newpwd = newpwdE.val();
        var newpwd2 = newpwd2E.val();

        // 1. 要在模版的meta标签中渲染一个csrf-token
        // 2. 在ajax请求的头部中设置X-CSRFtoken
        zlajax.post({
            'url': '/cms/resetpwd/',
            'data': {
                'oldpwd': oldpwd,
                'newpwd': newpwd,
                'newpwd2': newpwd2
            },
            'success': function (data) {
                if (data['code']== 200){
                    alert.alertSuccessToast("Congrulations! Change Password Success!");
                    oldpwdE.val("");
                    newpwdE.val("");
                    newpwd2E.val("");
                 }else{
                    var message=data['message'];
                    alert.alertInfo(message)
                }
                console.log(data);
            },
            'fail': function (error) {
                console.log(error);
                alert.alertNetworkError();
            }
        });
    });
});