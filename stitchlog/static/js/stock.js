import { showErrorMessage, clearMessage } from './utils.js';

// Load stock list
function loadStock() {
    clearMessage()
    
    fetch(list_url)
        .then(response => response.json())
        .then(data => {
            const tbody = document.getElementById('stock-table-body');
            const msgDiv = document.getElementById('error-message');
            // Clearing previous pages
            tbody.innerHTML = '';
            msgDiv.textContent = '';

            data.forEach(item => {
                const tr = document.createElement('tr');
                tr.innerHTML = `<td>${item.brand}</td>
                                <td>${item.fno}</td>`;
                tr.setAttribute('data-floss', `${item.brand}-${item.fno}`)
                tbody.appendChild(tr);
            });
        });
}

// Add stock
document.getElementById('button_add').addEventListener('click', () => {
    // Retrieve input
    const floss = document.getElementById('floss').value;
    clearMessage()

    fetch(add_url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ floss: floss })
        })
        .then(response => response.json())
        .then(result => {
            if (result.status == "ok") {
                document.getElementById('floss').value = ''; // clear input

                const tbody = document.getElementById('stock-table-body');
                const tr = document.createElement('tr');
                tr.innerHTML = `<td>${result.brand}</td>
                                <td>${result.fno}</td>`;

                tr.setAttribute('data-floss', `${result.brand}-${result.fno}`);
                tr.setAttribute('style', 'background-color:palegreen');
                
                // Insert new floss at top of table
                if (tbody.firstChild) {
                    tbody.insertBefore(tr, tbody.firstChild);
                } else {
                    tbody.appendChild(tr);
                }

            } else if (result.status == "error") {
                showErrorMessage(result.message);
            } else {
                alert(result.message || "Error!");
            }
        });
});

// Delete stock
document.getElementById('button_delete').addEventListener('click', () => {
    // Retrieve input
    const floss = document.getElementById('floss').value;
    clearMessage()

    fetch(delete_url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ floss: floss })
    })
    .then(response => response.json())
    .then(result => {
        if (result.status == "ok") {
            document.getElementById('floss').value = ''; // clear input

            // Remove row with matching fno
            const tbody = document.getElementById('stock-table-body');
            const row = tbody.querySelector(`tr[data-floss="${result.brand}-${result.fno}"]`);
            if (row) row.remove();
        } else if (result.status == "error") {
            showErrorMessage(result.message);
        } else {
            alert(result.message || "Error!");
        }
    });
});

// Loads stock on page render
window.onload = loadStock;