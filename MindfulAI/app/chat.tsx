import { useState, useRef, useEffect } from 'react';
import { View, TextInput, TouchableOpacity, KeyboardAvoidingView, Platform, FlatList, Text, ActivityIndicator, Animated } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { useChatStore } from '../store/useChatStore';
import ChatBubble from '../components/chat/ChatBubble';
import { chatWithAIStream } from '../services/api';
import { BlurView } from 'expo-blur';

export default function ChatScreen() {
  const [inputText, setInputText] = useState('');
  const [statusMsg, setStatusMsg] = useState<string | null>(null);
  const flatListRef = useRef<FlatList>(null);
  const insets = useSafeAreaInsets();
  const typingFade = useRef(new Animated.Value(0)).current;
  
  const { messages, addMessage, updateMessage, isTyping, setTyping } = useChatStore();

  useEffect(() => {
    Animated.timing(typingFade, {
      toValue: isTyping ? 1 : 0,
      duration: 250,
      useNativeDriver: true,
    }).start();
  }, [isTyping]);

  const handleSend = async () => {
    if (!inputText.trim()) return;

    const userMessage = {
      id: Date.now().toString(),
      text: inputText.trim(),
      role: 'user' as const,
      createdAt: Date.now(),
    };

    addMessage(userMessage);
    setInputText('');
    setTyping(true);
    setStatusMsg(null);

    setTimeout(() => {
      flatListRef.current?.scrollToEnd({ animated: true });
    }, 100);

    const aiMessageId = (Date.now() + 1).toString();
    const aiMessage = {
      id: aiMessageId,
      text: '',
      role: 'assistant' as const,
      createdAt: Date.now(),
    };

    const MAX_RETRIES = 3;
    const RETRY_DELAY_MS = 5000;

    for (let attempt = 1; attempt <= MAX_RETRIES; attempt++) {
      try {
        const history = [...useChatStore.getState().messages].map((m) => ({
          role: m.role,
          text: m.text,
        }));

        let isFirstChunk = true;
        let receivedAnyChunk = false;
        await chatWithAIStream(history, (chunk) => {
          receivedAnyChunk = true;
          if (isFirstChunk) {
            setTyping(false);
            setStatusMsg(null);
            addMessage(aiMessage);
            isFirstChunk = false;
          }
          const currentMessage = useChatStore.getState().messages.find((m) => m.id === aiMessageId);
          if (currentMessage) {
            updateMessage(aiMessageId, currentMessage.text + chunk);
          }
        });

        if (!receivedAnyChunk) {
          addMessage({
            ...aiMessage,
            text: "I connected, but did not receive a response from the model. Please try again.",
          });
        }

        // Success — break out of retry loop
        break;
      } catch (error: any) {
        const isNetworkError = error?.message?.includes('Network error');
        const isLastAttempt = attempt === MAX_RETRIES;

        if (isNetworkError && !isLastAttempt) {
          setStatusMsg(`AI is waking up... retrying (${attempt}/${MAX_RETRIES - 1})`);
          await new Promise((r) => setTimeout(r, RETRY_DELAY_MS));
        } else {
          setStatusMsg(null);
          // Show error as a chat message instead of crashing
          const errText = isNetworkError
            ? "I'm having trouble connecting right now. Please try again in a moment."
            : `Something went wrong: ${error?.message ?? 'Unknown error'}`;
          addMessage({ ...aiMessage, text: errText });
          console.error('AI response error:', error);
          break;
        }
      }
    }

    setTyping(false);
    setStatusMsg(null);
  };

  return (
    <View className="flex-1 bg-background" style={{ paddingTop: insets.top }}>
      {/* Header */}
      <View className="px-6 py-4 border-b border-white/5 z-10 bg-background/90 absolute top-0 left-0 right-0" style={{ marginTop: insets.top }}>
        <Text className="text-xl font-semibold text-text tracking-wide">MindfulAI</Text>
      </View>

      <KeyboardAvoidingView
        style={{ flex: 1 }}
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        keyboardVerticalOffset={insets.top}
      >
        <FlatList
          ref={flatListRef}
          data={messages}
          keyExtractor={(item) => item.id}
          renderItem={({ item }) => <ChatBubble message={item} />}
          contentContainerStyle={{ paddingHorizontal: 20, paddingTop: 80, paddingBottom: 20 }}
          onContentSizeChange={() => flatListRef.current?.scrollToEnd({ animated: true })}
          showsVerticalScrollIndicator={false}
        />

        {/* Cold-start / retry status message */}
        {statusMsg && (
          <View className="px-6 pb-1">
            <View className="bg-yellow-500/10 self-start rounded-full px-4 py-2 border border-yellow-500/20">
              <Text className="text-yellow-400 text-xs font-medium">{statusMsg}</Text>
            </View>
          </View>
        )}

        {/* Typing indicator — sits above the input bar */}
        <Animated.View
          style={{ opacity: typingFade }}
          pointerEvents={isTyping ? 'auto' : 'none'}
        >
          <View className="px-6 pb-2">
            <View className="bg-surface/80 self-start rounded-full px-4 py-2.5 flex-row items-center gap-2 border border-white/5 shadow-sm">
              <ActivityIndicator size="small" color="#38BDF8" />
              <Text className="text-textMuted text-sm font-medium">MindfulAI is typing...</Text>
            </View>
          </View>
        </Animated.View>

        {/* Input bar — in normal flow so KeyboardAvoidingView pushes it up */}
        <BlurView
          intensity={80}
          tint="dark"
          className="border-t border-white/5"
          style={{ paddingBottom: Math.max(insets.bottom, 12), paddingTop: 12, paddingHorizontal: 16 }}
        >
          <View className="flex-row items-end bg-[#1E293B]/60 rounded-3xl border border-white/10 pr-2 pl-5 py-1.5 shadow-lg">
            <TextInput
              className="flex-1 text-text text-base pt-2.5 pb-2.5 max-h-32"
              placeholder="Type your feelings..."
              placeholderTextColor="#64748B"
              value={inputText}
              onChangeText={setInputText}
              multiline
              maxLength={500}
            />
            <TouchableOpacity
              onPress={handleSend}
              disabled={!inputText.trim() || isTyping}
              className={`ml-2 mb-1.5 rounded-full h-10 w-10 items-center justify-center ${
                inputText.trim() && !isTyping ? 'bg-primary' : 'bg-white/5'
              }`}
            >
              <Text className={`text-xl font-bold ${inputText.trim() && !isTyping ? 'text-background' : 'text-white/20'}`}>
                ↑
              </Text>
            </TouchableOpacity>
          </View>
        </BlurView>
      </KeyboardAvoidingView>
    </View>
  );
}
