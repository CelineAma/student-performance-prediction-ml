"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.hashPassword = exports.authenticateUser = void 0;
const bcryptjs_1 = __importDefault(require("bcryptjs"));
const jsonwebtoken_1 = __importDefault(require("jsonwebtoken"));
const config_1 = require("../config");
// Mock user database (replace with real user store in production)
const users = {
    admin: '$2b$12$LQv3c1yqBFV6xTqB9vE9vQOqXjO5e8qF8pWqE', // password: admin123
};
const authenticateUser = async (username, password) => {
    const storedHash = users[username];
    if (!storedHash) {
        return null;
    }
    const isValid = await bcryptjs_1.default.compare(password, storedHash);
    if (!isValid) {
        return null;
    }
    const token = jsonwebtoken_1.default.sign({ username }, config_1.config.jwtSecret, { expiresIn: '1h' });
    return { token };
};
exports.authenticateUser = authenticateUser;
// Helper to generate a hash for new users (not used in mock, but kept for completeness)
const hashPassword = async (password) => {
    const saltRounds = 12;
    return bcryptjs_1.default.hash(password, saltRounds);
};
exports.hashPassword = hashPassword;
