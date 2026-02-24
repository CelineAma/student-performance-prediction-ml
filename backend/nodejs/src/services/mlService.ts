import axios, { AxiosError } from 'axios';
import { config } from '../config';
import { PredictionRequest, PredictionResponse } from '../types';

export class MLServiceError extends Error {
  constructor(
    message: string,
    public statusCode?: number,
    public originalError?: unknown
  ) {
    super(message);
    this.name = 'MLServiceError';
  }
}

export const predictRisk = async (request: PredictionRequest): Promise<PredictionResponse> => {
  try {
    const response = await axios.post<PredictionResponse>(
      config.pythonMlServiceUrl,
      request,
      {
        headers: { 'Content-Type': 'application/json' },
        timeout: 15000, // 15 seconds timeout
      }
    );
    return response.data;
  } catch (error: unknown) {
    if (error instanceof AxiosError) {
      const status = error.response?.status;
      const message = (error.response?.data as any)?.message || error.message;
      throw new MLServiceError(
        `ML service error: ${message}`,
        status,
        error
      );
    }
    throw new MLServiceError('Unexpected error communicating with ML service', 500, error);
  }
};
