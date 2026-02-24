import rateLimit from 'express-rate-limit';
import { Request, Response } from 'express';

/**
 * Rate limiting configuration for the /api/predict endpoint.
 *
 * Why rate limiting is important:
 * - Prevents abuse/overload of the ML inference service
 * - Ensures fair usage among academic users
 * - Protects against accidental or malicious bursts of requests
 * - Helps maintain system stability during peak usage (e.g., end-of-semester advising)
 *
 * Where it is applied:
 * - Applied only to the /api/predict endpoint, which involves ML inference
 * - Not applied to /api/auth/login (authentication should be responsive)
 * - Positioned after authentication but before validation and prediction logic
 */
export const predictRateLimit = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 30, // Allow up to 30 prediction requests per IP per 15 minutes
  message: {
    error: 'Too many prediction requests',
    details: 'You have exceeded the allowed number of prediction requests. Please try again later.',
  },
  standardHeaders: true, // Return rate limit info in `RateLimit-*` headers
  legacyHeaders: false, // Disable the `X-RateLimit-*` headers
  keyGenerator: (req: Request): string => {
    // Use IP address; in production with trusted proxies, consider req.ip behind a proxy
    return req.ip ?? 'unknown';
  },
  handler: (req: Request, res: Response) => {
    res.status(429).json({
      error: 'Too many prediction requests',
      details: 'You have exceeded the allowed number of prediction requests. Please try again later.',
      retryAfter: '15 minutes',
    });
  },
});
