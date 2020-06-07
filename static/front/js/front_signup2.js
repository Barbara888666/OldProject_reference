$(function(){
    $('#captcha-img').click(function (event) {
        var self = $(this);
        var src = self.attr('src'); //??=123
        var newsrc = param.setParam(src,'xx',Math.random());//add params to url
        self.attr('src',newsrc);
    });
});


$(function () {
    $("#sms-captcha-btn").click(function (event) {
        event.preventDefault();
        var self = $(this);//change this js to a JQ
        var telephone = $("input[name='telephone']").val();
        if(!(/^1[345879]\d{9}$/.test(telephone))){
            alert.alertInfoToast('Please enter the correct phone number！');
            return;
        }

        var timestamp = (new Date).getTime();
        var sign= md5(timestamp+telephone+"q3423805gdflvbdfvhsdoa`#$%");
        zlajax.post({
            'url': '/c/sms_captcha/',
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
                            self.text('Send code');
                        }
                    },1000);
                }else{
                    alert.alertInfoToast("The phone is registered");
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
        var studentnumber_input = $("input[name='studentnumber']");
        var username_input = $("input[name='username']");
        var password1_input = $("input[name='password1']");
        var password2_input = $("input[name='password2']");
        var graph_captcha_input = $("input[name='graph_captcha']");

        var telephone = telephone_input.val();
        var sms_captcha = sms_captcha_input.val();
        var studentnumber = studentnumber_input.val();
        var username = username_input.val();
        var password1 = password1_input.val();
        var password2 = password2_input.val();
        var graph_captcha = graph_captcha_input.val();

        if(!telephone){
            console.log(telephone)
            alert.alertInfoToast('Please enter phonenumber！');
            return;
        }
        if(!sms_captcha){
            console.log(sms_captcha)
            alert.alertInfoToast('Please enter the SMS verification code！');
            return;
        }
        if(!studentnumber){
            console.log(studentnumber)
            alert.alertInfoToast('Please enter studentnumber！');
            return;
        }
        if(!username){
            console.log(username)
            alert.alertInfoToast('Please enter username！');
            return;
        }
        if(!password1){
            console.log(password1)
            alert.alertInfoToast('Please enter password！');
            return;
        }
        if(!password2){
            console.log(password2)
            alert.alertInfoToast('Please confirm password！');
            return;
        }
        if(!graph_captcha){
            console.log(graph_captcha)
            alert.alertInfoToast('Please enter the graphic verification code');
            return;
        }
        zlajax.post({
            'url': '/signup/',
            'data': {
                'telephone': telephone,
                'sms_captcha': sms_captcha,
                'studentnumber':studentnumber,
                'username': username,
                'password1': password1,
                'password2': password2,
                'graph_captcha': graph_captcha
            },
            'success': function(data){
                if(data['code'] == 200){
                    window.location = '/signin/';
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

