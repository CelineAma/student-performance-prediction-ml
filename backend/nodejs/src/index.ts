import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import { config } from './config';
import apiRoutes from './routes';

const app = express();

app.use(helmet());
app.use(cors());

app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));

app.use('/api', apiRoutes);

app.get('/health', (req: express.Request, res: express.Response) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

app.use((err: any, req: express.Request, res: express.Response, next: express.NextFunction) => {
  console.error('Unhandled error:', err);
  res.status(500).json({ error: 'Internal server error' });
});

const PORT = config.port;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
