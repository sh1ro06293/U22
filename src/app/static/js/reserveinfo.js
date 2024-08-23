function submitRemove() {
    // URLのidの部分を/submit_removeにPOSTする
    // URLのクエリから取得
    var url = location.search;
    // ?id=以降の部分を取得
    var id = url.split('?id=')[1];
    var apiUrl = '/submit_remove';
    var data = {
        'id': id
    };
    // POSTで送信
    $.post(apiUrl, data, function(response){
        // 成功時にリダイレクト
        window.location.href = response.redirect_url;
    }).fail(function() {
        alert('エラーが発生しました。');
    });
}
