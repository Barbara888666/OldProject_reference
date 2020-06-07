

$(function(){
    $("#submit-btn").click(function (event) {
        event.preventDefault();
        var telephone_input = $("input[name='telephone']");
        var password_input = $("input[name='password']");
        var remember_input = $("input[name='remember']");

        var telephone = telephone_input.val();
        var password = password_input.val();
        var remember = remember_input.checked ? 1 : 0;


        zlajax.post({
            'url': '/signin/',
            'data': {
                'telephone': telephone,
                'password': password,
                'remember': remember
            },//mei
            'success': function (data) {
                if(data['code'] == 200){
                    var return_to = $("#return-to-span").text();
                    if(return_to){
                        if(return_to=='/signup/'){
                            window.location = '/';
                        }else if(return_to=='/forget_password/'){
                            window.location = '/';
                        }else{
                            window.location = return_to;
                        }
                    }else{
                        window.location = '/';
                    }
                }else{
                    alert.alertInfo(data['message']);
                }
            }
        });
    });
});

$(function () {
    $("#resetpwd-link").click(function (event) {
        event.preventDefault();
        alert.alertConfirm({
                        'msg': 'Reset password means restart signup, are you sure?',
                        'cancelText': 'Wrong Click',
                        'confirmText': 'Sure',
                        'cancelCallback': function () {
                            window.location = '/signin/';
                        },
                        'confirmCallback': function () {
                            window.location = '/forget_password/';
                        }
                    });

    });

});


