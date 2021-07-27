'use strict';

$(function () {
    $("td[colspan=3]").find("p").hide();
    $("table").click(function (event) {
        event.stopPropagation();
        var $target = $(event.target);
        if ($target.closest("td").attr("colspan") > 1) {
            $target.slideUp();
        } else {
            $target.closest("tr").next().find("p").slideToggle();
        }
    });
});

$(document).click('change', '.checkbox', function () {
    let id;
    if ($(this).attr('checked')) {
        $(this).removeAttr('checked');

        id = $(this).val();

        $.ajax({
            url: '/todo/update',
            type: 'POST',
            data: {id: id, done: 0}
        });

    } else {
        $(this).attr('checked', 'checked');
        id = $(this).val();

        $.ajax({
            url: '/todo/update',
            type: 'POST',
            data: {id: id, done: 1}
        });
    }
    $(this).parent().toggleClass('completed');
    localStorage.setItem('listItems', $('#list-items').html());
});


