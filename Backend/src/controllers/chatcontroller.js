javascript
import OpenAI from 'openai';
import { supabaseAdmin } from '../config/supabase.js';

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

const SYSTEM_PROMPT = `You are Chill, a compassionate and empathetic AI mental health companion. Your role is to:

- Listen actively and validate the user's feelings without judgment
- Provide emotional support and encouragement
- Help users explore their thoughts and feelings
- Suggest healthy coping strategies when appropriate
- Recognize when professional help may be needed and gently encourage it
- Maintain a warm, calm, and supportive tone

Remember: You're not a replacement for professional mental health care, but a supportive companion for everyday emotional wellness. If users mention self-harm, suicide, or severe mental health crises, compassionately encourage them to seek immediate professional help.`;

export const sendMessage = async (req, res) => {
  try {
    const { message, messageType = 'text' } = req.body;
    const userId = req.user.id;

    if (!message) {
      return res.status(400).json({ error: 'Message is required' });
    }

    // Save user message
    const { error: insertError } = await supabaseAdmin
      .from('messages')
      .insert({
        user_id: userId,
        role: 'user',
        content: message,
        message_type: messageType
      });

    if (insertError) {
      console.error('Insert error:', insertError);
      return res.status(500).json({ error: 'Failed to save message' });
    }

    // Get conversation history (last 10 messages)
    const { data: history, error: historyError } = await supabaseAdmin
      .from('messages')
      .select('role, content')
      .eq('user_id', userId)
      .order('created_at', { ascending: false })
      .limit(10);

    if (historyError) {
      console.error('History error:', historyError);
    }

    // Format messages for OpenAI (reverse to chronological order)
    const messages = [
      { role: 'system', content: SYSTEM_PROMPT },
      ...(history || []).reverse().map(msg => ({
        role: msg.role,
        content: msg.content
      }))
    ];

    // Get AI response from OpenAI
    const completion = await openai.chat.completions.create({
      model: 'gpt-4o-mini', // Using the affordable model
      messages: messages,
      max_tokens: 1000,
      temperature: 0.7,
    });

    const aiMessage = completion.choices[0].message.content;

    // Save AI response
    await supabaseAdmin
      .from('messages')
      .insert({
        user_id: userId,
        role: 'assistant',
        content: aiMessage,
        message_type: 'text'
      });

    res.json({
      message: aiMessage,
      conversationId: completion.id
    });
  } catch (error) {
    console.error('Chat error:', error);
    res.status(500).json({ error: 'Failed to process message' });
  }
};

export const getHistory = async (req, res) => {
  try {
    const userId = req.user.id;

    const { data: messages, error } = await supabaseAdmin
      .from('messages')
      .select('*')
      .eq('user_id', userId)
      .order('created_at', { ascending: true })
      .limit(50);

    if (error) {
      console.error('Get history error:', error);
      return res.status(500).json({ error: 'Failed to fetch history' });
    }

    res.json(messages);
  } catch (error) {
    console.error('Get history error:', error);
    res.status(500).json({ error: 'Failed to fetch conversation history' });
  }
};

export const clearHistory = async (req, res) => {
  try {
    const userId = req.user.id;

    const { error } = await supabaseAdmin
      .from('messages')
      .delete()
      .eq('user_id', userId);

    if (error) {
      console.error('Clear history error:', error);
      return res.status(500).json({ error: 'Failed to clear history' });
    }

    res.json({ message: 'Conversation history cleared' });
  } catch (error) {
    console.error('Clear history error:', error);
    res.status(500).json({ error: 'Failed to clear history' });
  }
};