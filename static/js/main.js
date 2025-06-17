window.onload(updateLength());

function updateLength() {
    var range = document.getElementById("vid-length");
    var label = document.getElementById("length-label");
    var value = range.value;
    label.innerHTML = value;
}

function generateVidRequest(event) {
    event.preventDefault();
    
    var subject_field = document.getElementById('vid-subject');
    var range = document.getElementById("vid-length");
    var generate_button = document.getElementById('gen-button');
    var subtitle_check = document.getElementById('sub-check');
    var subtitle_check_lbl = document.getElementById('sub-check-label');
    var size_select = document.getElementById('size-select');

    var subject = subject_field.value;
    var length = range.value;
    var size = size_select.value;
    var optgroup = size_select.options[size_select.selectedIndex].parentElement;
    console.log(optgroup.label);
    
    // Disabling all the options while the video is being generated
    subject_field.setAttribute("disabled", "");
    range.setAttribute("disabled", "");
    generate_button.setAttribute("disabled", "");
    subtitle_check.setAttribute("disabled", "");
    subtitle_check_lbl.setAttribute("disabled", "");
    size_select.setAttribute("disabled", "");

    var container = document.getElementById("container-vid");
    var html_container = "<div class='loader'></div>"
    container.innerHTML = html_container;

    fetch('/generating-vid', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ vid_subject: subject, vid_length: length, sub_check: subtitle_check.checked, size: size, proportion: optgroup.label})

    })
    .then(response => response.json())
    .then(data => {
        showVid(data.vid, data.proportion);
        // Re-enabling the options
        subject_field.removeAttribute("disabled");
        range.removeAttribute("disabled");
        generate_button.removeAttribute("disabled");
        subtitle_check.removeAttribute("disabled");
        subtitle_check_lbl.removeAttribute("disabled");
        size_select.removeAttribute("disabled");
    })
    .catch(error => {
        console.error('Error:', error);
        window.location.replace("/error");
    });
}

function replaceJinja(texto, variaveis)
{
    return texto.replace(/\{\{\s*(\w+)\s*\}\}/g, (match, variavel) => {
        return variaveis[variavel] || match;
    });
}

function showVid(vid_path, proportion) {
    var container = document.getElementById("container-vid");
    if (vid_path != "ERROR") {
        switch (proportion) {
            case "16:9":
                var html_container = "<video width='640' height='360' controls><source src='{{ v }}' type='video/mp4'></video>";
                break;
            case "9:16":
                var html_container = "<video width='360' height='640' controls><source src='{{ v }}' type='video/mp4'></video>";
                break;
            // Used switch in case more proportions are added
        }
        var vid_replace = {v: vid_path}
        html_container = replaceJinja(html_container, vid_replace);
    }
    else {
        var html_container = "<p class='text-danger' style='margin-top:1vh'>An error occured. You may not have tokens for the AI model. Try again later!</p>"
    }
    container.innerHTML = html_container;
}

