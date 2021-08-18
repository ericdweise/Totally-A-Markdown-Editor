$(document).ready(function(){
    // Edit Button
    $('#edit').click(function() {
        $('#edit-menu').removeClass('hidden');
        $('#editor').removeClass('hidden');
        $('#view-menu').addClass('hidden');
        $('#viewer').addClass('hidden');
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

    // Create Directory Button
    // Create File Button
})
