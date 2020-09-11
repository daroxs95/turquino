class addFormsetFilled {
    constructor() {
        this.buttonAddFF = null;
    }

    setbuttonAddFF(el) {
        this.buttonAddFF = el;
    }
    sendAjaxRequest_and_UpdatePage() {
        var el = this.buttonAddFF;
        $.post("getProduccionFormset", {
                csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").attr("value"), //revisar si es mejor hacer .val(), y si no trae problemas de seguridad enviarlo asi
                producto: $("#id_producto_name").val(),
                cantidad: $("#id_cantidad").val()
            },
            function(data, status) {
                $('#PredefinedAmountModalForm').hide();
                return addFormset(el, $(el).attr("to"), 'pickPFormset', data, false);
            });
    }
}
var Instance_addFormsetFilled = new addFormsetFilled;

$(function() {
    $('.dynamic-fformset').on('click', '.add-row', function() {
        return addForm($(this).attr("to"), $(this).parents('.dynamic-formset'));
    });

    $('.dynamic-fformset').on('click', '.delete-row', function() {
        return deleteForm(this, $(this).attr("from"));
    })

    $('.add-formset').on('click', function() {
        return addFormset(this, $(this).attr("to"), 'pickPFormset');
    });

    $('.add-formset-filled').on('click', function() {
        $('#PredefinedAmountModalForm').show();
        return Instance_addFormsetFilled.setbuttonAddFF(this);
    });

    $("#PredefinedAmountModalForm_FORM").submit(function(e) {
        e.preventDefault();
        return Instance_addFormsetFilled.sendAjaxRequest_and_UpdatePage();
    });

    $('.dynamic-fformset').on('click', '.delete-formset', function() {
        return deleteFormset(this, $(this).attr("from"), 'pickPFormset');
    })
})