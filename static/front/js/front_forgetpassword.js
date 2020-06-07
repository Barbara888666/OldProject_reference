$(function () {
    $("#sms-captcha-btn").click(function (event) {
        event.preventDefault();
        var self = $(this);//change this js to a JQ
        var telephone = $("input[name='telephone']").val();
        if(!(/^1[345879]\d{9}$/.test(telephone))){
            alert.alertInfoToast('请输入正确的手机号码！');
            return;
        }
        var timestamp = (new Date).getTime();
        var sign= md5(timestamp+telephone+"q2458805182gdflvbdfvhsdoa`#$%");
        zlajax.post({
            'url': '/c/sms_captcha2/',
            'data':{
                'telephone':telephone,
                'timestamp':timestamp,
                'sign':sign,
            },
            'success':function (data) {
                console.log(data)
                if(data['code']==200){
                    alert.alertSuccessToast("Send Message Success!");
                    self.attr("disabled","disabled");
                    var timeCount=60;
                    var timer = setInterval(function () {
                        timeCount--;
                        self.text(timeCount);
                        if(timeCount<=0){
                            self.removeAttr('disabled');
                            clearInterval(timer);
                            self.text('发送验证码');
                        }
                    },1000);
                }else{
                    alert.alertInfoToast("这个手机没有注册");
                }
            }
        });
    });
});

$(function(){
    $("#submit-btn").click(function(event){
        event.preventDefault();
        var telephone_input = $("input[name='telephone']");
        var sms_captcha_input = $("input[name='sms_captcha']");

        var telephone = telephone_input.val();
        var sms_captcha = sms_captcha_input.val();

        zlajax.post({
            'url': '/forget_password/',
            'data': {
                'telephone': telephone,
                'sms_captcha': sms_captcha,
            },
            'success': function(data){
                if(data['code'] == 200){
                    window.location = '/';
                }else{
                    alert.alertInfo(data['message']);
                }
            },
            'fail': function(){
                alert.alertNetworkError();
            }
        });
    });
});

