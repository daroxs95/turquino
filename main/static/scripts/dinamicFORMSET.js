function updateElementIndex(el, prefix, ndx) {
    var id_regex = new RegExp('(' + prefix + '-\\d+)');
    var replacement = prefix + '-' + ndx;

    if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
    if (el.id) el.id = el.id.replace(id_regex, replacement);
    if (el.name) el.name = el.name.replace(id_regex, replacement);
    if ($(el).attr("to")) $(el).attr("to", $(el).attr("to").replace(id_regex, replacement));
    if ($(el).attr("from")) $(el).attr("from", $(el).attr("from").replace(id_regex, replacement));

}

function addForm(prefix, addto, blank_it = true) { //prefix for updating managementform values and stuff, and addto is the object to add
    var formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
    var row = addto.children('.dynamic-form:first').clone(true).get(0);


    //$(row).removeAttr('id').insertAfter($(addto.children('.dynamic-form:last'))).children('.hidden').removeClass('hidden');
    $(row).insertAfter($(addto.children('.dynamic-form:last'))).children('.hidden').removeClass('hidden');

    updateElementIndex(row, prefix, formCount);
    $(row).children().each(function() {
        updateElementIndex(this, prefix, formCount);
        if (blank_it) $(this).val('');
    });
    $(row).children().not(':last').find("*").each(function() {
        updateElementIndex(this, prefix, formCount);
        if (blank_it) $(this).val('');
    });

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
            $(forms.get(i)).children().not(':last').children().each(function() { //averiguar para q esta en not last aqui
                updateElementIndex(this, prefix, i);
            });
        }
    }

    return false;
}

function addFormset(btn, prefix, extra_prefixes, formset, blank_it = true) {
    var formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMSETS').val());
    var fformset = $(btn).siblings('.dynamic-fformset');

    if (!formset) {
        formset = fformset.find('.dynamic-formset:first').clone(true).get(0); //no se por q estaba aqui el get 0, pero sin muchas pruebas sin el tambien funciona, UPDT: parece q get 0 coje solo el objeto html, y no el objeto jquery
    }

    //$(formset).removeAttr('id').insertAfter($(fformset.find('.dynamic-formset:last'))).children('.hidden').removeClass('hidden');
    $(formset).insertAfter($(fformset.find('.dynamic-formset:last'))).children('.hidden').removeClass('hidden');


    formset = fformset.find('.dynamic-formset:last').get(0); //esto esta aqui para poder actualizar todos los indices bien
    updateElementIndex(formset, prefix, formCount);
    $(formset).find("*").each(function() {
        updateElementIndex(this, prefix, formCount);
        if (blank_it) $(this).val(''); //lo quite porq no se para q se usaba y me daba problemas cuando se copiaba el management form
    });

    $('#id_' + prefix + '-TOTAL_FORMSETS').val(formCount + 1);

    extra_prefixes = extra_prefixes.split(" ");
    for (var i = 0, prefixesCount = extra_prefixes.length; i < prefixesCount; i++) {
        $('#id_' + extra_prefixes[i] + '-TOTAL_FORMS').val(formCount + 1);

        $(formset).find("*").each(function() {
            updateElementIndex(this, extra_prefixes[i], formCount);
            if (blank_it) $(this).val(''); //lo quite porq no se para q se usaba y me daba problemas cuando se copiaba el management form
        });
    }
    return false;
}

function deleteFormset(btn, prefix, extra_prefixes) { //parece funcionar mas pruebas requeridas
    extra_prefixes = extra_prefixes.split(" ")
    var parentFormset = $(btn).parents('.dynamic-formset');
    var formsetCount = parseInt($('#id_' + prefix + '-TOTAL_FORMSETS').val());

    //if (parentFormset.attr("id") != prefix + '-0-formset') { //aqui meti las pezunnas no es el mismo code del snippet
    if (formsetCount != 1) { //aqui meti las pezunnas no es el mismo code del snippet
        var formsets = parentFormset.siblings('.dynamic-formset');
        parentFormset.remove();

        $('#id_' + prefix + '-TOTAL_FORMSETS').val(formsets.length);

        extra_prefixes.forEach((extra_prefix) => {
            $('#id_' + extra_prefix + '-TOTAL_FORMS').val(formsets.length);
            formsets.each((index, element) => {
                $(element).each(function() {
                    updateElementIndex(this, extra_prefix, index); //no se si para los formsets tenga q actualizar algo pero ahora mismo esto no funciona, y no es necesario para los forms
                });
                $(element).find("*").each(function() {
                    updateElementIndex(this, extra_prefix, index); //no se si para los formsets tenga q actualizar algo pero ahora mismo esto no funciona, y no es necesario para los forms
                });
            });
        });

        formsets.each((index, element) => {
            //alert(formsets.get(i)).children().not(':last').children());
            $(element).each(function() {
                updateElementIndex(this, prefix, index); //no se si para los formsets tenga q actualizar algo pero ahora mismo esto no funciona, y no es necesario para los forms
            });
            $(element).find("*").each(function() {
                updateElementIndex(this, prefix, index); //no se si para los formsets tenga q actualizar algo pero ahora mismo esto no funciona, y no es necesario para los forms
            });
        });
    };

    return false;
}