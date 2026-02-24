"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.login = void 0;
const authService_1 = require("../services/authService");
const login = async (req, res) => {
    try {
        const { username, password } = req.body;
        if (!username || !password) {
            return res.status(400).json({ error: 'Username and password are required' });
        }
        const result = await (0, authService_1.authenticateUser)(username, password);
        if (!result) {
            return res.status(401).json({ error: 'Invalid credentials' });
        }
        res.json(result);
    }
    catch (error) {
        console.error('Login error:', error);
        res.status(500).json({ error: 'Internal server error' });
    }
};
exports.login = login;
