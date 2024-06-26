const express = require('express');
const mysql = require('mysql');

const app = express();

// Create a MySQL connection
const connection = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: 'daim123',
  database: 'mydatabase'
});

// Connect to MySQL
connection.connect((err) => {
  if (err) {
    console.error('Error connecting to MySQL: ' + err.stack);
    return;
  }
  console.log('Connected to MySQL as id ' + connection.threadId);
});

// Set up a route to fetch data from the database and display it
app.get('/', (req, res) => {
  connection.query('SELECT * FROM transactions', (err, rows) => {
    if (err) {
      console.error('Error executing MySQL query: ' + err.stack);
      res.status(500).send('Internal Server Error');
      return;
    }

    // Check if rows is not null or undefined
    if (!rows || rows.length === 0) {
      console.error('No rows returned from MySQL query');
      res.status(500).send('Internal Server Error');
      return;
    }

    let tableHtml = '<table><tr><th>Transaction ID</th><th>Customer ID</th><th>Amount</th><th>Transaction Date</th><th>Payment Method</th></tr>';
    rows.forEach(row => {
      tableHtml += `<tr><td>${row.transaction_id}</td><td>${row.customer_id}</td><td>${row.amount}</td><td>${row.transaction_date}</td><td>${row.payment_method}</td></tr>`;
    });
    tableHtml += '</table>';

    res.send(`
      <!DOCTYPE html>
      <html lang="en">
      <head>
        <meta charset="UTF-8">
        <title>Transaction Information</title>
        <style>
          table {
            border-collapse: collapse;
            width: 100%;
          }
          th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
          }
          th {
            background-color: #f2f2f2;
          }
        </style>
      </head>
      <body>
        <h2>Transaction Information</h2>
        ${tableHtml}
      </body>
      </html>
    `);
  });
});

// Start the server
const PORT = 4000;
app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
