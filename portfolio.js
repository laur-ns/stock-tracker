async function printTable() {
  const response = await fetch('portfolio.json');
  const json = await response.json();

  const table = document.querySelector('table');
  json.Stocks.forEach((s) => {
    const tableRow = document.createElement('tr');
    const name = document.createElement('td');
    const quantity = document.createElement('td');
    const price = document.createElement('td');
    const gainLoss = document.createElement('td');

    name.textContent = s.Name;
    quantity.textContent = s.Quantity;
    price.textContent = `${s.Price}`;
    gainLoss.textContent = `${s.GainLoss}%`;

    tableRow.append(name);
    tableRow.append(quantity);
    tableRow.append(price);
    tableRow.append(gainLoss);
    table.append(tableRow);
  });
}

printTable();
