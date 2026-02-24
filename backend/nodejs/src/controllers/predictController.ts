import { Request, Response } from 'express';
import { AuthenticatedRequest, PredictionRequest, PredictionResponse } from '../types';
import { predictRisk, MLServiceError } from '../services/mlService';

export const predict = async (req: AuthenticatedRequest, res: Response) => {
  try {
    const request: PredictionRequest = req.body;
    const result: PredictionResponse = await predictRisk(request);
    res.json(result);
  } catch (err: unknown) {
    if (err instanceof MLServiceError) {
      return res.status(err.statusCode || 500).json({ error: err.message });
    }
    console.error('Prediction error:', err);
    res.status(500).json({ error: 'Internal server error' });
  }
};
