"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.predictRisk = exports.MLServiceError = void 0;
const axios_1 = __importStar(require("axios"));
const config_1 = require("../config");
class MLServiceError extends Error {
    constructor(message, statusCode, originalError) {
        super(message);
        this.statusCode = statusCode;
        this.originalError = originalError;
        this.name = 'MLServiceError';
    }
}
exports.MLServiceError = MLServiceError;
const predictRisk = async (request) => {
    try {
        const response = await axios_1.default.post(config_1.config.pythonMlServiceUrl, request, {
            headers: { 'Content-Type': 'application/json' },
            timeout: 15000, // 15 seconds timeout
        });
        return response.data;
    }
    catch (error) {
        if (error instanceof axios_1.AxiosError) {
            const status = error.response?.status;
            const message = error.response?.data?.message || error.message;
            throw new MLServiceError(`ML service error: ${message}`, status, error);
        }
        throw new MLServiceError('Unexpected error communicating with ML service', 500, error);
    }
};
exports.predictRisk = predictRisk;
