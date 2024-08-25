$(document).ready(function() {
    $('.reserveBtn').click(function() {
        var id = $(this).data('id');
        console.log(id);
        // window.location.href = '/reserveInfo?id=' + id; // これを削除して $.get に変更
        $.get('/staffReserveInfo', { id: id }, function(response) {
            window.location.href = '/staffReserveInfo?id=' + id;
        });
    });
});
