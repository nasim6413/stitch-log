import { showErrorMessage, clearMessage } from './utils.js';

// Create table row
function addFlossRow(tbody, item, green = false) {
    const tr = document.createElement('tr');
    tr.innerHTML = `<td>${item.brand}</td>
                    <td>${item.fno}</td>
                    <td style="text-align:center; width:20px;">
                        <button class="icon-button" id="button-delete">
                            <img src="/static/icons/delete.png" 
                                class="small-icon" />
                            </button>
                    </td>`;

    tr.setAttribute('data-brand', `${item.brand}`)
    tr.setAttribute('data-fno', `${item.fno}`)

    // Newly added rows
    if (green === true) {
    tr.setAttribute('style', 'background-color:palegreen');
    }

    // Attach event handler directly inside the loop
    tr.querySelector('#button-delete').addEventListener('click', () => {
        deleteStock(tr);
    });

    tbody.appendChild(tr);

    return tr
}

// Load stock list
function loadStock() {
    fetch(list_url)
        .then(response => response.json())
        .then(result => {
            if (result.status === "ok") {

            const tbody = document.getElementById('stock-table-body');
            const msgDiv = document.getElementById('error-message');

            // Clearing previous pages
            tbody.innerHTML = '';
            msgDiv.textContent = '';

            result.data.forEach(item => addFlossRow(tbody, item))

            } else {
            alert(result.message || "Error!")
        }
    });
};

// Delete stock    
function deleteStock(tr) {
    const floss_brand = tr.getAttribute('data-brand');
    const floss_fno = tr.getAttribute('data-fno');

    fetch(delete_url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ 
        brand: floss_brand,
        fno : floss_fno
     })
    })
    .then(response => response.json())
    .then(result => {
        if (result.status == "ok") {
            tr.remove();
        } else if (result.status == "error") {
            showErrorMessage(result.message);
        } else {
            alert(result.message || "Error!");
        }
    });
};

// Add stock
document.getElementById('button-add').addEventListener('click', () => {
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
                const tr = addFlossRow(tbody, result.data, true)

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

// Loads stock on page render
window.onload = loadStock;