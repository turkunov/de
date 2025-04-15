import express from 'express';
import path from 'path';
import { fileURLToPath } from 'url';
import { verifyToken } from './middlewares/auth.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const port = process.env.PORT || 3000;

// Serve static files from client
app.use('/build', express.static(path.join(__dirname, '../../client/build')));
app.use(express.static(path.join(__dirname, '../../client/public')));

// API routes
app.get('/api/protected', verifyToken, (req, res) => {
  res.json({ message: 'Token is valid!' });
});

// All other routes to Svelte app
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, '../../client/index.html'));
});


app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});