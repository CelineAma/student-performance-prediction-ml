"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = require("express");
const authController_1 = require("../controllers/authController");
const predictController_1 = require("../controllers/predictController");
const auth_1 = require("../middleware/auth");
const studentValidator_1 = require("../validation/studentValidator");
const rateLimit_1 = require("../middleware/rateLimit");
const router = (0, express_1.Router)();
// Public route: login
router.post('/auth/login', authController_1.login);
// Protected route: prediction (with validation and rate limiting)
router.post('/predict', auth_1.authenticateToken, rateLimit_1.predictRateLimit, studentValidator_1.validateStudentInput, studentValidator_1.handleValidationErrors, predictController_1.predict);
exports.default = router;
