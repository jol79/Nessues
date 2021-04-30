// open modal with value
$(function(){
    $(".completeTask").click(function(){
        $('.close_task_modal').show();
        // how to get data.id from the template?
        var id = $(this).data('id');
        $(".form-group-id #id_id").val(id);
    })
});

