$(function () {
    $("#submit-product-btn").click(function (event) {
        event.preventDefault();
        var nameInput = $('input[name="name"]');
        var priceInput = $("input[name='price']");
        var boardSelect = $("select[name='board_id']");
        var situationSelect = $("select[name='situation']");
        var termSelect = $("select[name='term']");
        var descpiptionInput = $("input[name='descpiption']");
        // var fileInput =$('#pic').fileinput
        // var fileInput = $("input[name='pic']");


        var name = nameInput.val();
        var price = priceInput.val();
        var board_id = boardSelect.val();
        var situation = situationSelect.val();
        var term = termSelect.val();
        var descpiption = descpiptionInput.val();

        zlajax.post({
            'url': '/aproduct/',
            'data': {
                'name': name,
                'price':price,
                'board_id': board_id,
                'situation':situation,
                'term':term,
                'description':descpiption,
                // 'file':fileInput,
            },
            'success': function (data) {
                if(data['code'] == 200){
                    alert.alertConfirm({
                        'msg': 'congratulations! Successful product launch!',
                        'cancelText': 'Back to Home',
                        'confirmText': 'Upload again',
                        'cancelCallback': function () {
                            window.location = '/';
                        },
                        'confirmCallback': function () {
                            window.location = '/aproduct/';
                        }
                    });
                }else{
                    alert.alertInfo(data['message']);
                }
            }
        });
    });
});