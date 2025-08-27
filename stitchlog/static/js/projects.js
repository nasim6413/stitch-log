// import { showErrorMessage } from "./utils";

// Load projects list
function loadProjects () {
    fetch(projects_list_url)
    .then(response => response.json())
    .then(result => {
        const tbody = document.getElementById('projects-table-body');

        // Clearing previous pages
        tbody.innerHTML = '';
        console.log(result.data)
        result.data.forEach(item => {
            const tr = document.createElement('tr');
            tr.innerHTML = `<td><a href="${SCRIPT_ROOT}/projects/${item.project_name}" id="project-page">
                                ${item.project_name}
                            </td>
                            <td>
                            <div class="progress-cell">
                            <div class="progress-bar" style="width: ${item.project_progress}">
                                ${item.project_progress}%
                            </div>
                            </div></td>`;
            tbody.appendChild(tr);
    })
})};

// Create new project
document.getElementById('button-new').addEventListener('click', () => {
    fetch(create_project_url,
        { method: "POST" }
    )
    .then(response => response.json())
    .then(result => {
        if (result.status === "ok") {
            window.location.href = `${SCRIPT_ROOT}/projects/${result.data.project_name}`;
        } else {
            alert(result.message || "Error!" )
        }
    })
});

// Loads project list on page render
window.onload = loadProjects;