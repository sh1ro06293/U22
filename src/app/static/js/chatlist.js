
$(document).ready(function () {
    $('.reserveBtn').click(function () {
        var id = $(this).data('id');
        console.log(id);
        // window.location.href = '/reserveInfo?id=' + id; // これを削除して $.get に変更
        $.get('/reserveInfo', { id: id }, function (response) {
            window.location.href = '/Userchat?id=' + id;
        });
    });
});
