import { showErrorMessage, clearMessage } from './utils.js';

// Retrieve input & load table
function convertFloss() {
    clearMessage()
    const floss = document.getElementById('floss').value;

    // Fixes input data
    fetch(`${convert_url}/${floss}`)
    .then(response => response.json())
    .then(fixedData => {

        // Invalid data
        if (fixedData.status !== "ok") {
            showErrorMessage(fixedData.message);
            return;
        }
        
        // Converts floss with fixed input
        fetch(`${convert_url}/${fixedData.data.brand}-${fixedData.data.fno}`)
        .then(response => response.json())
        .then(result => {
            if (result.status === "ok") {
                const thead = document.getElementById('conversion-table-header');
                const tbody = document.getElementById('conversion-table-body');

                // Clears input & table
                document.getElementById('floss').value = '';
                thead.innerHTML = '';
                tbody.innerHTML = '';

                // Create header
                const tr = document.createElement('tr');
                tr.innerHTML = `<th>${result.data[0].brand}</th>
                                <th>${result.data[0].converted_brand}</th>
                                <th>Hex</th>
                                <th>Available</th>`;
                thead.appendChild(tr);         

                // Create table
                result.data.forEach(item => {
                    const tr = document.createElement('tr');
                    tr.innerHTML = `<td>${item.brand_fno}</td>
                                    <td>${item.converted_fno}</td>
                                    <td style="display: flex; align-items: center;">
                                        <span style="color: black; flex: 1;">#${item.hex}</span>
                                        <span style="width: 60px; height: 20px; margin-left: 10px; border: 1px solid #ccc; background-color: #${item.hex}"></span>
                                    </td>
                                    <td style="color: ${item.availability ? 'green' : 'red'}">${item.availability ? 'available' : 'not available'}</td>`;
                    tbody.appendChild(tr);
                    });
                } else {
                        showErrorMessage(result.message);
                    }
                });
            });
        }

document.getElementById('button_convert').addEventListener('click', () => convertFloss());