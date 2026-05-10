import dotenv from 'dotenv';

dotenv.config();

export const config = {
  port: parseInt(process.env.PORT || '3000', 10),
  jwtSecret: process.env.JWT_SECRET,
  pythonMlServiceUrl: process.env.PYTHON_ML_SERVICE_URL || 'http://localhost:8000/predict',
  adminUsername: process.env.ADMIN_USERNAME || 'admin',
  adminPasswordHash: process.env.ADMIN_PASSWORD_HASH,
};
console.log('\n=== CONFIG OBJECT ===');
console.log('config.adminUsername:', config.adminUsername);
console.log('config.adminPasswordHash exists:', !!config.adminPasswordHash);
console.log('config.adminPasswordHash prefix:', config.adminPasswordHash?.substring(0, 15));


if (!config.jwtSecret) {
  throw new Error('JWT_SECRET environment variable is required');
}

if (!config.adminPasswordHash) {
  throw new Error('Admin password hash environment variable is required');
}
