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
        return addForm($(this).attr("to"), $(this).parents('.dynamic-formset'), false);
    });

    $('.dynamic-fformset').on('click', '.delete-row', function() {
        return deleteForm(this, $(this).attr("from"));
    })

    $('.add-formset').on('click', function() {
        return addFormset(this, $(this).attr("to"), 'pickPFormset', null, false); //actualmente blank it lo desactive, daba problemas con el management form, aparecia total forms con value no definido, por lo q deba error al guardar, habia q annadar i eliminar un form para q se actualizara
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
    });

    $('.calc-totals').on('click', function() {
        calcTotals($(this).attr("to"));
        $('.' + $(this).attr("to")).show();
    });
    $('form').on('change', function() {
        calcTotals('table-totals');
        $('.table-totals').show();
    });
})

const calcTotals = (to) => {
    let used = {};
    let used_verbose_name = {};

    let node_totals = $('.' + to).find('.col-total');
    let col = $(node_totals).clone(true).get(0);

    $("[id^='formsets-'][id$='-row']").each((index, element) => {
        let selected = $(element).find("option:selected");
        if (selected.val()) {
            used[selected.val()] = (used[selected.val()] || 0) + (parseFloat($(element).find("[id$='-cantidad']").val()) || 0);
            used_verbose_name[selected.val()] = $(element).find("option:selected").html();
        }
    });;
    for (key in used) {
        $(node_totals).remove();

        let newcol = $(col).clone(true);
        $(newcol).appendTo($('.' + to).find('.row-totals'));
        newcol.find('[id="Producto"]').html(used_verbose_name[key]);
        newcol.find('[id="cantidad"]').html(used[key]);
    };
}