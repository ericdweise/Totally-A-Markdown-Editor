$(document).ready(function(){
    // Edit Button
    $('#edit').click(function() {
        $('#edit-menu').removeClass('hidden');
        $('#editor').removeClass('hidden');
        $('#view-menu').addClass('hidden');
        $('#viewer').addClass('hidden');

        var mdfile = window.location.pathname.replace(/\.html$/, '.md');
        console.log("Loading Markdown: " + mdfile);
        $.get("index.md", function (data) {
            $("#editor").html(data);
        });
    });

    // Save Button
    $('#save').click(function() {
        $('#edit-menu').addClass('hidden');
        $('#editor').addClass('hidden');
        $('#view-menu').removeClass('hidden');
        $('#viewer').removeClass('hidden');
    });

    // Abort Button
    $('#abort').click(function() {
        $('#edit-menu').addClass('hidden');
        $('#editor').addClass('hidden');
        $('#view-menu').removeClass('hidden');
        $('#viewer').removeClass('hidden');
    });
})
