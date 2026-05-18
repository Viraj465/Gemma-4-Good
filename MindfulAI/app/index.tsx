/// <reference types="nativewind/types" />
import { useEffect, useRef } from 'react';
import { View, Text, Animated } from 'react-native';
import { useRouter } from 'expo-router';
import { useAppStore } from '../store/useAppStore';

export default function SplashScreen() {
  const router = useRouter();
  const hasSeenOnboarding = useAppStore(state => state.hasSeenOnboarding);

  const fadeAnim = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    // Fade in logo over 1.5s
    Animated.timing(fadeAnim, {
      toValue: 1,
      duration: 1500,
      useNativeDriver: true,
    }).start();

    const timer = setTimeout(() => {
      if (hasSeenOnboarding) {
        router.replace('/chat');
      } else {
        router.replace('/onboarding');
      }
    }, 2500);
    return () => clearTimeout(timer);
  }, [hasSeenOnboarding, router]);

  return (
    <View className="flex-1 bg-background items-center justify-center">
      <Animated.View style={{ opacity: fadeAnim }}>
        <Text className="text-4xl font-semibold text-text tracking-widest text-center">
          Mindful<Text className="text-primary">AI</Text>
        </Text>
        <Text className="text-textMuted mt-4 text-center text-lg font-light">
          Your peaceful companion
        </Text>
      </Animated.View>
    </View>
  );
}