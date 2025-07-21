$.fn.loadSiteDir = function() {
	var xhr = new XMLHttpRequest();
	xhr.onreadystatechange = function() {
		if (xhr.readyState == XMLHttpRequest.DONE) {
			$("#directory").html(xhr.responseText);

			// Expand ToC to show current note
			let url = new URL(window.location.href);
			var note_name = url.searchParams.get('note');
			var note_fields = note_name.split("/");
			var toc_expand = document.getElementById('directory');

			for(var i = 0; i < note_fields.length - 1; i++) {
				// details = toc_expand.querySelectorAll('details');
				var search_elts = toc_expand.children;
				for (var j = 0; j < search_elts.length; j++) {
					if (search_elts[j].nodeName == 'DETAILS' && search_elts[j].querySelector('summary').innerHTML == note_fields[i]) {
						toc_expand = search_elts[j]
						toc_expand.setAttribute('open', '');
						break;
					}
				}
			}
			search_elts = toc_expand.children;
			for (j = 0; j < search_elts.length; j++) {
				if (search_elts[j].nodeName == 'P') {
					if (search_elts[j].querySelector('a').getAttribute('href') == 'view?note=' + note_name) {
						search_elts[j].style.fontWeight = "bold";
					}
				}
			}
		}
	}

	xhr.open( 'GET', '/site-directory', true);
	xhr.send();
};

$.fn.editNote = function() {
    let url = new URL(window.location.href);
    url.pathname = 'edit';
    window.location.replace(url.href);
};

$.fn.newNote = function() {
    // TODO: Add this to "on-click" of the "New Note" button

    // Prompt user for new file
    var note = prompt('Name of new note','');
    console.log('New note: ' + note);

    // Send AJAX, wait for response
    // TODO: Write the "new-note" POST endpoint
    var form = new FormData();
    form.append('note', note);
    form.append('field2', 'field2_data');

    var xhr = new XMLHttpRequest();
    xhr.onloadend = function() {
        if (xhr.status == 201) {
            // Open new note in Edit mode
            window.location.replace("/edit?note=" + note);
        } else {
            alert("Failed to create new note at " + note);
        }
    }

    // TODO: is this right?
    xhr.open('post', '/new-note', true);
    xhr.send(form);
};

$.fn.saveNote = function() {
	const url = new URL(window.location.href);
	var path = url.searchParams.get('note');

    let raw_data = document.getElementById("editor").value;

    var form = new FormData();
    form.append('note', path);
    form.append('raw', raw_data);

	var xhr = new XMLHttpRequest();
	xhr.onloadend = function() {
		if (xhr.status == 201) {
            let url = new URL(window.location.href);
            url.pathname = 'view';
            window.location.replace(url.href);
		} else {
            alert("Save was unsuccessful.");
        }
	}

    xhr.open('post', '/save', true);
    xhr.send(form);
};

$.fn.abortEdit = function() {
    let url = new URL(window.location.href);
    url.pathname = 'view';
    window.location.replace(url.href);
};

// Do when new page loads
$(document).ready(function() {
    if (document.location.pathname == '/view') {
        $.fn.loadSiteDir();
    }
})
