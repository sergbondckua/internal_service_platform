// Функція для форматування дати
function formatDate() {
    const dateInput = document.getElementById("id_date_contract");
    const formattedDate = document.getElementById("id_contract_number_suffix");

    if (dateInput.value) {
        const date = new Date(dateInput.value);
        const day = String(date.getDate()).padStart(2, '0');
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const year = String(date.getFullYear()).slice(2);
        formattedDate.textContent = `-${day}${month}${year}`;
    } else {
        formattedDate.textContent = "";
    }
}

// Викликаємо formatDate під час завантаження сторінки
window.onload = function () {
    formatDate();
};