$(function () {
    $("#save-cmsuser-btn").click(function (event) {
        event.preventDefault();
        var self = $(this);
        var dialog = $("#cmsuser-dialog");
        var emailInput = $("input[name='email']");
        var usernameInput = $("input[name='username']");
        var permissionSelect = $("select[name='permission']");

        var email = emailInput.val();
        var username = usernameInput.val();
        var permission = permissionSelect.val();

        if(!email ||!username||!permission){
            alert.alertInfoToast('请输入完整的cms用户数据！');
            return;
        }

        zlajax.post({
            "url": '/cms/acmsuser/',
            'data':{
                'email':email,
                'username': username,
                'permission': permission,
            },
            'success': function (data) {
                dialog.modal("hide");
                if(data['code'] == 200){
                    // 重新加载这个页面
                    window.location.reload();
                }else{
                    alert.alertInfo(data['message']);
                }
            },
            'fail': function () {
                alert.alertNetworkError();
            }
        });
    });
});