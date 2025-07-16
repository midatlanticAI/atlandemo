"""
Temporal Resonant Cognitive Substrate
Models experience as intersecting waves over time, not static symbols.
Cognition emerges from harmonic resonance, not computation.
"""

import time
import math
import hashlib
from typing import Dict, List, Optional, Any, Tuple
from collections import deque
from dataclasses import dataclass
from enum import Enum
from .schemas import Schema

from .cog_config import CogConfig
from .schema_store import SchemaStore, JsonSchemaStore, SQLiteSchemaStore


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
    
    def __init__(self, symbol: str, frequency: float, amplitude: float, phase: float = 0.0, decay_rate: float = 0.01):
        self.symbol = symbol
        self.frequency = frequency  # How fast it oscillates
        self.amplitude = amplitude  # How strong it is
        self.phase = phase         # Where in the cycle it starts
        self.birth_time = time.time()
        self.decay_rate = decay_rate  # How fast it fades (can be tuned per wave)
    
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

    def __init__(self, config: CogConfig, max_frames: int = 1000):
        self.config = config

        self.frames: deque = deque(maxlen=max_frames)
        self.active_waves: Dict[str, TemporalWave] = {}
        self.resonance_patterns: List[Dict] = []

        # Consolidation parameters
        self.consolidation_threshold = config.consolidation_threshold
        self.schema_support_threshold = config.schema_support_threshold
        self.max_schemas = config.max_schemas

        # Persistence backend selection
        if config.store_backend == "sqlite":
            self.store: SchemaStore = SQLiteSchemaStore(config.store_path)
        else:
            self.store = JsonSchemaStore(config.store_path)

        self.schemas: Dict[Tuple[str, str], Schema] = self.store.load()

        # Save throttling
        self._unsaved_changes = 0
        self._save_frequency = max(1, config.save_frequency)

    def add_experience(self, frame: ExperienceFrame):
        """Add a new experience frame and update wave dynamics."""
        self.frames.append(frame)
        self._generate_waves_from_frame(frame)
        self._update_wave_interference()
        self._consolidate_patterns()
    
    def _generate_waves_from_frame(self, frame: ExperienceFrame):
        """Generate temporal waves from the symbolic content of a frame."""
        current_time = time.time()
        
        symbols_to_process = list(frame.get_all_symbols())

        # Banded emotion encoding ---------------------------------------
        # Theta-band (6 Hz) valence marker: phase encodes sign, amplitude encodes magnitude
        if abs(frame.mood) >= 0.05:
            symbols_to_process.append("valence_marker")
        # Gamma-band (40 Hz) arousal marker: amplitude encodes arousal
        if frame.arousal >= 0.05:
            symbols_to_process.append("arousal_marker")
        
        # magnitude symbols (very low freq, constant amplitude)
        if abs(frame.mood) >= 0.05:
            symbols_to_process.append("valence_mag")
        if frame.arousal >= 0.05:
            symbols_to_process.append("arousal_mag")
        
        for symbol in symbols_to_process:
            # Calculate wave properties based on frame characteristics
            if symbol == "valence_marker":
                frequency = 6.0  # theta band
                amplitude = abs(frame.mood)
                phase = 0.0 if frame.mood > 0 else math.pi
            elif symbol == "arousal_marker":
                frequency = 40.0  # gamma band
                amplitude = frame.arousal
                phase = 0.0  # phase not used for arousal
            elif symbol == "valence_mag":
                frequency = 0.001  # quasi-DC
                amplitude = abs(frame.mood)
                phase = math.pi / 2  # sin = 1 -> activation ~ amplitude
            elif symbol == "arousal_mag":
                frequency = 0.001
                amplitude = frame.arousal
                phase = math.pi / 2
            else:
                frequency = self._calculate_frequency(symbol, frame)
                amplitude = self._calculate_amplitude(symbol, frame)
                phase = self._calculate_phase(symbol, frame)
            # Decay rate inversely proportional to arousal (high arousal → slower decay)
            decay_rate = 0.0025 * (1.0 - frame.arousal) + 0.0005
            
            # Create or update wave
            if symbol in self.active_waves:
                # Reinforce existing wave
                existing_wave = self.active_waves[symbol]
                existing_wave.amplitude = min(2.0, existing_wave.amplitude + amplitude * 0.5)
                # Nudge phase toward current mood so memory drifts with affect
                existing_wave.phase = (existing_wave.phase + frame.mood * 0.02) % (2 * math.pi)
                existing_wave.birth_time = current_time  # Reset decay
            else:
                # Create new wave with arousal-informed decay
                self.active_waves[symbol] = TemporalWave(symbol, frequency, amplitude, phase, decay_rate)
    
    def _calculate_frequency(self, symbol: str, frame: ExperienceFrame) -> float:
        """Calculate wave frequency based on arousal and attention."""
        base_frequency = 1.0
        arousal_factor = 1.0 + frame.arousal
        attention_factor = 1.0 + frame.attention
        return base_frequency * arousal_factor * attention_factor
    
    def _calculate_amplitude(self, symbol: str, frame: ExperienceFrame) -> float:
        """Return base + k*arousal (linear)."""
        base_amplitude = 0.2
        k = 1.5
        return base_amplitude + k * frame.arousal
    
    def _stable_hash_1000(self, text: str) -> int:
        """Return a stable 0-999 hash value for *text* using MD5 (deterministic across runs)."""
        digest = hashlib.md5(text.encode("utf-8")).hexdigest()
        return int(digest[:6], 16) % 1000  # 24-bit slice → 0-999

    def _calculate_phase(self, symbol: str, frame: ExperienceFrame) -> float:
        """Phase anchors valence: 0 rad for positive, π for negative (±0.1 band).

        A small deterministic symbol-specific offset (≤π/2) is added so that
        identical-valence symbols are not perfectly phase-locked, preventing
        total reinforcement runaway.
        """
        # Anchor by mood sign
        if frame.mood >= 0.1:
            base_phase = 0.0
        elif frame.mood <= -0.1:
            base_phase = math.pi
        else:  # near-neutral – assign pseudo-random offset in ±π/4
            jitter = (self._stable_hash_1000(symbol) / 1000.0 - 0.5) * (math.pi / 2)
            return (jitter) % (2 * math.pi)

        # Add bounded symbol-specific offset to break perfect synchrony (≤π/8, centred at 0)
        offset = (self._stable_hash_1000(symbol) / 1000.0 - 0.5) * (math.pi / 16)
        return (base_phase + offset) % (2 * math.pi)
    
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
        """Promote frequently recurring resonance patterns into stable schemas.

        The method scans recent `resonance_patterns`, aggregates counts per
        symbol pair, and stores them in `self.schemas`.  A pair is considered a
        *schema* once it has appeared `schema_support_threshold` times.  Old or
        weak schemas are pruned to keep the store bounded.
        """
        if not self.resonance_patterns:
            return

        recent_patterns = self.resonance_patterns[-20:]  # only the most recent bursts
        for p in recent_patterns:
            symbols = tuple(sorted(p["symbols"]))  # deterministic ordering
            strength = abs(float(p["interference"]))
            ts = p["timestamp"]

            schema = self.schemas.get(symbols)
            if schema:
                schema.register_observation(strength, ts)
            else:
                self.schemas[symbols] = Schema(symbols=symbols, count=1, cumulative_strength=strength, last_seen=ts)

        # Prune schemas if we exceed the max allowed
        if len(self.schemas) > self.max_schemas:
            # Drop the schemas with the lowest counts first
            sorted_items = sorted(self.schemas.items(), key=lambda kv: kv[1].count)
            for kv in sorted_items[: len(self.schemas) - self.max_schemas]:
                self.schemas.pop(kv[0], None)

        # Throttled persistence
        self._unsaved_changes += 1
        if self._unsaved_changes >= self._save_frequency:
            try:
                self.store.save(self.schemas)
                self._unsaved_changes = 0
            except Exception as e:
                print(f"[ExperienceStream] Warning: failed to persist schemas: {e}")

    def get_schema_summary(self, min_count: int = 3, top_k: int = 10) -> List[Dict]:
        """Return a summary of the strongest schemas for inspection or export."""
        qualified = [s for s in self.schemas.values() if s.count >= min_count]
        qualified.sort(key=lambda s: (s.count, s.avg_strength), reverse=True)
        summary = [
            {
                "symbols": s.symbols,
                "count": s.count,
                "avg_strength": round(s.avg_strength, 3),
                "last_seen": s.last_seen,
            }
            for s in qualified[:top_k]
        ]
        return summary
    
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
    
    def __init__(self, config: Optional[CogConfig] = None):
        """Create a cognition engine.

        Args:
            config: Optional CogConfig; if None, defaults are used.
        """

        from random import seed as _seed

        self.config = config or CogConfig()

        if self.config.deterministic and self.config.seed is not None:
            _seed(self.config.seed)

        self.experience_stream = ExperienceStream(self.config)
        self.replay_cycles = 0
        self.dream_frequency = 5  # Every 5 experiences, trigger replay

        # Rolling windows for integrated emotion
        from collections import deque as _dq
        self._valence_hist = _dq(maxlen=20)  # ~20 frames window
        self._arousal_hist = _dq(maxlen=20)
        
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

        # Update rolling emotion integrators (simple moving average)
        self._valence_hist.append(mood)
        self._arousal_hist.append(arousal)

        val_integrated = sum(self._valence_hist) / len(self._valence_hist)
        ar_integrated = sum(self._arousal_hist) / len(self._arousal_hist)
        
        # Trigger replay/consolidation periodically
        if len(self.experience_stream.frames) % self.dream_frequency == 0:
            self._dream_replay()
        
        return {
            "frame_count": len(self.experience_stream.frames),
            "active_waves": len(self.experience_stream.active_waves),
            "activation_field": self.experience_stream.get_current_activation_field(),
            "recent_resonance": self.experience_stream.get_resonance_summary(),
            "valence_integrated": val_integrated,
            "arousal_integrated": ar_integrated,
        }
    
    def _dream_replay(self):
        """Simulate dream-like replay of recent experiences for consolidation."""
        self.replay_cycles += 1

        # Reinforce active waves that belong to the most frequent schemas
        top_schemas = sorted(
            self.experience_stream.schemas.values(),
            key=lambda s: s.count,
            reverse=True,
        )[:5]

        for schema in top_schemas:
            for sym in schema.symbols:
                if sym in self.experience_stream.active_waves:
                    wave = self.experience_stream.active_waves[sym]
                    wave.amplitude = min(wave.amplitude * 1.1, 3.0)  # bounded growth

        print(
            f"Dream replay cycle {self.replay_cycles} | reinforced {len(top_schemas)} schemas, active waves: {len(self.experience_stream.active_waves)}"
        )
    
    def get_cognitive_state(self) -> Dict[str, Any]:
        """Get comprehensive view of current cognitive state."""
        state = {
            "total_experiences": len(self.experience_stream.frames),
            "active_symbol_count": len(self.experience_stream.active_waves),
            "replay_cycles": self.replay_cycles,
            "activation_field": self.experience_stream.get_current_activation_field(),
            "resonance_patterns": len(self.experience_stream.resonance_patterns),
            "recent_resonance": self.experience_stream.get_resonance_summary(),
            "schemas": self.experience_stream.get_schema_summary(),
        }

        return state 

    def get_emotion_state(self):
        """Return current integrated valence and arousal."""
        if self._valence_hist:
            v = sum(self._valence_hist) / len(self._valence_hist)
            a = sum(self._arousal_hist) / len(self._arousal_hist)
        else:
            v = 0.0
            a = 0.0
        return {"valence": v, "arousal": a} 