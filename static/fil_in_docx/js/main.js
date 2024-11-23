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

// Функція для керування відображенням суфікса
function toggleSuffix() {
    const suffixElement = document.getElementById("id_contract_number_suffix");
    const isSuffixChecked = document.getElementById("id_is_suffix_number").checked;

    suffixElement.style.display = isSuffixChecked ? 'inline' : 'none';
}

// Функція для форматування дати// Виклик функції при завантаженні сторінки та на зміну поля is_suffix_number
document.getElementById("id_is_suffix_number").addEventListener("change", toggleSuffix);
document.getElementById("id_date_contract").addEventListener("input", formatDate);

// Функція для форматування розміру
function formatFileSize(bytes) {
    if (bytes < 1024) return `${bytes} Б`;
    if (bytes < 1048576) return `${(bytes / 1024).toFixed(1)} КБ`;
    return `${(bytes / 1048576).toFixed(1)} МБ`;
}

// Функція для перевірки статусу завдання
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

document.addEventListener("DOMContentLoaded", function () {
    const legalFormSelect = document.querySelector("select[name='legal_form']");
    const fullNameInput = document.querySelector("input[name='full_name']");
    const shortNameCheckbox = document.querySelector("input[name='is_short_name']");

    const shortNameContainer = document.createElement("div");
    shortNameContainer.id = "short-name-display";
    shortNameContainer.classList.add("mt-2", "text-muted");

    const checkboxParent = shortNameCheckbox.closest(".form-check");
    checkboxParent.appendChild(shortNameContainer);

    function updateShortName() {
        if (shortNameCheckbox.checked) {
            const legalForm = legalFormSelect.options[legalFormSelect.selectedIndex]?.text.trim() || "";
            const fullName = fullNameInput.value.trim();
            if (legalForm && fullName) {
                shortNameContainer.textContent = `${legalForm} "${fullName.toUpperCase()}"`;
            } else {
                shortNameContainer.textContent = "Оберіть юридичну форму та заповніть повне найменування.";
            }
        } else {
            shortNameContainer.textContent = "";
        }
    }

    legalFormSelect.addEventListener("change", updateShortName);
    fullNameInput.addEventListener("input", updateShortName);
    shortNameCheckbox.addEventListener("change", updateShortName);

    updateShortName();
});

// Автозаповнення назви вулиці
$(document).ready(function () {
    // Додаємо autocomplete до поля street_name
    $("#id_street_name").autocomplete({
        source: function (request, response) {
            // Перевіряємо значення поля "city"
            const selectedCity = $("#id_city").val(); // Отримуємо значення з поля city
            if (selectedCity === "Черкаси") { // Перевіряємо, чи вибрано "Черкаси"
                $.ajax({
                    url: "/api/v1/streets/", // Відносний шлях до API
                    method: "GET",
                    dataType: "json",
                    success: function (data) {
                        // Фільтруємо дані за полями `name` та `old_name`
                        const filtered = data.filter(item =>
                            item.name.toLowerCase().includes(request.term.toLowerCase()) ||
                            item.old_name.toLowerCase().includes(request.term.toLowerCase())
                        );

                        // Форматуємо дані для автозаповнення
                        response(filtered.map(item => ({
                            label: `${item.prefix} ${item.name} ${item.old_name ? `(раніше: ${item.old_prefix} ${item.old_name})` : ''}`,
                            value: item.name // Тільки `name` буде вставлено в поле
                        })));
                    },
                    error: function () {
                        console.error("Не вдалося отримати дані з API.");
                    }
                });
            } else {
                response([]); // Якщо місто не "Черкаси", автозаповнення не працює
            }
        },
        minLength: 2, // Кількість символів для початку пошуку
        delay: 300 // Затримка перед виконанням запиту (мс)
    });

    // Якщо значення поля city змінюється, очищаємо поле street_name
    $("#id_city").on("change", function () {
        const selectedCity = $(this).val();
        if (selectedCity !== "Черкаси") {
            $("#id_street_name").val(""); // Очищаємо поле street_name
        }
    });
});
