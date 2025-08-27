// Delete project
document.getElementById('button_delete_project').addEventListener('click', () => {
    if (confirm(`Are you sure you want to delete project ${PROJECT_NAME}?`) === true) {
        fetch(delete_project_url,
            { 
                method : "POST"
            }
        )
        .then(response => response.json())
        .then(result => {
            if (result.status === "ok") {
                window.location.href = `${SCRIPT_ROOT}/projects`;
            } else {
                alert(result.message || "Error!")
            }
        })
    }
});