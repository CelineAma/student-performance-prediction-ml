import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';
import { config } from '../config';
import { AuthRequest, AuthResponse } from '../types';

const users: Record<string, string> = {
  [config.adminUsername]: config.adminPasswordHash!,
};
console.log('\n=== USERS OBJECT ===');
console.log('Users object keys:', Object.keys(users));
console.log('Users object:', users);

export const authenticateUser = async (username: string, password: string): Promise<AuthResponse | null> => {
  console.log('\n=== AUTH ATTEMPT ===');
  console.log('Username received:', username);
  console.log('Password received:', password);
  console.log('Looking for user:', username);
  console.log('Available users:', Object.keys(users));
  const storedHash = users[username];
  console.log('Stored hash found:', !!storedHash);
  if (!storedHash) {
    console.log('❌ No hash found for username:', username)
    return null;
  }

  const isValid = await bcrypt.compare(password, storedHash);
   console.log('bcrypt.compare result:', isValid);
  if (!isValid) {
     console.log('❌ Password does not match');
    return null;
  }

  const token = jwt.sign({ username }, config.jwtSecret!, { expiresIn: '24h' });
  return { token };
};

export const hashPassword = async (password: string): Promise<string> => {
  const saltRounds = 12;
  return bcrypt.hash(password, saltRounds);
};
