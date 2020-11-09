$(document).ready(function() {


    $(function() {
        $(".datepicker").datepicker({
            changeMonth: true,
            changeYear: true,
            dateFormat: 'yy-mm-dd'
        });
    });

    $(".tooltip").tooltip({
        show: { duration: 50 },
        hide: { duration: 50 },
        content: function() {
            tooltips = $(this).children(".tooltiptext");
            if (tooltips.length != 0) return $(this).children(".tooltiptext").html();
            else return null;
        },
        items: ".tooltip"
    });

    $(document).tooltip({
        show: { duration: 50 },
        hide: { duration: 50 },
    });

    $(".print-btn").on('click', () => {
        let table_data = $(".table-data")
        $("*").addClass("hide-to-print");
        $(".printable-model").parents().removeClass("hide-to-print");
        $(".printable-model").find("*").removeClass("hide-to-print");
        $(".printable-model").removeClass("hide-to-print");
        table_data.removeClass("w3-responsive");

        window.print();

        $("*").removeClass("hide-to-print");
        $(".table-data").addClass("w3-responsive");


    });

    $(".print-btn-sliced").on('click', () => {
        let table_data = $(".table-data")
        $("*").addClass("hide-to-print");
        $(".printable-model").parents().removeClass("hide-to-print");
        $(".printable-model").find("*").removeClass("hide-to-print");
        $(".printable-model").removeClass("hide-to-print");
        table_data.removeClass("w3-responsive");

        let original_table = table_data.find("table");
        let slice1 = original_table.clone(true).css("page-break-after", "always").insertAfter(table_data.find("table:last"));
        let slice2 = original_table.clone(true).insertAfter(table_data.find("table:last"));

        $(original_table).hide();

        let total_columns = $(original_table).find("tr:first").children("th").length;
        let half_columns = Math.ceil(total_columns / 2);

        $(slice2).find("tr").each((index, row) => {
            for (let i = 0; i < half_columns; i++) {
                $(row).children("td:first").remove();
                $(row).children("th:first").remove();
            }
        });
        $(slice1).find("tr").each((index, row) => {
            for (let i = 0; i < total_columns - half_columns; i++) {
                $(row).children("td:last").remove();
                $(row).children("th:last").remove();
            }
        });


        window.print();

        $(original_table).show();
        $(slice2).remove();
        $(slice1).remove();

        $("*").removeClass("hide-to-print");
        table_data.addClass("w3-responsive");

    });

    $(".save-finals").on('click', () => {
        document.body.style.cursor = 'wait';
        let finals = []
        let date = $(".model-title").attr('hasta');
        $(".table-data tbody").children('tr').each((index, element) => {
            let product = $(element).children('td:first').html();
            if (product != "Totales") {
                finals.push({ name: product, price: parseFloat($(element).children('td').eq(1).html()), amount: parseFloat($(element).children('td').eq(-2).html()), value: parseFloat($(element).children('td').eq(-1).html()) })
            }
        });
        let data = { finals: finals, date: date };
        let dataJSON = JSON.stringify(data);
        $.post("/save_finals", {
            //dataType: 'json',
            //contentType: "application/json",
            csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").attr("value"), //revisar si es mejor hacer .val(), y si no trae problemas de seguridad enviarlo asi
            dataJSON,
        }, function(data, status) {
            document.body.style.cursor = 'default';
            $(data).insertAfter('body');
        });
    });
});