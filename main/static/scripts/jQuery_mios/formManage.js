$(document).ready(function() {

    $('#add_form').click(function() {
        var form_idx = $('#id_form-TOTAL_FORMS').val();
        $('#form_set').append('<td class="text-center w3-border">' + $('#empty_form').html().replace(/__prefix__/g, form_idx) + '</td>');
        $('#id_form-TOTAL_FORMS').val(parseInt(form_idx) + 1);
    });

});