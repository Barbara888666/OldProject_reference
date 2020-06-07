$(function(){
    $("#captcha-btn").click(function (event){
        event.preventDefault();
        var email=$("input[name='email']").val()
        if(!email){
            alert.alertInfoToast('Please input the Email');
            return;
        }
        zlajax.get({
            'url':'/cms/email_captcha/',
            'data':{
                'email':email
            },
            'success': function (data) {
                if (data['code']==200){
                    alert.alertSuccessToast('Email Code Send Success!');
                }else{
                    alert.alertInfo(data['message']);
                }
            },
            'fail': function (error) {
                alert.alertNetworkError();
            }
        });
    });
});

$(function(){
    $("#submit").click(function (event){
        event.preventDefault();

        var emailE=$("input[name='email']")
        var captchaE=$("input[name='captcha']")

        var email=emailE.val()
        var captcha=captchaE.val()

        zlajax.post({
            'url':'/cms/resetemail/',
            'data':{
                'email':email,
                'captcha': captcha
            },
            'success': function (data) {
                // if (data['code']==200){
                //     alert.alertSuccessToast('Email Change Success!');
                // }else{
                //     alert.alertInfo(data['message']);
                // }
                if(data['code'] == 200){
                    emailE.val("");
                    captchaE.val("");
                    alert.alertSuccessToast('Operate successfully!');
                }else{
                    alert.alertInfo(data['message']);
                }
            },
            'fail': function (error) {
                alert.alertNetworkError();
            }
        });
    });
});
// $(function () {
//     $("#submit").click(function (event) {
//         event.preventDefault();
//         var emailE = $("input[name='email']");
//         var captchaE = $("input[name='captcha']");
//
//         var email = emailE.val();
//         var captcha = captchaE.val();
//
//         zlajax.post({
//             'url': '/cms/resetemail/',
//             'data': {
//                 'email': email,
//                 'captcha': captcha
//             },
//             'success': function (data) {
//                 if(data['code'] == 200){
//                     emailE.val("");
//                     captchaE.val("");
//                     zlalert.alertSuccessToast('恭喜！邮箱修改成功！');
//                 }else{
//                     zlalert.alertInfo(data['message']);
//                 }
//             },
//             'fail': function (error) {
//                 zlalert.alertNetworkError();
//             }
//         });
//     });
// });