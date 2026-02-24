"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.config = void 0;
const dotenv_1 = __importDefault(require("dotenv"));
dotenv_1.default.config();
exports.config = {
    port: parseInt(process.env.PORT || '3000', 10), // Default to 3000 if not set
    jwtSecret: process.env.JWT_SECRET,
    pythonMlServiceUrl: process.env.PYTHON_ML_SERVICE_URL || 'http://localhost:8000/predict',
};
if (!exports.config.jwtSecret) {
    throw new Error('JWT_SECRET environment variable is required');
}
