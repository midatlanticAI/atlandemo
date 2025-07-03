"""
Temporal Resonant Cognitive Substrate
Models experience as intersecting waves over time, not static symbols.
Cognition emerges from harmonic resonance, not computation.
"""

import time
import math
from typing import Dict, List, Optional, Any, Tuple
from collections import deque
from dataclasses import dataclass
from enum import Enum


class ResonanceType(Enum):
    CONSTRUCTIVE = "constructive"  # Waves reinforce
    DESTRUCTIVE = "destructive"    # Waves cancel
    HARMONIC = "harmonic"          # Waves create new frequency
    DISSONANT = "dissonant"        # Waves create tension


@dataclass
class ExperienceFrame:
    """A single moment in the stream of experience - multi-modal and temporal."""
    timestamp: float
    
    # Multi-modal sensory input (simplified but extensible)
    visual_symbols: List[str]      # What is "seen" symbolically
    auditory_symbols: List[str]    # What is "heard" symbolically  
    kinesthetic_symbols: List[str] # What is "felt" symbolically
    
    # Internal state
    mood: float                    # Emotional valence (-1.0 to 1.0)
    arousal: float                 # Energy level (0.0 to 1.0)
    attention: float               # Focus intensity (0.0 to 1.0)
    
    # Goal and context
    active_goals: List[str]        # What the agent wants
    context_tags: List[str]        # Situational markers
    
    # Outcome and reinforcement
    surprise: float                # Prediction error (0.0 to 1.0)
    satisfaction: float            # Goal achievement (-1.0 to 1.0)
    
    def get_all_symbols(self) -> List[str]:
        """Return all symbolic content from this frame."""
        return (self.visual_symbols + self.auditory_symbols + 
                self.kinesthetic_symbols + self.active_goals + self.context_tags)


class TemporalWave:
    """Represents a wave of activation spreading through symbolic space over time."""
    
    def __init__(self, symbol: str, frequency: float, amplitude: float, phase: float = 0.0):
        self.symbol = symbol
        self.frequency = frequency  # How fast it oscillates
        self.amplitude = amplitude  # How strong it is
        self.phase = phase         # Where in the cycle it starts
        self.birth_time = time.time()
        self.decay_rate = 0.01     # How fast it fades
    
    def get_activation(self, current_time: float) -> float:
        """Calculate current wave activation based on time."""
        age = current_time - self.birth_time
        decay = math.exp(-self.decay_rate * age)
        wave_value = math.sin(2 * math.pi * self.frequency * age + self.phase)
        return self.amplitude * wave_value * decay
    
    def interfere_with(self, other: 'TemporalWave', current_time: float) -> Tuple[float, ResonanceType]:
        """Calculate interference pattern with another wave."""
        self_activation = self.get_activation(current_time)
        other_activation = other.get_activation(current_time)
        
        # Calculate phase difference
        phase_diff = abs(self.phase - other.phase) % (2 * math.pi)
        
        # Determine resonance type
        if phase_diff < math.pi / 4 or phase_diff > 7 * math.pi / 4:
            resonance_type = ResonanceType.CONSTRUCTIVE
            interference = self_activation + other_activation
        elif phase_diff > 3 * math.pi / 4 and phase_diff < 5 * math.pi / 4:
            resonance_type = ResonanceType.DESTRUCTIVE
            interference = abs(self_activation - other_activation)
        elif abs(self.frequency - other.frequency) < 0.1:
            resonance_type = ResonanceType.HARMONIC
            interference = self_activation * other_activation
        else:
            resonance_type = ResonanceType.DISSONANT
            interference = (self_activation + other_activation) * 0.5
        
        return interference, resonance_type


class ExperienceStream:
    """Manages the temporal flow of experience frames and their resonant interactions."""
    
    def __init__(self, max_frames: int = 1000):
        self.frames: deque = deque(maxlen=max_frames)
        self.active_waves: Dict[str, TemporalWave] = {}
        self.resonance_patterns: List[Dict] = []
        self.consolidation_threshold = 0.7
        
    def add_experience(self, frame: ExperienceFrame):
        """Add a new experience frame and update wave dynamics."""
        self.frames.append(frame)
        self._generate_waves_from_frame(frame)
        self._update_wave_interference()
        self._consolidate_patterns()
    
    def _generate_waves_from_frame(self, frame: ExperienceFrame):
        """Generate temporal waves from the symbolic content of a frame."""
        current_time = time.time()
        
        for symbol in frame.get_all_symbols():
            # Calculate wave properties based on frame characteristics
            frequency = self._calculate_frequency(symbol, frame)
            amplitude = self._calculate_amplitude(symbol, frame)
            phase = self._calculate_phase(symbol, frame)
            
            # Create or update wave
            if symbol in self.active_waves:
                # Reinforce existing wave
                existing_wave = self.active_waves[symbol]
                existing_wave.amplitude = min(2.0, existing_wave.amplitude + amplitude * 0.5)
                existing_wave.birth_time = current_time  # Reset decay
            else:
                # Create new wave
                self.active_waves[symbol] = TemporalWave(symbol, frequency, amplitude, phase)
    
    def _calculate_frequency(self, symbol: str, frame: ExperienceFrame) -> float:
        """Calculate wave frequency based on arousal and attention."""
        base_frequency = 1.0
        arousal_factor = 1.0 + frame.arousal
        attention_factor = 1.0 + frame.attention
        return base_frequency * arousal_factor * attention_factor
    
    def _calculate_amplitude(self, symbol: str, frame: ExperienceFrame) -> float:
        """Calculate wave amplitude based on mood, surprise, and satisfaction."""
        base_amplitude = 0.5
        mood_factor = 1.0 + abs(frame.mood)
        surprise_factor = 1.0 + frame.surprise
        satisfaction_factor = 1.0 + abs(frame.satisfaction)
        return base_amplitude * mood_factor * surprise_factor * satisfaction_factor
    
    def _calculate_phase(self, symbol: str, frame: ExperienceFrame) -> float:
        """Calculate wave phase based on context and timing."""
        # Use symbol hash and frame properties to create phase
        symbol_hash = hash(symbol) % 1000
        mood_phase = frame.mood * math.pi
        return (symbol_hash / 1000.0 * 2 * math.pi + mood_phase) % (2 * math.pi)
    
    def _update_wave_interference(self):
        """Calculate interference patterns between all active waves."""
        current_time = time.time()
        wave_symbols = list(self.active_waves.keys())
        
        for i, symbol1 in enumerate(wave_symbols):
            for symbol2 in wave_symbols[i+1:]:
                wave1 = self.active_waves[symbol1]
                wave2 = self.active_waves[symbol2]
                
                interference, resonance_type = wave1.interfere_with(wave2, current_time)
                
                # Record significant interference patterns
                if abs(interference) > self.consolidation_threshold:
                    pattern = {
                        "symbols": [symbol1, symbol2],
                        "interference": interference,
                        "resonance_type": resonance_type.value,
                        "timestamp": current_time
                    }
                    self.resonance_patterns.append(pattern)
        
        # Remove waves that have decayed below threshold
        self._prune_weak_waves(current_time)
    
    def _prune_weak_waves(self, current_time: float):
        """Remove waves that have decayed below activation threshold."""
        threshold = 0.01
        to_remove = []
        
        for symbol, wave in self.active_waves.items():
            if abs(wave.get_activation(current_time)) < threshold:
                to_remove.append(symbol)
        
        for symbol in to_remove:
            del self.active_waves[symbol]
    
    def _consolidate_patterns(self):
        """Identify and consolidate recurring resonance patterns."""
        # This is where symbolic abstraction emerges from temporal patterns
        # For now, we track patterns - later this becomes belief formation
        pass
    
    def get_current_activation_field(self) -> Dict[str, float]:
        """Get the current activation levels of all symbols."""
        current_time = time.time()
        field = {}
        
        for symbol, wave in self.active_waves.items():
            field[symbol] = wave.get_activation(current_time)
        
        return field
    
    def get_resonance_summary(self) -> List[Dict]:
        """Get summary of recent resonance patterns."""
        # Return last 10 significant patterns
        return self.resonance_patterns[-10:] if self.resonance_patterns else []


class TemporalCognitionEngine:
    """Main engine that orchestrates temporal resonant cognition."""
    
    def __init__(self):
        self.experience_stream = ExperienceStream()
        self.replay_cycles = 0
        self.dream_frequency = 5  # Every 5 experiences, trigger replay
        
    def live_experience(self, 
                       visual: List[str] = None,
                       auditory: List[str] = None, 
                       kinesthetic: List[str] = None,
                       mood: float = 0.0,
                       arousal: float = 0.5,
                       attention: float = 0.5,
                       goals: List[str] = None,
                       context: List[str] = None,
                       surprise: float = 0.0,
                       satisfaction: float = 0.0) -> Dict[str, Any]:
        """Process a lived experience moment."""
        
        frame = ExperienceFrame(
            timestamp=time.time(),
            visual_symbols=visual or [],
            auditory_symbols=auditory or [],
            kinesthetic_symbols=kinesthetic or [],
            mood=mood,
            arousal=arousal,
            attention=attention,
            active_goals=goals or [],
            context_tags=context or [],
            surprise=surprise,
            satisfaction=satisfaction
        )
        
        self.experience_stream.add_experience(frame)
        
        # Trigger replay/consolidation periodically
        if len(self.experience_stream.frames) % self.dream_frequency == 0:
            self._dream_replay()
        
        return {
            "frame_count": len(self.experience_stream.frames),
            "active_waves": len(self.experience_stream.active_waves),
            "activation_field": self.experience_stream.get_current_activation_field(),
            "recent_resonance": self.experience_stream.get_resonance_summary()
        }
    
    def _dream_replay(self):
        """Simulate dream-like replay of recent experiences for consolidation."""
        self.replay_cycles += 1
        
        # In a full implementation, this would:
        # 1. Replay recent high-activation patterns
        # 2. Allow wave interference without new input
        # 3. Consolidate recurring patterns into stable beliefs
        # 4. Prune weak or contradictory patterns
        
        # For now, we just mark that replay occurred
        print(f"Dream replay cycle {self.replay_cycles} - consolidating {len(self.experience_stream.active_waves)} active patterns")
    
    def get_cognitive_state(self) -> Dict[str, Any]:
        """Get comprehensive view of current cognitive state."""
        return {
            "total_experiences": len(self.experience_stream.frames),
            "active_symbol_count": len(self.experience_stream.active_waves),
            "replay_cycles": self.replay_cycles,
            "activation_field": self.experience_stream.get_current_activation_field(),
            "resonance_patterns": len(self.experience_stream.resonance_patterns),
            "recent_resonance": self.experience_stream.get_resonance_summary()
        } 