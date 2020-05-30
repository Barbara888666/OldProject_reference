$(function () {
    $("#submit-product-btn").click(function (event) {
        event.preventDefault();
        var nameInput = $('input[name="name"]');
        var name = nameInput.val();
        console.log('name')
        console.log(name)
        if(!name){
            console.log(name)
            alert.alertInfoToast('请输入名字！');
            return;
        }
        var priceInput = $("input[name='price']");
        var price = priceInput.val();
        if(!price){
            alert.alertInfoToast('请输入价格！');
            return;
        }

        var boardSelect = $("select[name='board_id']");
        var situationSelect = $("select[name='situation']");
        var termSelect = $("select[name='term']");
        var descpiptionInput = $("input[name='descpiption']");
        var finput=$("#pic").get(0).files;
         var formData = new FormData();
        for(var a=0;a<finput.length;a++){
            formData.append('file',finput[a]);
        }
        formData.append('name',name);
        formData.append('price',price);
        var board_id = boardSelect.val();
        formData.append('board_id',board_id);
        var situation = situationSelect.val();
        formData.append('situation',situation);
        var term = termSelect.val();
        var descpiption = descpiptionInput.val();
        zlajax.post({
            type:'post',
            url: '/aproduct_form/',
            dataType :'text',
            data:formData,
            processData: false,
            contentType: false,
            'success': function (data) {
                console.log(data)
                if(data == "succcess"){ 
                    alert.alertConfirm({
                        'msg': 'congratulations! Successful product launch!',
                        'cancelText': 'Back to Home',
                        'confirmText': 'Upload again',
                        'cancelCallback': function () {
                            alert("bbbbb")
                            window.location = '/';
                        },
                        'confirmCallback': function () {
                            alert("aaaa");
                            window.location = '/aproduct/';
                        }
                    });
                    window.location = '/';
                }else{
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
                    console.log('11111111111111')
                }
            },
            'error': function (err) {
                console.log(err)
            }
        });
    });
});