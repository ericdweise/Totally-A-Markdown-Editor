$(document).ready(function(){
    // Edit Button
    $('#edit').click(function() {
        $('#edit-menu').removeClass('hidden');
        $('#editor').removeClass('hidden');
        $('#view-menu').addClass('hidden');
        $('#viewer').addClass('hidden');

        var mdfile = window.location.pathname.replace(/\.html$/, '.md');
        console.log("Loading Markdown: " + mdfile);
        $.get(mdfile, function (data) {
            $("#editor").html(data);
        });
    });

    // Save Button
    $('#save').click(function() {
        // Save editor content
        var mdfile = window.location.pathname.replace(/\.html$/, '.md');
        var form = new FormData();
        var data = $('#editor').text();
        console.log(data);
        form.append("data", data); // $('#editor').text().replace(/\n/g, '<br>'));
        form.append("target", mdfile);
        var xhr = (window.XMLHttpRequest) ? new XMLHttpRequest() : new activeXObject("Microsoft.XMLHTTP");
        xhr.open( 'post', '/htbin/save.py', true );
        xhr.overrideMimeType('text/x-python');
        xhr.send(form);

        // reload page
    });

    // Abort Button
    $('#abort').click(function() {
        $('#edit-menu').addClass('hidden');
        $('#editor').addClass('hidden');
        $('#view-menu').removeClass('hidden');
        $('#viewer').removeClass('hidden');
    });
})
