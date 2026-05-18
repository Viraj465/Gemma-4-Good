import { useEffect, useRef } from 'react';
import { View, Text, Animated } from 'react-native';
import { Message } from '../../store/useChatStore';
import Markdown from 'react-native-markdown-display';

interface ChatBubbleProps {
  message: Message;
}

export default function ChatBubble({ message }: ChatBubbleProps) {
  const isUser = message.role === 'user';
  const timeString = new Date(message.createdAt).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

  // FadeInUp animation for the bubble
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const translateY = useRef(new Animated.Value(20)).current;
  // FadeIn animation for the timestamp (delayed)
  const timeFade = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    Animated.spring(fadeAnim, {
      toValue: 1,
      useNativeDriver: true,
    }).start();

    Animated.spring(translateY, {
      toValue: 0,
      useNativeDriver: true,
    }).start();

    // Delayed fade-in for timestamp
    Animated.timing(timeFade, {
      toValue: 1,
      duration: 400,
      delay: 500,
      useNativeDriver: true,
    }).start();
  }, []);

  return (
    <Animated.View
      style={{
        opacity: fadeAnim,
        transform: [{ translateY }],
        width: '100%',
        flexDirection: 'row',
        marginVertical: 12,
        justifyContent: isUser ? 'flex-end' : 'flex-start',
      }}
    >
      {!isUser && (
        <View className="w-8 h-8 rounded-full bg-surface items-center justify-center mr-2 shadow-sm border border-surface/50 mt-auto mb-5">
          <Text className="text-primary text-sm">✨</Text>
        </View>
      )}
      
      <View style={{ maxWidth: isUser ? '85%' : '80%' }}>
        <View
          className={`rounded-3xl px-5 py-4 ${
            isUser
              ? 'bg-primary rounded-br-sm shadow-sm'
              : 'bg-surface rounded-bl-sm shadow-sm border border-white/5'
          }`}
        >
          {isUser ? (
            <Text className="text-base leading-6 text-background">
              {message.text}
            </Text>
          ) : (
            <Markdown 
              style={{
                body: { color: '#F8FAFC', fontSize: 16, lineHeight: 24 },
                strong: { color: '#38BDF8', fontWeight: '600' },
                bullet_list: { marginTop: 10 },
                list_item: { marginBottom: 5 },
                paragraph: { marginTop: 0, marginBottom: 0 }
              }}
            >
              {message.text}
            </Markdown>
          )}
        </View>
        <Animated.Text 
          style={{ opacity: timeFade }}
          className={`text-xs text-textMuted mt-1 ${isUser ? 'text-right mr-1' : 'ml-1'}`}
        >
          {timeString}
        </Animated.Text>
      </View>
    </Animated.View>
  );
}