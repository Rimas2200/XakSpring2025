document.addEventListener("DOMContentLoaded", function () {
  const menuToggle = document.getElementById("menuToggle");
  const sidebar = document.getElementById("sidebar");

  menuToggle.addEventListener("click", function () {
    sidebar.classList.toggle("hidden");

    // Меняем иконку
    const icon = this.querySelector("i");
    if (sidebar.classList.contains("hidden")) {
      icon.classList.replace("fa-bars", "fa-arrow-right");
    } else {
      icon.classList.replace("fa-arrow-right", "fa-bars");
    }
  });
});

document.addEventListener("DOMContentLoaded", () => {
  const exportBtn = document.getElementById("exportBtn");
  const exportModal = document.getElementById("exportModal");
  const closeModal = document.getElementById("closeModal");
  const wordExportBtn = document.getElementById("wordExportBtn");
  const excelExportBtn = document.getElementById("excelExportBtn");
  const clearBtn = document.getElementById("clearBtn"); // Кнопка "Очистить"
  const addRowBtn = document.getElementById("addRowBtn"); // Кнопка "Добавить строку"

  // Проверяем, что все элементы найдены
  if (
    !exportBtn ||
    !exportModal ||
    !closeModal ||
    !wordExportBtn ||
    !excelExportBtn ||
    !clearBtn ||
    !addRowBtn
  ) {
    console.error("Один или несколько элементов не найдены в DOM.");
    return;
  }

  // Открываем модальное окно при клике на кнопку "Выгрузить"
  exportBtn.addEventListener("click", () => {
    console.log('Кнопка "Выгрузить" нажата');
    exportModal.style.display = "block";
  });

  // Закрываем модальное окно при клике на крестик
  closeModal.addEventListener("click", () => {
    console.log("Модальное окно закрыто");
    exportModal.style.display = "none";
  });

  // Обработка выбора формата экспорта
  wordExportBtn.addEventListener("click", () => {
    console.log("Выбран экспорт в Word");
    exportToWord();
    exportModal.style.display = "none";
  });

  excelExportBtn.addEventListener("click", () => {
    console.log("Выбран экспорт в Excel");
    exportToExcel();
    exportModal.style.display = "none";
  });

  // Очистка всех полей ввода в таблице
  clearBtn.addEventListener("click", () => {
    console.log('Кнопка "Очистить" нажата');
    const inputs = document.querySelectorAll(".custom-table input"); // Находим все <input> в таблице
    inputs.forEach((input) => {
      input.value = ""; // Устанавливаем значение в пустую строку
    });
  });

  // Добавление новой строки в таблицу
  if (
    !exportBtn ||
    !exportModal ||
    !closeModal ||
    !wordExportBtn ||
    !excelExportBtn ||
    !clearBtn ||
    !addRowBtn
  ) {
    console.error("Один или несколько элементов не найдены в DOM.");
    return;
  }

  // Добавление новой строки в таблицу

  addRowBtn.addEventListener("click", () => {
    console.log("Добавлена новая строка");
    const tableBody = document.querySelector(".custom-table tbody");

    // Получаем <thead>
    const tableHead = document.querySelector(".custom-table thead");
    if (!tableHead) {
      console.error("Ошибка: <thead> не найден в таблице.");
      return;
    }

    // Получаем <tr> внутри <thead>
    const headerRow = tableHead.querySelector("tr");
    if (!headerRow) {
      console.error("Ошибка: <tr> не найден в <thead>.");
      return;
    }

    // Получаем количество столбцов из <thead>
    const columnsCount = headerRow.querySelectorAll("th").length;
    console.log("Количество столбцов:", columnsCount);
    if (columnsCount === 0) {
      console.error(
        "Ошибка: Нет столбцов в <thead>. Убедитесь, что <thead> содержит <th>"
      );
      return;
    }

    // Создаем новую строку
    const newRow = document.createElement("tr");

    // Создаем ячейки для новой строки
    for (let i = 0; i < columnsCount; i++) {
      const newCell = document.createElement("td");
      const newInput = document.createElement("input");
      newInput.type = "text";
      newInput.className = "table-input"; // Применяем класс для стилей
      newCell.appendChild(newInput);
      newRow.appendChild(newCell);
    }

    // Добавляем новую строку в таблицу
    tableBody.appendChild(newRow);

    // Устанавливаем фокус на первое поле ввода
    const firstInput = newRow.querySelector("input");
    if (firstInput) {
      firstInput.focus();
    }

    // Проверяем, что строка добавлена
    console.log("Текущее количество строк:", tableBody.children.length);
  });
  document.addEventListener('click', (event) => {
    if (event.target.classList.contains('delete-row-btn')) {
        const row = event.target.closest('tr');
        if (row) {
            row.remove();
        }
    }
  });
  document.addEventListener("keydown", (event) => {
    const currentInput = document.activeElement; // Текущее активное поле ввода
    if (!currentInput || !currentInput.classList.contains("table-input")) {
      return; // Выходим, если фокус не на поле ввода таблицы
    }

    const currentCell = currentInput.parentElement; // Текущая ячейка
    const currentRow = currentCell.parentElement; // Текущая строка
    const table = currentRow.parentElement.parentElement; // Таблица

    let targetInput = null;

    switch (event.key) {
      case "ArrowUp": // Вверх
        const prevRow = currentRow.previousElementSibling;
        if (prevRow) {
          const index = Array.from(currentRow.children).indexOf(currentCell);
          targetInput = prevRow.children[index]?.querySelector(".table-input");
        }
        break;

      case "ArrowDown": // Вниз
        const nextRow = currentRow.nextElementSibling;
        if (nextRow) {
          const index = Array.from(currentRow.children).indexOf(currentCell);
          targetInput = nextRow.children[index]?.querySelector(".table-input");
        }
        break;

      case "ArrowLeft": // Влево
        const prevCell = currentCell.previousElementSibling;
        if (prevCell) {
          targetInput = prevCell.querySelector(".table-input");
        }
        break;

      case "ArrowRight": // Вправо
        const nextCell = currentCell.nextElementSibling;
        if (nextCell) {
          targetInput = nextCell.querySelector(".table-input");
        }
        break;

      default:
        return; // Игнорируем другие клавиши
    }

    if (targetInput) {
      event.preventDefault(); // Предотвращаем стандартное поведение
      targetInput.focus(); // Устанавливаем фокус на целевое поле
    }
  });

  // Функция экспорта в Word (текстовый файл .txt)
  function exportToWord() {
    const table = document.querySelector(".custom-table");
    const rows = Array.from(table.querySelectorAll("tr"));

    // Создаем массив данных
    const data = [];
    rows.forEach((row) => {
      const cells = Array.from(row.querySelectorAll("td"));
      const rowData = cells.map(
        (cell) => cell.querySelector("input")?.value || ""
      );
      data.push(rowData.join("\t")); // Разделяем ячейки табуляцией
    });

    // Создаем текстовый файл
    const textContent = data.join("\n"); // Разделяем строки переносом строки
    const blob = new Blob([textContent], { type: "text/plain" });
    saveAs(blob, "data.txt");
  }

  // Функция экспорта в Excel
  function exportToExcel() {
    const table = document.querySelector(".custom-table");
    const rows = Array.from(table.querySelectorAll("tr"));

    // Создаем массив данных
    const data = [
      [
        "Дата",
        "Подразделение",
        "Операция",
        "Культура",
        "За день, га",
        "С начала операции, га",
        "Вал за день, ц",
        "Вал с начала, ц",
      ],
    ];
    rows.forEach((row) => {
      const cells = Array.from(row.querySelectorAll("td"));
      const rowData = cells.map(
        (cell) => cell.querySelector("input")?.value || ""
      );
      if (rowData.some((value) => value)) {
        // Добавляем только строки с данными
        data.push(rowData);
      }
    });

    // Создаем объект Workbook
    const workbook = XLSX.utils.book_new();
    const worksheet = XLSX.utils.aoa_to_sheet(data);
    XLSX.utils.book_append_sheet(workbook, worksheet, "Sheet1");

    // Сохраняем файл
    XLSX.writeFile(workbook, "data.xlsx");
  }
});
