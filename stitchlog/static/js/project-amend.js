// Create table row
function addNewRow(item = false) {
    const tbody = document.getElementById('project-floss-amend-body');
    const tr = document.createElement('tr');

    tr.innerHTML = `<td style="padding: 2px 5px;">
                        <div style="display:flex;">
                            <select name="floss-brand" class="floss-brand-select">
                                <option value="DMC">DMC</option>
                                <option value="Anchor">Anchor</option>
                            </select>
                            <input type="text" class="flossRow floss-input" name="floss" autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false">
                        </div>
                    </td>
                    <td style="border-left: 2px solid transparent; width: 10px; padding: 2px;"></td>
                    <td style="text-align:center; width:25px; padding: 2px;">
                        <button class="icon-button" id="deleteRow">
                            <img src="/static/icons/delete.png" class="small-icon" />
                        </button>
                    </td>`;

    // If floss item
    if (item) {
        tr.querySelector('.flossRow').value = item.floss;
        tr.querySelector('select[name="floss-brand"]').value = item.brand;
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
        const file = fileInput.files[0];
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
    })
    .finally(() => {
        fileInput.value = '';  // reset so change fires correctly next time
    });
}});

// Load stock list
function loadStock() {
    fetch(floss_list_url)
        .then(response => response.json())
        .then(result => {
            if (result.status === "ok") {

            result.data.forEach(item => {
                addNewRow(item);
            }); 
        }
    });
};

// Delete button
document.getElementById('deleteProject').addEventListener('click', () => {
    fetch(delete_project_url, 
        { method: "POST" })
        .then(response => response.json())
        .then(result => {
            if (result.status === "ok") {
                window.location.href = `${SCRIPT_ROOT}/projects`;
            } else {
                alert(result.message || "Error!");
            }
        });
});

// Cancel changes
document.getElementById('cancelChanges').addEventListener('click', () => {
    window.location.href = return_page_url;
});

// Save changes
document.getElementById('saveChanges').addEventListener('click', () => {
    const newProjectName = document.getElementById('projectName').value;
    const projectStartDate = document.getElementById('startDate').value;
    const projectEndDate = document.getElementById('endDate').value;

    // Collect each row's brand + floss number together
    const flossArray = [];
    const rows = document.querySelectorAll('#project-floss-amend-body tr');
    rows.forEach(row => {
        const brand = row.querySelector('select[name="floss-brand"]').value;
        const floss = row.querySelector('.flossRow').value;
        if (floss) {  // skip empty rows
            flossArray.push({ brand, floss });
        }
    });

    fetch(save_changes_url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
            project_id: PROJECT_ID,
            project_name: newProjectName,
            project_start_date: projectStartDate,
            project_end_date: projectEndDate,
            floss: flossArray
        })
    })
    .then(response => response.json())
    .then(result => {
        if (result.status === "ok") {
            window.location.href = `${SCRIPT_ROOT}/projects/${PROJECT_ID}`;
        } else {
            alert(result.message || "Error: unsaved changes!");
        }
    })
});

// Set default project name input
window.onload = () => {
    loadStock();
    document.getElementById("projectName").value = PROJECT_NAME;
};