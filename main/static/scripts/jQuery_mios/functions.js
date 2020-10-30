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

        window.print();
        $("*").removeClass("hide-to-print");

    });
});