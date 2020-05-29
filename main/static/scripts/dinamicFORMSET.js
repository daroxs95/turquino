function updateElementIndex(el, prefix, ndx) {
    var id_regex = new RegExp('(' + prefix + '-\\d+)');
    var replacement = prefix + '-' + ndx;

    if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
    if (el.id) el.id = el.id.replace(id_regex, replacement);
    if (el.name) el.name = el.name.replace(id_regex, replacement);
}

function addForm(btn, prefix) {
    var formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
    var parentFormset = $(btn).parents('.dynamic-formset');
    var row = parentFormset.children('.dynamic-form:first').clone(true).get(0);


    $(row).removeAttr('id').insertAfter($(parentFormset.children('.dynamic-form:last'))).children('.hidden').removeClass('hidden');
    $(row).children().not(':last').children().each(function() {
        updateElementIndex(this, prefix, formCount);
        $(this).val('');
    });

    /*
    $(row).find('.delete-row').click(function() {
        deleteForm(this, prefix);
    });
    */

    $('#id_' + prefix + '-TOTAL_FORMS').val(formCount + 1);
    return false;
}

function deleteForm(btn, prefix) {
    if ($(btn).parents('.dynamic-form').attr("id") != prefix + '-0-row') { //aqui meti las pezunnas no es el mismo code del snippet
        var parentFormset = $(btn).parents('.dynamic-formset');
        $(btn).parents('.dynamic-form').remove();

        var forms = parentFormset.children('.dynamic-form');
        $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);

        for (var i = 0, formCount = forms.length; i < formCount; i++) {
            $(forms.get(i)).children().not(':last').children().each(function() {
                updateElementIndex(this, prefix, i);
            });
        }
    }

    return false;
}

$(function() {
    $('.add-row').click(function() {
        return addForm(this, $(this).attr("to"));
    });

    $('.delete-row').click(function() {
        return deleteForm(this, $(this).attr("from"));
    })
})