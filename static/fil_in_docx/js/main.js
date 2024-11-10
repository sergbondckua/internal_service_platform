// Функція для форматування дати
function formatDate() {
    const dateInput = document.getElementById("id_date_contract");
    const formattedDate = document.getElementById("id_contract_number_suffix");

    if (dateInput.value) {
        const date = new Date(dateInput.value);
        const day = String(date.getDate()).padStart(2, '0');
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const year = String(date.getFullYear()).slice(2);
        formattedDate.textContent = `${day}${month}${year}`;
    } else {
        formattedDate.textContent = "";
    }
}

// Викликаємо formatDate під час завантаження сторінки
window.onload = function () {
    formatDate();
};

function formatFileSize(bytes) {
    if (bytes < 1024) return `${bytes} Б`;
    if (bytes < 1048576) return `${(bytes / 1024).toFixed(1)} КБ`;
    return `${(bytes / 1048576).toFixed(1)} МБ`;
}

function checkTaskStatus(taskId, attempt = 1, maxAttempts = 10) {
    fetch(`/contract/check-task-status?task_id=${taskId}`)
        .then(response => response.json())
        .then(data => {
            if (data.status === "completed") {
                // Відображення посилань на файли
                const linksContainer = document.getElementById("file-links");
                linksContainer.innerHTML = "";  // Очистити контейнер

                const listGroup = document.createElement("div");
                listGroup.classList.add("list-group", "list-group-flush", "mb-4");

                // Маппінг імен файлів
                const fileNames = {
                    "filled_contract_url": "Договір",
                    "filled_pax_akt_url": "Рахунок. Акт виконаних робіт",
                    "filled_add_agreement_url": "Додаткова угода"
                };

                for (const [key, fileData] of Object.entries(data.files)) {
                    const listItem = document.createElement("a");
                    listItem.href = fileData.url;
                    listItem.classList.add("list-group-item", "list-group-item-action", "d-flex", "justify-content-between", "align-items-center");

                    const spanText = document.createElement("span");
                    const displayName = fileNames[key.toLowerCase()] || key.replace("_", " ").toUpperCase();
                    const fileName = fileData.name || key.replace("_", " ").toUpperCase();
                    const fileSize = formatFileSize(fileData.size);

                    // Відображення файлу з іконкою та розміром
                    spanText.innerHTML = `
                          <i class="bi bi-file-earmark-word-fill me-2 text-primary"></i>
                          <strong>${displayName}</strong>`;
                    listItem.appendChild(spanText);

                    // Додано кнопку "Завантажити" з іконкою
                    const spanBadge = document.createElement("span");
                    spanBadge.classList.add("badge", "bg-light", "rounded-pill");
                    spanBadge.innerHTML = `<i class="text-primary bi bi-download"></i> <small class="text-muted"><i class="bi bi-filetype-docx"></i> ${fileName} (${fileSize})</small>`;
                    listItem.appendChild(spanBadge);

                    listGroup.appendChild(listItem);
                }

                linksContainer.appendChild(listGroup);
            } else if (attempt < maxAttempts) {
                // Якщо завдання ще не завершене, повторюємо запит
                setTimeout(() => checkTaskStatus(taskId, attempt + 1, maxAttempts), 2000);
            } else {
                // Показуємо повідомлення після досягнення максимальної кількості спроб
                const linksContainer = document.getElementById("file-links");
                linksContainer.innerHTML = "<p class='text-danger'>Завдання не завершене. Будь ласка, поверніться до форми й почніть спочатку.</p>";
            }
        })
        .catch(error => {
            console.error('Error fetching task status:', error);
        });
}


