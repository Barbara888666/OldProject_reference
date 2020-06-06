$(function () {
    $("#search-submit-btn").click(function (event) {
        event.preventDefault();

        var search_input = $("input[name='search-content']");
        var search = search_input.val();

        zlajax.post({
            'url': '/search/',
            'data': {
                'search': search
            },
            'success': function (data) {
                if (data['code'] == 200) {
                    window.location='/search/'+search;
                } else {
                    alert.alertInfo(data['message']);
                }
            }
        });

    });
});