import dotenv from 'dotenv';

dotenv.config();

export const config = {
  port: parseInt(process.env.PORT || '3000', 10), // Default to 3000 if not set
  jwtSecret: process.env.JWT_SECRET,
  pythonMlServiceUrl: process.env.PYTHON_ML_SERVICE_URL || 'http://localhost:8000/predict',
};

if (!config.jwtSecret) {
  throw new Error('JWT_SECRET environment variable is required');
}
