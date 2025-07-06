"""
Wave Engine Interactive Chatbot System
Advanced conversational AI with real-time adaptive control capabilities.
Uses temporal wave dynamics for precise timing and pattern recognition.
"""

import time
import math
import random
import asyncio
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from enum import Enum
import numpy as np
from collections import deque
import json

# Import our temporal cognition engine
from src.temporal_cognition import TemporalCognitionEngine, ExperienceFrame


class InteractionMode(Enum):
    CONVERSATION = "conversation"
    GUIDANCE = "guidance"
    REACTIVE = "reactive"
    PREDICTIVE = "predictive"
    ADAPTIVE = "adaptive"


class ResponseIntensity(Enum):
    GENTLE = "gentle"
    MODERATE = "moderate"
    INTENSE = "intense"
    EXTREME = "extreme"


@dataclass
class UserState:
    """Real-time user state tracking"""
    session_id: str
    arousal_level: float  # 0.0 to 1.0
    engagement_score: float  # 0.0 to 1.0
    response_pattern: List[float]  # Historical response times
    preferred_intensity: ResponseIntensity
    current_mood: str
    session_duration: float
    last_interaction: float
    
    def update_arousal(self, delta: float):
        """Update arousal with bounds checking"""
        self.arousal_level = max(0.0, min(1.0, self.arousal_level + delta))
    
    def get_response_signature(self) -> List[float]:
        """Generate wave signature for current state"""
        return [
            self.arousal_level,
            self.engagement_score,
            self.session_duration / 3600.0,  # Normalize to hours
            len(self.response_pattern) / 100.0,  # Normalize interaction count
            time.time() - self.last_interaction,  # Time since last interaction
        ]


@dataclass
class ChatMessage:
    """Structured chat message with metadata"""
    content: str
    sender: str  # "user" or "bot"
    timestamp: float
    message_type: str  # "text", "command", "response"
    emotion: str
    intensity: float
    context_tags: List[str]


@dataclass
class ControlCommand:
    """Real-time control command"""
    command_type: str
    intensity: float  # 0.0 to 1.0
    duration: float  # seconds
    pattern: str  # "steady", "pulse", "wave", "random"
    timestamp: float
    
    def to_wave_params(self) -> Dict[str, float]:
        """Convert to wave engine parameters"""
        return {
            "frequency": self.intensity * 10.0,  # 0-10 Hz
            "amplitude": self.intensity,
            "duration": self.duration,
            "pattern": self.pattern
        }


class WaveInteractiveChatbot:
    """
    Advanced chatbot with wave engine control capabilities.
    Combines conversational AI with real-time adaptive responses.
    """
    
    def __init__(self):
        self.cognition = TemporalCognitionEngine()
        self.user_sessions = {}
        self.conversation_history = deque(maxlen=1000)
        self.control_patterns = {}
        self.learning_enabled = True
        
        # Initialize response patterns
        self._initialize_response_patterns()
        
        # Conversation templates
        self.conversation_templates = {
            "greeting": [
                "Hello there! I'm here to make this experience amazing for you ✨",
                "Welcome! I can sense you're ready for something special 😊",
                "Hi beautiful! Let's create something incredible together 💫"
            ],
            "encouragement": [
                "You're doing so well! Let's keep building this energy 🔥",
                "I can feel how much you're enjoying this... let's go deeper 💖",
                "Your responses are perfect - trust the process 🌟"
            ],
            "guidance": [
                "Let me guide you through this next part... focus on the sensation",
                "I'm going to adjust the intensity based on your breathing",
                "Feel how your body responds... I'm matching your rhythm perfectly"
            ],
            "climax_approach": [
                "I can sense you're getting close... let me help you build it",
                "Your energy is peaking - should I increase the intensity?",
                "Almost there... I'm going to make this moment perfect for you"
            ],
            "aftercare": [
                "That was absolutely incredible! How are you feeling? 💖",
                "Take your time to breathe... you did amazing ✨",
                "I hope that was everything you wanted and more 🌙"
            ]
        }
    
    def _initialize_response_patterns(self):
        """Initialize control response patterns"""
        self.control_patterns = {
            "gentle_waves": {
                "frequency": 0.5,
                "amplitude": 0.3,
                "pattern": "sine",
                "duration": 30.0
            },
            "building_pulse": {
                "frequency": 1.0,
                "amplitude": 0.6,
                "pattern": "pulse",
                "duration": 60.0
            },
            "intense_rhythm": {
                "frequency": 2.0,
                "amplitude": 0.8,
                "pattern": "wave",
                "duration": 45.0
            },
            "climax_sequence": {
                "frequency": 3.0,
                "amplitude": 1.0,
                "pattern": "crescendo",
                "duration": 90.0
            },
            "afterglow": {
                "frequency": 0.2,
                "amplitude": 0.2,
                "pattern": "gentle",
                "duration": 120.0
            }
        }
    
    def start_session(self, user_id: str) -> str:
        """Start a new interactive session"""
        session_id = f"session_{user_id}_{int(time.time())}"
        
        self.user_sessions[session_id] = UserState(
            session_id=session_id,
            arousal_level=0.1,
            engagement_score=0.0,
            response_pattern=[],
            preferred_intensity=ResponseIntensity.MODERATE,
            current_mood="curious",
            session_duration=0.0,
            last_interaction=time.time()
        )
        
        # Send greeting
        greeting = random.choice(self.conversation_templates["greeting"])
        self._send_message(session_id, greeting, "greeting")
        
        return session_id
    
    def process_user_input(self, session_id: str, user_input: str) -> Dict[str, Any]:
        """Process user input and generate appropriate response"""
        if session_id not in self.user_sessions:
            return {"error": "Session not found"}
        
        user_state = self.user_sessions[session_id]
        current_time = time.time()
        
        # Update session duration
        user_state.session_duration += current_time - user_state.last_interaction
        user_state.last_interaction = current_time
        
        # Analyze user input
        input_analysis = self._analyze_input(user_input)
        
        # Generate response based on wave engine analysis
        response_data = self._generate_wave_response(session_id, input_analysis)
        
        # Update user state
        self._update_user_state(session_id, input_analysis, response_data)
        
        # Record interaction for learning
        self._record_interaction(session_id, user_input, response_data)
        
        return response_data
    
    def _analyze_input(self, user_input: str) -> Dict[str, Any]:
        """Analyze user input for emotional content and intent"""
        input_lower = user_input.lower()
        
        # Emotion detection
        emotion_keywords = {
            "excited": ["yes", "more", "harder", "faster", "love", "amazing"],
            "hesitant": ["maybe", "slow", "gentle", "not sure", "wait"],
            "satisfied": ["good", "perfect", "right", "exactly", "yes"],
            "overwhelmed": ["too much", "stop", "slower", "less", "pause"],
            "curious": ["what", "how", "why", "tell me", "show me"]
        }
        
        detected_emotion = "neutral"
        emotion_strength = 0.5
        
        for emotion, keywords in emotion_keywords.items():
            matches = sum(1 for keyword in keywords if keyword in input_lower)
            if matches > 0:
                detected_emotion = emotion
                emotion_strength = min(1.0, matches / len(keywords) + 0.5)
                break
        
        # Intent detection
        intent_keywords = {
            "increase": ["more", "harder", "faster", "intense", "up"],
            "decrease": ["less", "slower", "gentle", "soft", "down"],
            "maintain": ["keep", "stay", "continue", "same", "perfect"],
            "stop": ["stop", "pause", "break", "enough", "done"],
            "explore": ["try", "different", "new", "change", "experiment"]
        }
        
        detected_intent = "maintain"
        for intent, keywords in intent_keywords.items():
            if any(keyword in input_lower for keyword in keywords):
                detected_intent = intent
                break
        
        return {
            "emotion": detected_emotion,
            "emotion_strength": emotion_strength,
            "intent": detected_intent,
            "input_text": user_input,
            "timestamp": time.time()
        }
    
    def _generate_wave_response(self, session_id: str, input_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate response using wave engine dynamics"""
        user_state = self.user_sessions[session_id]
        
        # Calculate wave interference between user state and input
        user_signature = user_state.get_response_signature()
        input_signature = self._input_to_signature(input_analysis)
        
        # Wave interference calculation
        resonance_score = self._calculate_resonance(user_signature, input_signature)
        
        # Generate appropriate response
        response_text = self._select_response_text(user_state, input_analysis, resonance_score)
        
        # Generate control command
        control_command = self._generate_control_command(user_state, input_analysis, resonance_score)
        
        # Predict next user state
        predicted_arousal = self._predict_arousal_change(user_state, input_analysis, control_command)
        
        return {
            "response_text": response_text,
            "control_command": control_command,
            "predicted_arousal": predicted_arousal,
            "resonance_score": resonance_score,
            "timestamp": time.time(),
            "user_state": {
                "current_arousal": user_state.arousal_level,
                "engagement": user_state.engagement_score,
                "session_duration": user_state.session_duration
            }
        }
    
    def _input_to_signature(self, input_analysis: Dict[str, Any]) -> List[float]:
        """Convert input analysis to wave signature"""
        return [
            input_analysis["emotion_strength"],
            1.0 if input_analysis["intent"] == "increase" else 0.0,
            1.0 if input_analysis["intent"] == "decrease" else 0.0,
            1.0 if input_analysis["emotion"] == "excited" else 0.0,
            time.time() % 1.0  # Temporal component
        ]
    
    def _calculate_resonance(self, user_signature: List[float], input_signature: List[float]) -> float:
        """Calculate wave resonance between user state and input"""
        if len(user_signature) != len(input_signature):
            return 0.5
        
        resonance = 0.0
        for i in range(len(user_signature)):
            phase_diff = abs(user_signature[i] - input_signature[i])
            if phase_diff < 0.2:
                resonance += 1.0
            elif phase_diff < 0.5:
                resonance += 0.5
            else:
                resonance += 0.1
        
        return resonance / len(user_signature)
    
    def _select_response_text(self, user_state: UserState, input_analysis: Dict[str, Any], resonance: float) -> str:
        """Select appropriate response text based on context"""
        # Determine response category based on arousal level
        if user_state.arousal_level < 0.3:
            category = "encouragement"
        elif user_state.arousal_level < 0.7:
            category = "guidance"
        elif user_state.arousal_level < 0.9:
            category = "climax_approach"
        else:
            category = "aftercare"
        
        # Select response and personalize it
        base_response = random.choice(self.conversation_templates[category])
        
        # Add contextual elements based on input analysis
        if input_analysis["emotion"] == "excited":
            base_response += " I can feel your excitement! 🔥"
        elif input_analysis["emotion"] == "hesitant":
            base_response += " Take your time, there's no rush 💖"
        elif input_analysis["emotion"] == "overwhelmed":
            base_response = "Let's slow down and breathe together... that's perfect ✨"
        
        return base_response
    
    def _generate_control_command(self, user_state: UserState, input_analysis: Dict[str, Any], resonance: float) -> ControlCommand:
        """Generate control command based on user state and input"""
        current_time = time.time()
        
        # Base intensity on arousal level and resonance
        base_intensity = user_state.arousal_level * resonance
        
        # Modify based on user intent
        if input_analysis["intent"] == "increase":
            intensity = min(1.0, base_intensity + 0.2)
            duration = 30.0
            pattern = "building_pulse"
        elif input_analysis["intent"] == "decrease":
            intensity = max(0.1, base_intensity - 0.2)
            duration = 45.0
            pattern = "gentle_waves"
        elif input_analysis["intent"] == "stop":
            intensity = 0.0
            duration = 5.0
            pattern = "afterglow"
        else:  # maintain or explore
            intensity = base_intensity
            duration = 40.0
            pattern = "wave" if resonance > 0.7 else "pulse"
        
        return ControlCommand(
            command_type="intensity_control",
            intensity=intensity,
            duration=duration,
            pattern=pattern,
            timestamp=current_time
        )
    
    def _predict_arousal_change(self, user_state: UserState, input_analysis: Dict[str, Any], control_command: ControlCommand) -> float:
        """Predict how arousal will change based on control command"""
        current_arousal = user_state.arousal_level
        
        # Calculate expected change based on control intensity
        intensity_factor = control_command.intensity * 0.1
        
        # Modify based on user's emotional state
        if input_analysis["emotion"] == "excited":
            intensity_factor *= 1.5
        elif input_analysis["emotion"] == "hesitant":
            intensity_factor *= 0.5
        elif input_analysis["emotion"] == "overwhelmed":
            intensity_factor *= -0.5
        
        predicted_arousal = min(1.0, max(0.0, current_arousal + intensity_factor))
        return predicted_arousal
    
    def _update_user_state(self, session_id: str, input_analysis: Dict[str, Any], response_data: Dict[str, Any]):
        """Update user state based on interaction"""
        user_state = self.user_sessions[session_id]
        
        # Update arousal based on prediction
        user_state.arousal_level = response_data["predicted_arousal"]
        
        # Update engagement based on resonance
        resonance_boost = response_data["resonance_score"] * 0.1
        user_state.engagement_score = min(1.0, user_state.engagement_score + resonance_boost)
        
        # Update response pattern
        response_time = time.time() - input_analysis["timestamp"]
        user_state.response_pattern.append(response_time)
        if len(user_state.response_pattern) > 20:
            user_state.response_pattern.pop(0)
        
        # Update mood based on emotion
        user_state.current_mood = input_analysis["emotion"]
    
    def _record_interaction(self, session_id: str, user_input: str, response_data: Dict[str, Any]):
        """Record interaction for learning and analysis"""
        interaction = {
            "session_id": session_id,
            "user_input": user_input,
            "response_data": response_data,
            "timestamp": time.time()
        }
        
        self.conversation_history.append(interaction)
        
        # Record in cognition engine
        if self.learning_enabled:
            self._record_cognitive_experience(session_id, user_input, response_data)
    
    def _record_cognitive_experience(self, session_id: str, user_input: str, response_data: Dict[str, Any]):
        """Record interaction as cognitive experience"""
        user_state = self.user_sessions[session_id]
        
        # Visual symbols - what the system "sees"
        visual_symbols = [
            f"arousal_{user_state.arousal_level:.1f}",
            f"engagement_{user_state.engagement_score:.1f}",
            f"mood_{user_state.current_mood}"
        ]
        
        # Auditory symbols - what the system "hears"
        auditory_symbols = [
            f"input_emotion_{response_data.get('emotion', 'neutral')}",
            f"resonance_{response_data['resonance_score']:.1f}"
        ]
        
        # Context
        context = [
            f"session_{session_id}",
            f"duration_{user_state.session_duration:.1f}",
            f"intensity_{response_data['control_command'].intensity:.1f}"
        ]
        
        # Goals
        goals = ["maximize_pleasure", "maintain_engagement", "user_satisfaction"]
        
        # Calculate surprise and satisfaction
        surprise = abs(response_data["predicted_arousal"] - user_state.arousal_level)
        satisfaction = response_data["resonance_score"]
        
        # Record experience
        self.cognition.live_experience(
            visual=visual_symbols,
            auditory=auditory_symbols,
            mood=user_state.arousal_level * 2 - 1,  # Convert to -1 to 1
            arousal=user_state.arousal_level,
            attention=user_state.engagement_score,
            goals=goals,
            context=context,
            surprise=surprise,
            satisfaction=satisfaction
        )
    
    def _send_message(self, session_id: str, message: str, message_type: str):
        """Send message to user (placeholder for actual implementation)"""
        chat_message = ChatMessage(
            content=message,
            sender="bot",
            timestamp=time.time(),
            message_type=message_type,
            emotion="friendly",
            intensity=0.7,
            context_tags=[]
        )
        
        # In real implementation, this would send to user interface
        print(f"🤖 Bot: {message}")
    
    def get_session_analytics(self, session_id: str) -> Dict[str, Any]:
        """Get comprehensive analytics for a session"""
        if session_id not in self.user_sessions:
            return {"error": "Session not found"}
        
        user_state = self.user_sessions[session_id]
        cognitive_state = self.cognition.get_cognitive_state()
        
        return {
            "session_id": session_id,
            "duration": user_state.session_duration,
            "current_arousal": user_state.arousal_level,
            "engagement_score": user_state.engagement_score,
            "interaction_count": len(user_state.response_pattern),
            "average_response_time": np.mean(user_state.response_pattern) if user_state.response_pattern else 0,
            "current_mood": user_state.current_mood,
            "cognitive_patterns": cognitive_state["active_symbol_count"],
            "learning_cycles": cognitive_state["total_experiences"]
        }


def run_interactive_demo():
    """Demonstrate the wave interactive chatbot"""
    print("🌊 WAVE ENGINE INTERACTIVE CHATBOT DEMO")
    print("=" * 60)
    
    # Initialize chatbot
    chatbot = WaveInteractiveChatbot()
    
    # Start session
    session_id = chatbot.start_session("demo_user")
    print(f"🎯 Started session: {session_id}")
    
    # Simulate conversation
    demo_inputs = [
        "Hi there! I'm ready to start",
        "This feels amazing, can you make it more intense?",
        "Yes! That's perfect, keep going",
        "I'm getting close... don't stop",
        "That was incredible! Thank you"
    ]
    
    print(f"\n💬 SIMULATED CONVERSATION")
    print("-" * 40)
    
    for i, user_input in enumerate(demo_inputs, 1):
        print(f"\n👤 User: {user_input}")
        
        # Process input
        response = chatbot.process_user_input(session_id, user_input)
        
        # Display response
        print(f"🤖 Bot: {response['response_text']}")
        
        # Display control command
        cmd = response['control_command']
        print(f"⚡ Control: {cmd.intensity:.1f} intensity, {cmd.pattern} pattern for {cmd.duration:.0f}s")
        
        # Display metrics
        print(f"📊 Arousal: {response['user_state']['current_arousal']:.2f}, "
              f"Engagement: {response['user_state']['engagement']:.2f}, "
              f"Resonance: {response['resonance_score']:.2f}")
        
        # Simulate time passing
        time.sleep(0.5)
    
    # Show analytics
    print(f"\n📈 SESSION ANALYTICS")
    print("-" * 40)
    analytics = chatbot.get_session_analytics(session_id)
    
    for key, value in analytics.items():
        if key != "session_id":
            if isinstance(value, float):
                print(f"   {key.replace('_', ' ').title()}: {value:.3f}")
            else:
                print(f"   {key.replace('_', ' ').title()}: {value}")
    
    print(f"\n🚀 BUSINESS APPLICATIONS")
    print("-" * 40)
    print(f"   🔥 Real-time responsiveness: Sub-second adaptation")
    print(f"   🧠 Learning AI: Improves with each interaction")
    print(f"   🎯 Personalization: Wave-based user matching")
    print(f"   📊 Analytics: Comprehensive session insights")
    print(f"   🌊 Wave Control: Precise temporal pattern generation")
    
    print(f"\n💰 REVENUE POTENTIAL")
    print("-" * 40)
    print(f"   📱 Premium subscription tier")
    print(f"   🔧 Custom hardware integration")
    print(f"   📊 Advanced analytics dashboard")
    print(f"   🎨 Personality customization")
    print(f"   🌐 Multi-platform deployment")


if __name__ == "__main__":
    run_interactive_demo() 