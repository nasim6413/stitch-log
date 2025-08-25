import { showErrorMessage, clearMessage } from './utils.js';

console.log("stock.js loaded")

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

            result.data.forEach(item => {
                const tr = document.createElement('tr');
                tr.innerHTML = `<td>${item.brand}</td>
                                <td>${item.fno}</td>
                                <td style="text-align:center; width:20px;">
                                    <button class="delete-button">
                                    <img src="/static/icons/delete.png" 
                                        class="delete-icon" />
                                        </button>
                                </td>`;

                tr.setAttribute('data-brand', `${item.brand}`)
                tr.setAttribute('data-fno', `${item.fno}`)

                // Attach event handler directly inside the loop
                const btn = tr.querySelector('.delete-button');
                btn.addEventListener('click', () => {
                    deleteStock(tr);
                });

                tbody.appendChild(tr);
            }); 
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
                tr.innerHTML = `<td>${result.data.brand}</td>
                                <td>${result.data.fno}</td>
                                <td style="text-align:center; width:20px;">
                                    <button class="delete-button">
                                    <img src="/static/icons/delete.png" 
                                        class="delete-icon" />
                                        </button>
                                </td>`;

                tr.setAttribute('data-brand', `${result.data.brand}`)
                tr.setAttribute('data-fno', `${result.data.fno}`)
                tr.setAttribute('style', 'background-color:palegreen');

                // Attach event handler directly inside the loop
                const btn = tr.querySelector('.delete-button');
                btn.addEventListener('click', () => {
                    deleteStock(tr);
                });

                tbody.appendChild(tr);

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