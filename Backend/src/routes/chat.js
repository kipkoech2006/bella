javascript
import express from 'express';
import { sendMessage, getHistory, clearHistory } from '../controllers/chatController.js';
import { authenticateToken } from '../middleware/auth.js';

const router = express.Router();

router.post('/message', authenticateToken, sendMessage);
router.get('/history', authenticateToken, getHistory);
router.delete('/history', authenticateToken, clearHistory);

export default router;