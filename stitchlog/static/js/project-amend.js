// Create table row
function addNewRow(item = false) {
    const tbody = document.getElementById('project-floss-amend-body');
    const tr = document.createElement('tr');

    tr.innerHTML = `<td>
                        <select name="floss-brand" id="floss-brand">
                            <option value="DMC">DMC</option>
                            <option value="Anchor">Anchor</option>
                        </select>
                        <input type="text" class="flossRow" name="floss" autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false">
                    </td>
                    <td style="border-left: 2px solid transparent; width: 10px;"></td>
                    <td style="text-align:center; width:25px;">
                        <button class="icon-button" id="deleteRow">
                            <img src="/static/icons/delete.png" 
                                class="small-icon" />
                        </button>
                    </td>`;

    // If floss item
    if (item) {
        tr.querySelector('.flossRow').value = item;
    }

    // Deletes row
    tr.querySelector('#deleteRow').addEventListener('click', () => {
        tr.remove();
    });

    tbody.appendChild(tr);

    return tr
}

document.getElementById('amendAddStock').addEventListener('click', () => {
    addNewRow()
});

// Upload & extract floss
const fileInput = document.getElementById("uploadPattern");
const uploadBtn = document.getElementById("uploadPatternBtn");

uploadBtn.addEventListener("click", () => {
  fileInput.click();
});

fileInput.addEventListener('change', () => {
    if (fileInput.files.length > 0) {
        const file = uploadPattern.files[0];
        const formData = new FormData();
        formData.append('file', file);

    fetch(extract_floss_url, {
        method: "POST",
        body: formData,
    })
    .then(response => response.json())
    .then(result => {
        if (result.status == "ok") {
            result.data.forEach((item) => {
                addNewRow(item)
            })
        }
    }
    )
    .catch(error => {
      console.error('Upload error:', error);
      alert('Upload failed.');
    });
}});

// Cancel changes
document.getElementById('cancelChanges').addEventListener('click', () => {
    window.location.href = return_page_url;
});

// Save changes
document.getElementById('saveChanges').addEventListener('click', () => {
    const newProjectName = document.getElementById('projectName').value;
    // const flossInputs = document.querySelectorAll('.flossRow');

    // const flossArray = [];
    // inputs.forEach(input => {
    //     flossArray.push(input.value);
    // });

    fetch(save_changes_url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
            prev_name: PROJECT_NAME,
            new_name: newProjectName,
            // floss: flossArray
        })
    })
    .then(response => response.json())
    .then(result => {
        if (result.status === "ok") {
            window.location.href = `${SCRIPT_ROOT}/projects/${newProjectName}`;
        } else {
            alert(result.message || "Error: unsaved changes!");
        }
    })
});

// Set default project name input
window.onload = document.getElementById("projectName").value = PROJECT_NAME;