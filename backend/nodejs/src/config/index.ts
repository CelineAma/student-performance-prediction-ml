import dotenv from 'dotenv';

dotenv.config();

export const config = {
  port: parseInt(process.env.PORT || '3000', 10), // Default to 3000 if not set
  jwtSecret: process.env.JWT_SECRET,
  pythonMlServiceUrl: process.env.PYTHON_ML_SERVICE_URL || 'http://localhost:8000/predict',
  adminUsername: process.env.ADMIN_USERNAME || 'admin',
  adminPasswordHash: process.env.ADMIN_PASSWORD_HASH,
};

if (!config.jwtSecret) {
  throw new Error('JWT_SECRET environment variable is required');
}

if (!config.adminPasswordHash) {
  throw new Error('ADMIN_PASSWORD_HASH environment variable is required');
}
