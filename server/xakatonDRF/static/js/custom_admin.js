
(function ($) {
    $(document).ready(function () {
        var newLink = $('<li><a href="/admin/custom-menu/">Новая Менюшка</a></li>');
        $('.side-menu').append(newLink);
    });
})(django.jQuery);