async function printJSON() {
  const response = await fetch('stock-symbols.json');
  json = await response.json();

  const stocksInfo = document.querySelector('.stock-info');
  json.forEach((s) => {
    const stockElem = document.createElement('div');
    const stockName = document.createElement('div');
    const stockSymbol = document.createElement('div');
    stockElem.classList.add('stock-info__cell');
    stockName.classList.add('stock-info__cell__name');
    stockSymbol.classList.add('stock-info__cell__symbol');
    stockName.textContent = s.name;
    stockSymbol.textContent = s.symbol;
    stockElem.appendChild(stockName);
    stockElem.appendChild(stockSymbol);
    stocksInfo.appendChild(stockElem);
  });
}

async function printTable() {
  const response = await fetch('portfolio.json');
  console.log(response);
  json = await response.json();

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

printJSON();
printTable();
