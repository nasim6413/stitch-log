// Create table row
function addNewRow(item = false) {
    const tbody = document.getElementById('project-floss-amend-body');
    const tr = document.createElement('tr');

    tr.innerHTML = `<td>
                        <input type="text" id="flossRow" name="floss" autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false">
                    </td>
                    <td style="text-align:center; width:20px;">
                        <button class="icon-button" id="deleteRow">
                            <img src="/static/icons/delete.png" 
                                class="small-icon" />
                        </button>
                    </td>`;

    // If floss item
    if (item) {
        tr.querySelector('#flossRow').value = item;
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

// Add extracted floss
document.getElementById('uploadPattern').addEventListener('click', () => {
    const fileInput = document.getElementById('patternFile');
    const file = fileInput.files[0];
    if (!file) {
        alert("Please select a file first.");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

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
});

// Cancel changes
document.getElementById('cancelChanges').addEventListener('click', () => {
    window.location.href = cancel_changes_url;
});

// Save changes
// document.getElementById('saveChanges').addEventListener('click', () => {
// });
