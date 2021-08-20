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
        var text = new FormData();
        text.append("data", $('#editor').text());
        text.append("file", mdfile);
        var xhr = (window.XMLHttpRequest) ? new XMLHttpRequest() : new activeXObject("Microsoft.XMLHTTP");
        xhr.open( 'post', '/assets/php/save.php', true );
        xhr.send(text);

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
