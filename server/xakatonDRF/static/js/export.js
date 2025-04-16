// Функции для работы с модальным окном
function showExportModal() {
    document.getElementById('exportModal').style.display = 'block';
}

function hideExportModal() {
    document.getElementById('exportModal').style.display = 'none';
}

// Закрытие при клике вне модального окна
window.onclick = function(event) {
    const modal = document.getElementById('exportModal');
    if (event.target == modal) {
        hideExportModal();
    }
}

// Функция для получения данных таблицы
function getTableData() {
    const table = document.querySelector('.custom-table');
    const headers = Array.from(table.querySelectorAll('th')).map(th => th.textContent.trim());
    const rows = Array.from(table.querySelectorAll('tbody tr'));
    
    return {
        headers: headers,
        data: rows.map(row => {
            const inputs = row.querySelectorAll('input');
            return headers.reduce((obj, header, i) => {
                obj[header] = inputs[i]?.value || '';
                return obj;
            }, {});
        })
    };
}

// Экспорт в Excel
function exportToExcel() {
    const { headers, data } = getTableData();
    const ws = XLSX.utils.json_to_sheet(data, { header: headers });
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, "Данные");
    XLSX.writeFile(wb, 'сельхоз_данные.xlsx');
    hideExportModal();
}

// Экспорт в Word
function exportToWord() {
    const { headers, data } = getTableData();
    const { Document, Paragraph, Table, TableRow, TableCell, HeadingLevel } = docx;
    
    // Создаем строки таблицы для Word
    const wordRows = [
        new TableRow({
            children: headers.map(header => 
                new TableCell({
                    children: [new Paragraph(header)],
                    shading: {
                        fill: "DDDDDD"
                    }
                })
            )
        }),
        ...data.map(row => 
            new TableRow({
                children: headers.map(header => 
                    new TableCell({
                        children: [new Paragraph(row[header] || '')]
                    })
                )
            })
        )
    ];
    
    // Создаем документ Word
    const doc = new Document({
        sections: [{
            children: [
                new Paragraph({
                    text: "Сельскохозяйственные данные",
                    heading: HeadingLevel.HEADING_1
                }),
                new Table({
                    rows: wordRows,
                    width: {
                        size: 100,
                        type: "PERCENTAGE"
                    }
                })
            ]
        }]
    });
    
    // Генерируем и скачиваем файл
    docx.Packer.toBlob(doc).then(blob => {
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = 'сельхоз_данные.docx';
        link.click();
        URL.revokeObjectURL(url);
        hideExportModal();
    });
}