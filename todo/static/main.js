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


$('.checkbox').change(function() {
   let id = $(this).attr('id');

   if (this.checked) {
     $(this).parent().next().css("text-decoration", "line-through");
     $.ajax({
            url: '/todo/update',
            type: 'POST',
            data: {id: id, done: 1}
     });
   } else {
     $(this).parent().next().css("text-decoration", "none");
     $.ajax({
            url: '/todo/update',
            type: 'POST',
            data: {id: id, done: 0}
     });

   }
 });
