import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';
import { config } from '../config';
import { AuthRequest, AuthResponse } from '../types';

const users: Record<string, string> = {
  [config.adminUsername]: config.adminPasswordHash!,
};

export const authenticateUser = async (username: string, password: string): Promise<AuthResponse | null> => {

  const storedHash = users[username];
  if (!storedHash) {
    console.log('No hash found for username:', username)
    return null;
  }

  const isValid = await bcrypt.compare(password, storedHash);
  if (!isValid) {
     console.log('Password does not match');
    return null;
  }

  const token = jwt.sign({ username }, config.jwtSecret!, { expiresIn: '24h' });
  return { token };
};

export const hashPassword = async (password: string): Promise<string> => {
  const saltRounds = 12;
  return bcrypt.hash(password, saltRounds);
};
