import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import { config } from './config';
import apiRoutes from './routes';

const app = express();

// Security middleware
app.use(helmet());
app.use(cors());

// Body parsing middleware
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));

// API routes
app.use('/api', apiRoutes);

// Health check endpoint
app.get('/health', (req: express.Request, res: express.Response) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// Error handling middleware
app.use((err: any, req: express.Request, res: express.Response, next: express.NextFunction) => {
  console.error('Unhandled error:', err);
  res.status(500).json({ error: 'Internal server error' });
});

// Start server
const PORT = config.port;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
