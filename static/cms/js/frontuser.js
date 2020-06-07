$(function () {
    $(".warning-user-btn").click(function () {
        var self = $(this);
        var tr = self.parent().parent();
        var user_id = tr.attr("data-id");
        zlajax.post({
            'url': '/cms/warnfuser/',
            'data': {
                'user_id': user_id
            },
            'success': function (data) {
                if(data['code'] == 200){
                    alert.alertSuccessToast('Operate successfully!');
                }else{
                    alert.alertInfo(data['message']);
                }
            }
        });
    });
});