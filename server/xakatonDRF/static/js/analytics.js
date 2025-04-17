fetch("static/data/data.json")
  .then((response) => response.json())
  .then((data) => {
    // Гистограмма прогнозов завершения операций
    const barChartForecast = {
      data: [],
      layout: {
        title: "Прогноз завершения операций (дни)",
        xaxis: { title: "Операция", tickangle: 45, tickfont: { size: 12 } },
        yaxis: { title: "Оставшиеся дни", gridcolor: "#eee" },
        margin: { t: 40, b: 100, l: 50, r: 20 },
        plot_bgcolor: "#f9f9f9",
        paper_bgcolor: "#ffffff",
        font: { family: "Roboto", size: 14, color: "#333" },
        transition: { duration: 500 },
        barmode: "group",
        bargap: 0, // Расстояние между группами столбцов
        bargroupgap: 0, // Расстояние между столбцами внутри группы
      },
    };

    data.forEach((d, index) => {
      barChartForecast.data.push({
        x: [d.Операция],
        y: [d["Прогноз (дней)"]],
        type: "bar",
        name: `Операция ${index + 1}`,
        marker: {
          color: ["#4CAF50", "#FFC107", "#2196F3", "#E91E63", "#9C27B0"][
            index % 5
          ],
          line: { width: 0.5, color: "#388E3C" },
        },
        text: d.Подразделение,
        textposition: "auto",
        hoverinfo: "x+y+text",
        width: 0.07,
      });
    });

    Plotly.newPlot(
      "bar-chart-forecast",
      barChartForecast.data,
      barChartForecast.layout
    );

    // Сводка для прогнозов завершения операций
    const summaryForecast = document.getElementById("summary-forecast");
    summaryForecast.innerHTML = `
          <h2>Сводка данных</h2>
          <p><strong>Общее количество операций:</strong> ${data.length}</p>
          <p><strong>Основные операции:</strong> ${[
            ...new Set(data.map((d) => d.Операция)),
          ].join(", ")}</p>
          <p><strong>Прогноз завершения операций:</strong></p>
          <ul>
            ${data
              .map((d) => `<li>${d.Операция}: ${d["Прогноз (дней)"]} дней</li>`)
              .join("")}
          </ul>
        `;

    // Диаграмма отстающих подразделений
    const laggingData = data.filter((d) => d["Прогноз (дней)"] > 10);
    const barChartLagging = {
      x: laggingData.map((d) => d.Подразделение),
      y: laggingData.map((d) => d["Прогноз (дней)"]),
      type: "bar",
      marker: {
        color: "#FF5722",
        line: { width: 1.5, color: "#D84315" },
      },
      text: laggingData.map((d) => d.Операция),
      textposition: "auto",
      hoverinfo: "x+y+text",
    };

    const layoutBarLagging = {
      title: "Отстающие подразделения",
      xaxis: {
        title: "Подразделение",
        tickangle: 45,
        tickfont: { size: 12 },
      },
      yaxis: { title: "Оставшиеся дни", gridcolor: "#eee" },
      margin: { t: 40, b: 100, l: 50, r: 20 },
      plot_bgcolor: "#f9f9f9",
      paper_bgcolor: "#ffffff",
      font: { family: "Roboto", size: 14, color: "#333" },
      transition: { duration: 500 },
    };

    Plotly.newPlot("bar-chart-lagging", [barChartLagging], layoutBarLagging);

    // Сводка для отстающих подразделений
    const summaryLagging = document.getElementById("summary-lagging");
    summaryLagging.innerHTML = `
          <h2>Сводка данных</h2>
          <p><strong>Отстающие подразделения:</strong></p>
          <ul>
            ${laggingData
              .map(
                (d) =>
                  `<li>${d.Подразделение}: ${d["Прогноз (дней)"]} дней (${d.Операция})</li>`
              )
              .join("")}
          </ul>
        `;

    // Круговая диаграмма распределения операций
    const operationCounts = {};
    data.forEach((d) => {
      operationCounts[d.Операция] = (operationCounts[d.Операция] || 0) + 1;
    });

    const pieChartOperations = {
      labels: Object.keys(operationCounts),
      values: Object.values(operationCounts),
      type: "pie",
      marker: { colors: ["#FFC107", "#2196F3", "#E91E63", "#9C27B0"] },
      textinfo: "percent",
      textposition: "inside",
      hoverinfo: "label+percent",
    };

    const layoutPieOperations = {
      title: "Распределение операций",
      margin: { t: 40, b: 40, l: 40, r: 40 },
      plot_bgcolor: "#f9f9f9",
      paper_bgcolor: "#ffffff",
      font: { family: "Roboto", size: 14, color: "#333" },
      transition: { duration: 500 },
    };

    Plotly.newPlot(
      "pie-chart-operations",
      [pieChartOperations],
      layoutPieOperations
    );

    // Сводка для распределения операций
    const summaryOperations = document.getElementById("summary-operations");
    summaryOperations.innerHTML = `
          <h2>Сводка данных</h2>
          <p><strong>Распределение операций:</strong></p>
          <ul>
            ${Object.entries(operationCounts)
              .map(([op, count]) => `<li>${op}: ${count} раз</li>`)
              .join("")}
          </ul>
        `;

    // Обработчик изменения размера окна
    window.addEventListener("resize", () => {
      Plotly.relayout("bar-chart-forecast", {
        width: window.innerWidth * 0.7,
      });
      Plotly.relayout("bar-chart-lagging", {
        width: window.innerWidth * 0.7,
      });
      Plotly.relayout("pie-chart-operations", {
        width: window.innerWidth * 0.7,
      });
    });
  })
  .catch((error) => {
    console.error("Ошибка:", error);
    alert(
      "Не удалось загрузить данные. Проверьте консоль для подробной информации."
    );
  });
