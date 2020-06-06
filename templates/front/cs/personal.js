
$scope.newFile =function(){
    		 $scope.showdiv();

    	};
 $scope.showdiv=function(){
		  $('#my_dialog').dialog({
			  modal:true,
			  width:"400",
	    	  height:"223"
		  	});
		  document.getElementById("my_dialog").style.display="block";
	  };
$scope.create_paper_cancel=function(){
		 console.info("取消");
   	     $("#create_name").val("");
		 $("#create_author").val("");
		 $("#create_type").empty();
		 var ops={
					"总结报告":"总结报告",
					"辅助授课":"辅助授课",
					"其他":"其他"
				};
		 var parent=document.getElementById("create_type");
		 for(var key in ops)
		 {
			 var o = new Option(ops[key],key);
	         parent.appendChild(o);

		 }
   	     $('#my_dialog').dialog("close");
	};
