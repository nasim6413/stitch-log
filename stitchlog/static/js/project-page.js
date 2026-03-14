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

document.getElementById('amendProject').addEventListener('click', () => {
    window.location.href = `${SCRIPT_ROOT}/projects/${PROJECT_ID}/amend`;
});

// Load stock list
function loadStock() {
    fetch(floss_list_url)
        .then(response => response.json())
        .then(result => {
            if (result.status === "ok") {

            const tbody = document.getElementById('project-floss-body');

            // Clearing previous pages
            tbody.innerHTML = '';

            result.data.forEach(item => {
                const tr = document.createElement('tr');
                tr.innerHTML = `<td>${item.brand}</td>
                                <td>${item.floss}</td>
                                <td style="color: ${item.availability ? 'green' : 'red'}">${item.availability ? 'available' : 'not available'}</td>`;

                tbody.appendChild(tr);
            }); 
        }
    });
};

// Loads stock on page render
window.onload = () => {
    loadStock();
    document.getElementById("projectName").textContent = PROJECT_NAME;
};