// open modal with value
$(function(){
    $(".completeTask").click(function(){
        $('.close_task_modal').show();
        // how to get data.id from the template?
        var task_to_close = $(this).task_id;
        $(".form-group-id #id_id").val(task_to_close);
    })
});

