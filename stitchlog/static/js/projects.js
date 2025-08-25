// Load projects list
function loadProjects () {
    fetch(projects_list_url)
    .then(response => response.json())
    .then(data => {
        const tbody = document.getElementById('projects-table-body');

        // Clearing previous pages
        tbody.innerHTML = '';

        data.forEach(item => {
            const tr = document.createElement('tr');
            tr.innerHTML = `<td><a href="/projects/${item.project_name}/" id="project-page">
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
})

// // Create new project
// function createProject () {
//     fetch()
// }