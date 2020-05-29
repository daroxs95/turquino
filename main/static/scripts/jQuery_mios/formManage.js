$(document).ready(function() {

    $('#add_form').click(function() {
        var form_idx = $('#id_form-TOTAL_FORMS').val();
        $('#form_set').append('<td class="text-center w3-border">' + $('#empty_form').html().replace(/__prefix__/g, form_idx) + '</td>');
        $('#id_form-TOTAL_FORMS').val(parseInt(form_idx) + 1);
    });

    /*Esto va en el htaml
        <div id="empty_form" style="display:none">
        <td id="{{ form.prefix }}-row" class="text-center w3-border">
            <!--ne se por q en mi metodo de annadir al formset no se annade con el td este, tengo q annadirlo manualmente en el metodo js-->
            {{ valeformset.empty_form.as_p }}
            <button id="remove-{{ form.prefix }}-row" class="w3-btn w3-gray delete-row" type="button">Delete form</button>
        </td>
    </div>
    */

});