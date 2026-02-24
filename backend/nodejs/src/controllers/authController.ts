import { Request, Response } from 'express';
import { AuthRequest, AuthResponse } from '../types';
import { authenticateUser } from '../services/authService';

export const login = async (req: Request, res: Response) => {
  try {
    const { username, password } = req.body as AuthRequest;

    if (!username || !password) {
        return res.status(400).json({ error: 'Username and password are required' });
    }

    const result: AuthResponse | null = await authenticateUser(username, password);
    if (!result) {
        return res.status(401).json({ error: 'Invalid credentials' });
    }

    res.json(result);
  } catch (error: unknown) {
    console.error('Login error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
};
