document.addEventListener('DOMContentLoaded', function () {
    console.log("Таблица загружена");

    // Пример: Добавьте здесь логику для работы с таблицей
    const clearButton = document.querySelector('.btn-danger');
    clearButton.addEventListener('click', function () {
        const inputs = document.querySelectorAll('.table-input');
        inputs.forEach(input => input.value = '');
    });
});