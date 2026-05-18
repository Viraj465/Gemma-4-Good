import { create } from 'zustand';

export interface Message {
  id: string;
  text: string;
  role: 'user' | 'assistant';
  createdAt: number;
}

interface ChatState {
  messages: Message[];
  isTyping: boolean;
  addMessage: (message: Message) => void;
  updateMessage: (id: string, text: string) => void;
  setTyping: (isTyping: boolean) => void;
}

export const useChatStore = create<ChatState>()((set) => ({
  messages: [
    {
      id: '1',
      text: 'Hello. I am MindfulAI, your peaceful companion. How are you feeling today?',
      role: 'assistant',
      createdAt: Date.now(),
    },
  ],
  isTyping: false,
  addMessage: (message) =>
    set((state) => ({ messages: [...state.messages, message] })),
  updateMessage: (id, text) =>
    set((state) => ({
      messages: state.messages.map((m) =>
        m.id === id ? { ...m, text } : m
      ),
    })),
  setTyping: (isTyping) => set({ isTyping }),
}));