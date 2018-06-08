function successAlert(){
	$(".myAlert-top-success").show();
	setTimeout(function(){
		$(".myAlert-top-success").hide(); 
	}, 3000);
}
function errorAlert(){
	$(".myAlert-top-error").show();
	setTimeout(function(){
	    $(".myAlert-top-error").hide(); 
	}, 3000);
}
$(document).ready(function(){
	$(".statusEditButton").on('click',function(){
		var but = $(this);
		var id = $(this).attr('data-id');
		/* console.log(id); */				
		/* if (confirm('Are you sure you want to change status?')) { */
			
	        $.ajax({
	            url: '/statuschange',
	            type: "POST",
	            data: {
	                "tid":id
	            },
	            success: function (response) {
	            	successAlert();
	                /* console.log(but); */
	                if(but.html() == "Mark As Undone"){
	                	but.html("Mark As done");
	                	$("#"+id+'cardheader').css("background-color","#d29034");
	                	$("#"+id+'cardheader').parent("div").parent('div').removeClass('done');
	                	$("#"+id+'cardheader').parent("div").parent('div').addClass('notdone');
	                }else{
	                	but.html("Mark As Undone");
		                /* alert("#"+id+'cardheader'); */
		                $("#"+id+'cardheader').css("background-color","#61bd4f");
		                $("#"+id+'cardheader').parent("div").parent('div').removeClass('notdone');
	                	$("#"+id+'cardheader').parent("div").parent('div').addClass('done');
	                }
	                
	                
	            },
	            error: function (response) {
	            	errorAlert();
	            }
	        });
	    /* } */
	});
    $('#hidebutton').click(function () {
    	/* console.log($(this).html()); */
        if ($(this).html() == 'Hide Marked Done') {
            /* console.log("Hidden"); */
            $(".done").css('visibility', 'hidden');
            $(".done").css('display', 'none');
        } else {
          
        	$(".done").css('visibility', 'visible');
            $(".done").css('display', 'block');
          
          
          
           /* console.log("Not Hidden"); */
        }
        $(this).html($(this).html() == 'Show Marked Done' ? 'Hide Marked Done' : 'Show Marked Done')
    });
});