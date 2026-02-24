"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.predict = void 0;
const mlService_1 = require("../services/mlService");
const predict = async (req, res) => {
    try {
        const request = req.body;
        const result = await (0, mlService_1.predictRisk)(request);
        res.json(result);
    }
    catch (err) {
        if (err instanceof mlService_1.MLServiceError) {
            return res.status(err.statusCode || 500).json({ error: err.message });
        }
        console.error('Prediction error:', err);
        res.status(500).json({ error: 'Internal server error' });
    }
};
exports.predict = predict;
