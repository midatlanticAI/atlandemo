#!/usr/bin/env python3
"""
Temporal Wave Field Visualizer
Real-time visualization of cognitive wave interference patterns.
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import time
from src.temporal_cognition import TemporalCognitionEngine
from collections import defaultdict


class WaveFieldVisualizer:
    """Visualizes the temporal cognitive field as interfering waves."""
    
    def __init__(self, engine):
        self.engine = engine
        self.fig, (self.ax1, self.ax2, self.ax3) = plt.subplots(3, 1, figsize=(12, 10))
        self.fig.suptitle('🧠 Temporal Cognitive Wave Field - Live', fontsize=16)
        
        # Wave field plot
        self.ax1.set_title('Active Symbol Waves')
        self.ax1.set_xlabel('Time')
        self.ax1.set_ylabel('Activation Amplitude')
        self.ax1.grid(True, alpha=0.3)
        
        # Interference pattern plot
        self.ax2.set_title('Wave Interference Patterns')
        self.ax2.set_xlabel('Symbol Pairs')
        self.ax2.set_ylabel('Interference Strength')
        
        # Activation field heatmap
        self.ax3.set_title('Current Activation Field')
        
        self.wave_lines = {}
        self.time_points = np.linspace(0, 10, 100)
        
    def update_visualization(self):
        """Update all visualization components."""
        current_time = time.time()
        
        # Clear previous plots
        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()
        
        # Reset titles and labels
        self.ax1.set_title('Active Symbol Waves')
        self.ax1.set_xlabel('Time')
        self.ax1.set_ylabel('Activation Amplitude')
        self.ax1.grid(True, alpha=0.3)
        
        # Plot active waves
        wave_data = []
        for symbol, wave in self.engine.experience_stream.active_waves.items():
            activations = []
            times = []
            for i, t_offset in enumerate(self.time_points):
                t = current_time - (10 - t_offset)  # Last 10 seconds
                activation = wave.get_activation(t)
                activations.append(activation)
                times.append(t_offset)
            
            if max(abs(a) for a in activations) > 0.01:  # Only show significant waves
                self.ax1.plot(times, activations, label=symbol[:10], alpha=0.7)
                wave_data.append((symbol, max(activations, key=abs)))
        
        self.ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        # Plot interference patterns
        resonance = self.engine.experience_stream.get_resonance_summary()
        if resonance:
            pairs = []
            strengths = []
            colors = []
            
            for pattern in resonance[-10:]:  # Last 10 patterns
                pair_name = f"{pattern['symbols'][0][:5]}↔{pattern['symbols'][1][:5]}"
                pairs.append(pair_name)
                strengths.append(pattern['interference'])
                
                # Color by resonance type
                if pattern['resonance_type'] == 'constructive':
                    colors.append('green')
                elif pattern['resonance_type'] == 'destructive':
                    colors.append('red')
                elif pattern['resonance_type'] == 'harmonic':
                    colors.append('blue')
                else:
                    colors.append('orange')
            
            if pairs:
                bars = self.ax2.bar(range(len(pairs)), strengths, color=colors, alpha=0.7)
                self.ax2.set_xticks(range(len(pairs)))
                self.ax2.set_xticklabels(pairs, rotation=45, ha='right')
                self.ax2.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        
        # Activation field heatmap
        field = self.engine.experience_stream.get_current_activation_field()
        if field:
            symbols = list(field.keys())[:20]  # Top 20 symbols
            activations = [field[s] for s in symbols]
            
            # Create heatmap data
            heatmap_data = np.array(activations).reshape(1, -1)
            
            im = self.ax3.imshow(heatmap_data, cmap='RdBu_r', aspect='auto', 
                               vmin=-2, vmax=2, interpolation='nearest')
            self.ax3.set_xticks(range(len(symbols)))
            self.ax3.set_xticklabels([s[:8] for s in symbols], rotation=45, ha='right')
            self.ax3.set_yticks([])
            
            # Add colorbar
            plt.colorbar(im, ax=self.ax3, shrink=0.8)
        
        plt.tight_layout()
        return []
    
    def animate(self, frame):
        """Animation function for real-time updates."""
        return self.update_visualization()
    
    def start_live_view(self, interval=1000):
        """Start live visualization with updates every interval ms."""
        ani = animation.FuncAnimation(self.fig, self.animate, interval=interval, blit=False)
        plt.show()
        return ani


def run_live_wave_demo():
    """Run a live demonstration with wave visualization."""
    
    print("🌊 Starting Live Wave Field Demonstration...")
    
    # Create engine
    engine = TemporalCognitionEngine()
    
    # Create visualizer
    visualizer = WaveFieldVisualizer(engine)
    
    # Simulate some initial experiences
    print("Adding initial experiences...")
    
    engine.live_experience(
        visual=["bird", "flying"],
        auditory=["chirping"],
        mood=0.7,
        arousal=0.8,
        attention=0.9,
        goals=["observe"],
        surprise=0.6,
        satisfaction=0.8
    )
    
    time.sleep(0.5)
    
    engine.live_experience(
        visual=["airplane", "sky"],
        auditory=["engine"],
        mood=0.5,
        arousal=0.6,
        attention=0.7,
        goals=["understand"],
        surprise=0.4,
        satisfaction=0.7
    )
    
    time.sleep(0.5)
    
    engine.live_experience(
        visual=["butterfly", "wings"],
        auditory=["silence"],
        mood=0.8,
        arousal=0.5,
        attention=0.9,
        goals=["appreciate"],
        surprise=0.5,
        satisfaction=0.9
    )
    
    # Show initial state
    visualizer.update_visualization()
    
    print("\n🧠 Wave Field Visualization Ready!")
    print("You should see:")
    print("• Top: Active symbol waves over time")
    print("• Middle: Interference patterns between concepts") 
    print("• Bottom: Current activation field heatmap")
    print("\nPress Ctrl+C to exit")
    
    try:
        # Start live visualization
        visualizer.start_live_view(interval=2000)  # Update every 2 seconds
    except KeyboardInterrupt:
        print("\n🌊 Wave visualization ended.")
        plt.close('all')


def static_wave_analysis():
    """Generate static analysis of wave patterns without live plotting."""
    
    print("🔬 Static Wave Pattern Analysis")
    print("=" * 50)
    
    # Create engine and add experiences
    engine = TemporalCognitionEngine()
    
    experiences = [
        {
            "name": "Bird Flying",
            "visual": ["bird", "wings", "sky"],
            "auditory": ["chirping", "wind"],
            "mood": 0.6, "arousal": 0.8, "attention": 0.9,
            "goals": ["observe"], "surprise": 0.7, "satisfaction": 0.5
        },
        {
            "name": "Parent Teaching",
            "visual": ["parent"], "auditory": ["birds", "fly", "wings"],
            "mood": 0.4, "arousal": 0.6, "attention": 0.8,
            "goals": ["learn"], "surprise": 0.3, "satisfaction": 0.7
        },
        {
            "name": "Failed Flight Attempt",
            "visual": ["arms", "flapping"], "auditory": ["whooshing"],
            "mood": 0.2, "arousal": 0.9, "attention": 0.7,
            "goals": ["fly"], "surprise": 0.8, "satisfaction": -0.3
        },
        {
            "name": "Understanding",
            "visual": ["self", "different"], "auditory": ["explanation"],
            "mood": 0.1, "arousal": 0.5, "attention": 0.8,
            "goals": ["understand"], "surprise": 0.4, "satisfaction": 0.8
        },
        {
            "name": "Toy Airplane",
            "visual": ["airplane", "toy"], "auditory": ["zoom"],
            "mood": 0.7, "arousal": 0.7, "attention": 0.6,
            "goals": ["play"], "surprise": 0.2, "satisfaction": 0.9
        }
    ]
    
    for i, exp in enumerate(experiences, 1):
        print(f"\nExperience {i}: {exp['name']}")
        result = engine.live_experience(**{k: v for k, v in exp.items() if k != 'name'})
        print(f"  Active waves: {result['active_waves']}")
        print(f"  Resonance patterns: {len(result['recent_resonance'])}")
        time.sleep(0.1)
    
    # Analyze final state
    print(f"\n🧠 Final Cognitive State:")
    state = engine.get_cognitive_state()
    print(f"  Total experiences: {state['total_experiences']}")
    print(f"  Active symbols: {state['active_symbol_count']}")
    print(f"  Resonance patterns: {state['resonance_patterns']}")
    print(f"  Dream cycles: {state['replay_cycles']}")
    
    # Show top activations
    print(f"\n📊 Top Symbol Activations:")
    field = state['activation_field']
    sorted_field = sorted(field.items(), key=lambda x: abs(x[1]), reverse=True)
    
    for symbol, activation in sorted_field[:10]:
        strength = "🔥" if abs(activation) > 0.5 else "⚡" if abs(activation) > 0.2 else "✨"
        print(f"  {strength} {symbol}: {activation:.3f}")
    
    # Test generalization
    print(f"\n🦋 Testing Butterfly Generalization...")
    result = engine.live_experience(
        visual=["butterfly", "wings", "colorful"],
        mood=0.8, arousal=0.6, attention=0.9,
        goals=["observe"], surprise=0.6, satisfaction=0.8
    )
    
    field = result['activation_field']
    wings_activation = field.get('wings', 0)
    fly_activation = field.get('fly', 0)
    
    print(f"  Wings activation: {wings_activation:.3f}")
    print(f"  Fly activation: {fly_activation:.3f}")
    
    if abs(wings_activation) > 0.1 or abs(fly_activation) > 0.1:
        print("  ✅ Generalization detected through wave resonance!")
    else:
        print("  ❌ No clear generalization pattern")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--static":
        static_wave_analysis()
    else:
        try:
            run_live_wave_demo()
        except ImportError:
            print("⚠️  matplotlib not available for live visualization")
            print("Running static analysis instead...\n")
            static_wave_analysis() 