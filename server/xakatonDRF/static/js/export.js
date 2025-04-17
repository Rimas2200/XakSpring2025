document.addEventListener('DOMContentLoaded', () => {
    const exportBtn = document.getElementById('exportBtn');
    const exportModal = document.getElementById('exportModal');
    const closeModal = document.getElementById('closeModal');
    const wordExportBtn = document.getElementById('wordExportBtn');
    const excelExportBtn = document.getElementById('excelExportBtn');

    // Открываем модальное окно при клике на кнопку "Выгрузить"
    exportBtn.addEventListener('click', () => {
        console.log('Кнопка "Выгрузить" нажата');
        exportModal.style.display = 'block';
    });

    // Закрываем модальное окно при клике на крестик
    closeModal.addEventListener('click', () => {
        console.log('Модальное окно закрыто');
        exportModal.style.display = 'none';
    });

    // Обработка выбора формата экспорта
    wordExportBtn.addEventListener('click', () => {
        console.log('Выбран экспорт в Word');
        exportToWord();
        exportModal.style.display = 'none';
    });

    excelExportBtn.addEventListener('click', () => {
        console.log('Выбран экспорт в Excel');
        exportToExcel();
        exportModal.style.display = 'none';
    });

    // Функция экспорта в Word
    function exportToWord() {
        const table = document.querySelector('.custom-table');
        const rows = Array.from(table.querySelectorAll('tr'));

        // Создаем массив данных
        const data = [];
        rows.forEach(row => {
            const cells = Array.from(row.querySelectorAll('td'));
            const rowData = cells.map(cell => cell.querySelector('input').value);
            data.push(rowData);
        });

        // Создаем документ Word
        const doc = new Document();
        const tableRows = data.map(row => new TableRow(...row.map(cell => new TableCell(cell))));
        doc.addSection({ children: [new Table(tableRows)] });

        // Сохраняем файл
        Packer.toBlob(doc).then(blob => {
            saveAs(blob, 'data.docx');
        });
    }

    // Функция экспорта в Excel
    function exportToExcel() {
        const table = document.querySelector('.custom-table');
        const rows = Array.from(table.querySelectorAll('tr'));

        // Создаем массив данных
        const data = [['Дата', 'Подразделение', 'Операция', 'Культура', 'За день, га', 'С начала операции, га', 'Вал за день, ц', 'Вал с начала, ц']];
        rows.forEach(row => {
            const cells = Array.from(row.querySelectorAll('td'));
            const rowData = cells.map(cell => cell.querySelector('input')?.value || '');
            if (rowData.some(value => value)) { // Добавляем только строки с данными
                data.push(rowData);
            }
        });

        // Создаем объект Workbook
        const workbook = XLSX.utils.book_new();
        const worksheet = XLSX.utils.aoa_to_sheet(data);
        XLSX.utils.book_append_sheet(workbook, worksheet, 'Sheet1');

        // Сохраняем файл
        XLSX.writeFile(workbook, 'data.xlsx');
    }
});