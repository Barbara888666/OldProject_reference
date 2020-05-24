$(document).ready(function () {
    $(".menu_main>a").click(function () {
        var Node=$(this).next("ul");
        Node.toggle(500);
    })

})