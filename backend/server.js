const express = require('express');
const path = require('path');
const { exec } = require('child_process');

const app = express();
const port = 3000;

// Serve static files from the 'public' directory
app.use(express.static(path.join(__dirname, '../public')));
app.get('/', (req, res) => {
  res.send('Hello, Meta Agent with More Agents!');
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});


app.get('/run-python', (req, res) => {
  exec('python ../app.py', (error, stdout, stderr) => {
    if (error) {
      res.status(500).send(`Error: ${error.message}`);
      return;
    }
    if (stderr) {
      res.status(500).send(`Stderr: ${stderr}`);
      return;
    }
    res.send(`Stdout: ${stdout}`);
  });
});