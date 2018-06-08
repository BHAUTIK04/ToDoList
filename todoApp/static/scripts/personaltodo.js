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
			$(".editTaskButton").on('click',function(){
				var modal = document.getElementById('editModal');
				var but = document.getElementsByClassName("close")[0];
				var id = $(this).attr("data-id");
				console.log(id);
				console.log('#'+id+"card");
				console.log(document.getElementById(id+"card"));
				$.ajax({
					url: '/task/'+id,
		            type: "GET",
		            data: {
		                "tid":id
		            },
		            success: function (response) {
		            	resp = JSON.parse(response)	
			         	console.log(resp);
			         	$(".modal-body #title").val(resp["title"]);
			         	$(".modal-body #description").val(resp["description"]);
			         	$(".modal-body #tid").val(resp["tid"]);
		            }
				})
				modal.style.display = "block";
				but.onclick = function(){
					modal.style.display = "none";
				}
				$(".saveTask").on("click", function(){
					var title = $(".modal-body #title").val();
					var description = $(".modal-body #description").val();
					console.log($(".modal-body #title").val());
					console.log($(".modal-body #description").val());
					$.ajax({
						url: '/yourtodo',
			            type: "POST",
			            data: {
			                "title":title,
			                "description":description,
			                "tid": id
			            },
			            success: function (response) {
			            	
			            	console.log(response);
			            	resp = JSON.parse(response)
			            	if(resp["response"] == "done"){
			            		modal.style.display = "none";
			            		successAlert();
			            	}
			            	location.reload();
			            }
					})
				});
			});
			$(".statusEditButton").on('click',function(){
				var but = $(this);
				var id = $(this).attr('data-id');
				/* console.log(id); */				
				/* if (confirm('Are you sure you want to change status?')) { */
					
			        $.ajax({
			            url: '/statuschange',
			            type: "PUT",
			            data: JSON.stringify({"tid":id}),
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
			
			$(".deleteButton").on('click', function(){
				var tid = $(this).attr("data-id");
				console.log(tid);
				$.ajax({
					url:"/task/"+tid,
					method:"delete",
					success: function(response){
						console.log(response);
						location.reload();
					}
						
				});
			})
			
		});