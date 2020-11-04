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
        $("*").addClass("hide-to-print");
        $(".printable-model").parents().removeClass("hide-to-print");
        $(".printable-model").find("*").removeClass("hide-to-print");
        $(".printable-model").removeClass("hide-to-print");
        $(".table-data").removeClass("w3-responsive");

        let original_table = $(".table-data").find("table");
        let slice1 = original_table.clone(true).insertAfter($(".table-data").find("table:last"));
        let separator = $("br").css("page-break-after", "always").insertAfter($(".table-data").find("table:last"));
        let slice2 = original_table.clone(true).insertAfter($(".table-data").find("br:last"));
        $(original_table).hide();

        let total_columns = $(original_table).find("tr:first").children("th").length;
        console.log(total_columns);

        $(slice2).find("tr").each((index, row) => {
            for (let i = 0; i < 15; i++) {
                $(row).children("td:first").remove();
                $(row).children("th:first").remove();
            }
        });
        $(slice1).find("tr").each((index, row) => {
            for (let i = 0; i < 15; i++) {
                $(row).children("td:last").remove();
                $(row).children("th:last").remove();
            }
        });

        window.print();

        $(original_table).show();
        $(slice2).remove();
        $(slice1).remove();
        $(separator).remove();

        $("*").removeClass("hide-to-print");
        $(".table-data").addClass("w3-responsive");


    });
});