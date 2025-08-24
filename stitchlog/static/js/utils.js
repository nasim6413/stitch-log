// Display message
export function showErrorMessage(msg) {
    const msgDiv = document.getElementById('error-message');
    msgDiv.style.textAlign = "center";
    msgDiv.style.text
    msgDiv.style.color = "red";
    msgDiv.style.marginBottom = "5px";
    msgDiv.textContent = msg;
}

export function clearMessage() {
    const msgDiv = document.getElementById('error-message');
    msgDiv.textContent = '';
}