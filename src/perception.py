import time
from typing import List, Tuple, Dict, Any


class ToneEngine:
    """Scores phrase sentiment based on keywords and basic negation handling."""
    
    def __init__(self):
        # Simple keyword mapping for sentiment scoring
        self.affect_map = {
            # Positive terms
            "great": 0.6, "scheduled": 0.5, "ready": 0.5, "satisfaction": 0.7,
            "happy": 0.9, "hopeful": 0.7, "okay": 0.4, "neutral": 0.0,
            "grateful": 0.8, "energized": 0.6, "pleased": 0.7, "thanked": 0.7,
            "resolved": 0.6, "success": 0.8, "appreciate": 0.7, "satisfied": 0.6,
            "premium": 0.5, "interest": 0.4, "quick": 0.5, "renewal": 0.3,
            
            # Negative terms
            "missed": -0.4, "no reply": -0.6, "upset": -0.5, "unresolved": -0.7,
            "delayed": -0.6, "tired": -0.3, "anxious": -0.6, "angry": -0.8,
            "sad": -0.7, "frustrated": -0.6, "issue": -0.4, "complaint": -0.7,
            "urgent": -0.4, "problem": -0.5, "misunderstanding": -0.3, "billing": -0.2,
            
            # Neutral/context terms
            "help": 0.1, "followed up": 0.2, "no change": 0.0, "appointment": 0.1,
            "voicemail": -0.1, "meeting": 0.2, "call": 0.0, "service": 0.2
        }
        
        self.negation_words = {"not", "no", "didn't", "wasn't", "never", "none"}
        
        # Response templates for different emotional tones
        self.response_templates = {
            "uplifting": "You're doing great — keep the momentum going!",
            "encouraging": "I see progress — want to build on that?",
            "neutral": "I'm here if you want to explore more.",
            "gentle": "That sounds like a lot. Take your time.",
            "soothing": "Let's slow down and focus on one thing together."
        }

    def score_phrase(self, phrase: str) -> float:
        """Calculates a sentiment score for the input phrase."""
        score = 0.0
        words = phrase.lower().split()
        word_set = set(words)
        negation_present = bool(self.negation_words.intersection(word_set))
        
        for keyword, value in self.affect_map.items():
            # Check if keyword is present (can be improved with stemming/lemmatization)
            if keyword in phrase.lower():  # Simple substring check
                score += value
        
        # Apply basic negation: flip score if negation words are nearby
        # (This is very rudimentary sentiment analysis)
        if negation_present and score != 0:
            score *= -0.5  # Dampen and potentially flip score
        
        # Ensure score stays within a reasonable range, e.g., -1 to 1
        return round(max(-1.0, min(1.0, score)), 2)

    def infer_tone(self, mood_score: float) -> str:
        """
        Classifies tone based on average mood value.

        Args:
            mood_score: Mood value between -1.0 and 1.0

        Returns:
            Tone classification string
        """
        if mood_score > 0.5:
            return "uplifting"
        elif mood_score > 0.1:
            return "encouraging"
        elif mood_score < -0.5:
            return "soothing"
        elif mood_score < -0.1:
            return "gentle"
        else:
            return "neutral"

    def get_response_template(self, tone: str) -> str:
        """
        Returns a tone-calibrated response template.

        Args:
            tone: The tone classification

        Returns:
            Response template string
        """
        return self.response_templates.get(tone, self.response_templates["neutral"])


class DriftTracker:
    """Tracks mood history, calculates drift, average, and volatility."""
    
    def __init__(self, max_window: int = 30):
        if not isinstance(max_window, int) or max_window <= 0:
            raise ValueError("max_window must be a positive integer")
        self.max_window = max_window
        self.mood_history: List[Tuple[float, float]] = []  # (timestamp, mood_score)

    def add_mood(self, mood_score: float):
        """Adds a mood score to the history, maintaining the window size."""
        # Basic validation
        if not isinstance(mood_score, (int, float)):
            # Potentially log a warning or raise error for non-numeric input
            return
        mood_score = float(mood_score)
        
        self.mood_history.append((time.time(), mood_score))
        # Efficiently remove oldest entry if window size exceeded
        if len(self.mood_history) > self.max_window:
            self.mood_history.pop(0)

    def avg_mood(self) -> float:
        """Calculates the average mood score in the current window."""
        if not self.mood_history:
            return 0.0
        return round(sum(s for _, s in self.mood_history) / len(self.mood_history), 3)

    def drift(self) -> float:
        """Calculates the difference between the latest and earliest mood score in the window."""
        if len(self.mood_history) < 2:
            return 0.0
        
        # Ensure indices are valid
        start_mood = self.mood_history[0][1]
        end_mood = self.mood_history[-1][1]
        return round(end_mood - start_mood, 3)

    def classify_drift(self) -> str:
        """
        Classifies the current drift direction and magnitude.

        Returns:
            String classification of drift
        """
        drift = self.drift()
        if drift > 0.5:
            return "strong positive"
        elif drift > 0.1:
            return "mild positive"
        elif drift < -0.5:
            return "strong negative"
        elif drift < -0.1:
            return "mild negative"
        else:
            return "stable"

    def volatility(self) -> float:
        """Calculates the average absolute change between consecutive mood scores."""
        if len(self.mood_history) < 2:
            return 0.0
        
        # Use generator expression for potentially better memory efficiency
        diffs_sum = sum(abs(self.mood_history[i][1] - self.mood_history[i-1][1])
                       for i in range(1, len(self.mood_history)))
        return round(diffs_sum / (len(self.mood_history) - 1), 3)

    def get_state(self) -> Dict[str, Any]:
        """Returns the current state of the tracker."""
        return {
            "average_mood": self.avg_mood(),
            "drift": self.drift(),
            "drift_classification": self.classify_drift(),
            "volatility": self.volatility(),
            "history_length": len(self.mood_history)
        } 