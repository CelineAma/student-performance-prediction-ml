import { Router } from 'express';
import { login } from '../controllers/authController';
import { predict } from '../controllers/predictController';
import { authenticateToken } from '../middleware/auth';
import { validateStudentInput, handleValidationErrors } from '../validation/studentValidator';
import { predictRateLimit } from '../middleware/rateLimit';

const router = Router();

// Public route: login
router.post('/auth/login', login);

// Protected route: prediction (with validation and rate limiting)
router.post('/predict', authenticateToken, predictRateLimit, validateStudentInput, handleValidationErrors, predict);

export default router;
