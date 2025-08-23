// Load stock list
function loadStock() {
    fetch(list_url)
        .then(response => response.json())
        .then(data => {
            const tbody = document.getElementById('stock-table-body');
            tbody.innerHTML = ''; // clear table
            data.forEach(item => {
                const tr = document.createElement('tr');
                tr.innerHTML = `<td>${item.brand}</td>
                                <td>${item.fno}</td>`;
                tbody.appendChild(tr);
            });
        });
}

// Send floss to stock
function sendStock(action) {
    // Retrieve input
    const floss = document.getElementById('floss').value;

    // Generates URL
    let url 
    
    if (action == 'add') {
        url = add_url
    } else if (action == 'delete') {
        url = delete_url
    };

    // Accesses API depending on URL used
    fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ floss: floss })
        })
    .then(response => response.json())
    .then(result => {
        if (result.status === "ok") {
            document.getElementById('floss').value = ''; // clear input
            loadStock(); // refresh table
        } else {
            alert(result.message || "Error");
        }
    })
    .then(() => loadStock());
}

// Button function calls
document.getElementById('button_add').addEventListener('click', () => sendStock('add'));
document.getElementById('button_delete').addEventListener('click', () => sendStock('delete'));

// Loads stock on page render
window.onload = loadStock;