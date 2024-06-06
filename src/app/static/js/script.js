$(document).ready(function() {
    console.log("Document ready");
    
    $('#btn1kai').click(function() {
        console.log("一回ボタンがクリックされました");
        $('#form1').show();
        $('#form2').hide();
        $('#form3').hide();
    });

    $('#btnOfuku').click(function() {
        console.log("往復ボタンがクリックされました");
        $('#form1').hide();
        $('#form2').show();
        $('#form3').hide();
    });

    $('#btnTeiki').click(function() {
        console.log("定期ボタンがクリックされました");
        $('#form1').hide();
        $('#form2').hide();
        $('#form3').show();
    });
});
