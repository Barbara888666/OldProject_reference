$(function () {
    $("#submit-product-btn").click(function (event) {
        event.preventDefault();
        var nameInput = $('input[name="name"]');
        var priceInput = $("input[name='price']");
        var boardSelect = $("select[name='board_id']");
        var situationSelect = $("select[name='situation']");
        var termSelect = $("select[name='term']");
        var descpiptionInput = $("input[name='descpiption']");
        var fileInput =$('#pic').fileinput;
       // alert(fileInput);
        //var file = document.getElementById('pic').files;
         console.log(file);
        // // var file = $("input[name='pic']").file
         var file = $("input[name='pic']").file;
         alert(file.val());
         var formData = new FormData();
    // // 服务端要求参数是 pic1
         formData.append('file',file);
    //
        var name = nameInput.val();
        var price = priceInput.val();
        var board_id = boardSelect.val();
        var situation = situationSelect.val();
        var term = termSelect.val();
        var descpiption = descpiptionInput.val();
        // console.log(file)
        // // var file=fileInput.val();

        zlajax.post({
            'url': '/aproduct_form/',
            'data': {
                'name': name,
                'price':price,
                'board_id': board_id,
                'situation':situation,
                'term':term,
                'description':descpiption,
                'file':fileInput,
                // 'cache': false, //上传文件不需要缓存
                // 'processData': false, // 告诉jQuery不要去处理发送的数据
                // 'contentType': false,

            },
            'success': function (data) {
                if(data['code'] == 200){
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
                }else{
                    alert("ccc")
                    alert.alertInfo(data['message']);
                }
            }
        });
    });
});

// $(function () {
//     $("#pic").click(function (event) {
//         // event.preventDefault();
//         var file = this.file;
//         var formData = new FormData();
//     // 服务端要求参数是 pic1
//         formData.append('file',file);
//         // var fileInput = $("input[name='pic']");
//         // file=fileInput.val()
//         zlajax.post({
//             'url': '/aproduct/',
//             'data': {
//                 'file':formData,
//                 'cache': false, //上传文件不需要缓存
//                 'processData': false, // 告诉jQuery不要去处理发送的数据
//                 'contentType': false,
//             },
//             'success': function () {
//                 console.log('test')
//             }
//         });
//     });
// });