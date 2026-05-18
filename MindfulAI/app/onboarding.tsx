import { useEffect, useRef } from 'react';
import { View, Text, TouchableOpacity, Animated } from 'react-native';
import { useRouter } from 'expo-router';
import { useAppStore } from '../store/useAppStore';

export default function OnboardingScreen() {
  const router = useRouter();
  const setHasSeenOnboarding = useAppStore((state) => state.setHasSeenOnboarding);

  // Animations
  const fade1 = useRef(new Animated.Value(0)).current;
  const slide1 = useRef(new Animated.Value(30)).current;
  const fade2 = useRef(new Animated.Value(0)).current;
  const slide2 = useRef(new Animated.Value(30)).current;

  useEffect(() => {
    // First block: fade + slide up immediately
    Animated.parallel([
      Animated.timing(fade1, { toValue: 1, duration: 700, useNativeDriver: true }),
      Animated.spring(slide1, { toValue: 0, useNativeDriver: true }),
    ]).start();

    // Second block: delayed
    Animated.sequence([
      Animated.delay(500),
      Animated.parallel([
        Animated.timing(fade2, { toValue: 1, duration: 700, useNativeDriver: true }),
        Animated.spring(slide2, { toValue: 0, useNativeDriver: true }),
      ]),
    ]).start();
  }, []);

  const handleStart = () => {
    setHasSeenOnboarding(true);
    router.replace('/chat');
  };

  return (
    <View className="flex-1 bg-background px-6 pt-20 pb-12 justify-between">
      <View className="flex-1 justify-center">
        <Animated.View style={{ opacity: fade1, transform: [{ translateY: slide1 }] }}>
          <Text className="text-4xl font-semibold text-text mb-4 text-center">
            A Safe Space
          </Text>
          <Text className="text-lg text-textMuted text-center leading-7 px-4">
            MindfulAI is here to listen, support, and help you find peace in your daily life.
          </Text>
        </Animated.View>
      </View>

      <Animated.View style={{ opacity: fade2, transform: [{ translateY: slide2 }] }}>
        <TouchableOpacity
          onPress={handleStart}
          className="bg-primary py-4 rounded-full items-center shadow-lg"
        >
          <Text className="text-background font-semibold text-lg">
            Begin Your Journey
          </Text>
        </TouchableOpacity>
      </Animated.View>
    </View>
  );
}