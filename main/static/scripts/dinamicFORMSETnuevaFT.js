$(function() {
    $('.add-row').on('click', function() {
        return addForm($(this).attr("to"), $(this).siblings('.dynamic-fformset').children().children('.dynamic-formset')); //here is children.children because of the table body
    });

    $('.dynamic-fformset').on('click', '.delete-row', function() {
        return deleteForm(this, $(this).attr("from"));
    })
    $('.new-product').on('click', function() {
        $('#AddProductModalForm').show();
    });

    const addProductForm = $('#AddProductModalForm').children().children('#modalForm');
    addProductForm.on('submit', function(e) {
        e.preventDefault();
        $.post("/nuevo_product", addProductForm.serialize(), function(data, status) {
            $('#AddProductModalForm').hide();
            $(data).insertAfter('body');
            setTimeout(() => { location.reload() }, 2000);
        });
    });
})