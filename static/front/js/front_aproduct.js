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
        var fileInput = $("#pic").get(0).files[0];
         //$('#pic_img')[0].files[0]
       // alert(fileInput);
        //var file = document.getElementById('pic').files;
        if (!fileInput){
            console.log(name)
            alert.alertInfoToast('请输入图片！');
            return;
        }

         console.log(fileInput);
        // // var file = $("input[name='pic']").file
         // var file = $("input[name='pic']").files;
        //var file = $("input[name='pic']").val();
        //alert(file);

         var formData = new FormData();
    // // 服务端要求参数是 pic1
         formData.append('file',fileInput);

        formData.append('name',name);

        formData.append('price',price);
        var board_id = boardSelect.val();
        formData.append('board_id',board_id);
        var situation = situationSelect.val();
        formData.append('situation',situation);
        var term = termSelect.val();
       // formData.append('term',term);
        var descpiption = descpiptionInput.val();

//console.log(file);

        // $.zlajax({
        zlajax.post({
            type:'post',
            url: '/aproduct_form/',
            dataType :'text',
            data:formData,
            processData: false,
            contentType: false,
            /*{
                'name': name,
                'price':price,
                'board_id': board_id,
                'situation':situation,
                'term':term,
                'description':descpiption,
                'file':file,
                // 'cache': false, //上传文件不需要缓存
                // 'processData': false, // 告诉jQuery不要去处理发送的数据
                // 'contentType': false,

            },*/
            'success': function (data) {
                console.log(data)
                if(data == "succcess"){ //传回来了 但是 参数对了 也没执
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
                            // alert("bbbbb")
                            window.location = '/';
                        },
                        'confirmCallback': function () {
                            // alert("aaaa");
                            window.location = '/aproduct/';
                        }
                    });
                    console.log('11111111111111')
                    // alert.alertInfo(data['message']);
                }
                // if(data['code'] == 200){ //传回来了 但是 参数对了 也没执
                //     alert.alertConfirm({
                //         'msg': 'congratulations! Successful product launch!',
                //         'cancelText': 'Back to Home',
                //         'confirmText': 'Upload again',
                //         'cancelCallback': function () {
                //             alert("bbbbb")
                //             window.location = '/';
                //         },
                //         'confirmCallback': function () {
                //             alert("aaaa");
                //             window.location = '/aproduct/';
                //         }
                //     });
                //     window.location = '/';
                // }else{
                //     console.log('11111111111111')
                //     alert.alertInfo(data['message']);
                // }
            },
            'error': function (err) {
                console.log(err)
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
