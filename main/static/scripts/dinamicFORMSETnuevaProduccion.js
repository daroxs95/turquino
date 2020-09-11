$(function() {
    $('.add-row').on('click', function() {
        return addForm($(this).attr("to"), $(this).siblings('.dynamic-fformset').children().children('.dynamic-formset')); //here is children.children becouse of the table body
    });

    $('.dynamic-fformset').on('click', '.delete-row', function() {
        return deleteForm(this, $(this).attr("from"));
    })

})