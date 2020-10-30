$(function() {
    $('.add-row').on('click', function() {
        return addForm($(this).attr("to"), $(this).siblings('.dynamic-fformset').children().children('.dynamic-formset'), false); //here is children.children because of the table body
    });

    $('.dynamic-fformset').on('click', '.delete-row', function() {
        return deleteForm(this, $(this).attr("from"));
    })

})