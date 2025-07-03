#!/usr/bin/env python3
"""
Ultimate Wave-Native Cognition Visual Suite
Real-time visualization of consciousness through wave physics
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle, Rectangle
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
from collections import deque
import time
import threading
from src.temporal_cognition import TemporalCognitionEngine
import colorcet as cc

# Set up the visual style
plt.style.use('dark_background')
sns.set_palette("husl")

class WaveVisualizationSuite:
    """Ultimate visual accompaniment for wave-native cognition"""
    
    def __init__(self):
        self.engine = TemporalCognitionEngine()
        self.wave_history = deque(maxlen=1000)
        self.interference_history = deque(maxlen=500)
        self.consciousness_metrics = deque(maxlen=200)
        
        # Color schemes for different wave types
        self.colors = {
            'constructive': '#00ff41',  # Matrix green
            'destructive': '#ff073a',   # Deep red
            'harmonic': '#7209b7',      # Purple
            'dissonant': '#ff8500',     # Orange
            'neural': '#00d4ff',        # Cyan
            'memory': '#ffff00',        # Yellow
        }
        
        # Initialize the master figure
        self.fig = None
        self.axes = {}
        self.animations = []
        self.running = False
        
    def setup_master_display(self):
        """Create the ultimate multi-panel visualization"""
        # Create massive figure with subplots
        self.fig = plt.figure(figsize=(24, 16))
        self.fig.suptitle('🌊 WAVE-NATIVE CONSCIOUSNESS VISUALIZATION 🧠', 
                         fontsize=20, fontweight='bold', color='white')
        
        # Define grid layout (4x4 for maximum visual impact)
        gs = self.fig.add_gridspec(4, 4, hspace=0.3, wspace=0.3)
        
        # Top row: Wave interference patterns
        self.axes['wave_3d'] = self.fig.add_subplot(gs[0, 0:2], projection='3d')
        self.axes['interference'] = self.fig.add_subplot(gs[0, 2:4])
        
        # Second row: Cognitive dynamics
        self.axes['activation_field'] = self.fig.add_subplot(gs[1, 0:2])
        self.axes['consciousness_spiral'] = self.fig.add_subplot(gs[1, 2:4], projection='polar')
        
        # Third row: Specialized visualizations
        self.axes['harmony_waves'] = self.fig.add_subplot(gs[2, 0])
        self.axes['phase_space'] = self.fig.add_subplot(gs[2, 1])
        self.axes['resonance_coupling'] = self.fig.add_subplot(gs[2, 2])
        self.axes['temporal_flow'] = self.fig.add_subplot(gs[2, 3])
        
        # Bottom row: Neural-like activity
        self.axes['neural_field'] = self.fig.add_subplot(gs[3, 0:2])
        self.axes['memory_consolidation'] = self.fig.add_subplot(gs[3, 2:4])
        
        # Style all axes
        for name, ax in self.axes.items():
            if hasattr(ax, 'set_facecolor'):
                ax.set_facecolor('black')
            ax.grid(True, alpha=0.3)
            
        return self.fig
    
    def visualize_wave_interference_3d(self, symbols_data):
        """Ultimate 3D wave interference visualization"""
        ax = self.axes['wave_3d']
        ax.clear()
        
        if not symbols_data:
            return
        
        # Create 3D wave mesh
        x = np.linspace(-5, 5, 100)
        y = np.linspace(-5, 5, 100)
        X, Y = np.meshgrid(x, y)
        Z = np.zeros_like(X)
        
        # Add each symbol as a wave source
        for symbol, activation in symbols_data.items():
            if abs(activation) > 0.1:  # Only show significant activations
                # Create wave centered at random position
                center_x = hash(symbol) % 10 - 5
                center_y = hash(symbol + 'y') % 10 - 5
                
                # Calculate wave contribution
                distance = np.sqrt((X - center_x)**2 + (Y - center_y)**2)
                wave_freq = 1.0 + abs(activation)
                wave_amp = activation * 0.5
                
                # Add wave to surface
                wave_contrib = wave_amp * np.sin(wave_freq * distance + time.time() * 3)
                Z += wave_contrib
        
        # Create stunning 3D surface
        surf = ax.plot_surface(X, Y, Z, cmap='plasma', alpha=0.8, 
                              linewidth=0, antialiased=True)
        
        # Add wave sources as glowing spheres
        for symbol, activation in symbols_data.items():
            if abs(activation) > 0.3:
                center_x = hash(symbol) % 10 - 5
                center_y = hash(symbol + 'y') % 10 - 5
                color = self.colors['constructive'] if activation > 0 else self.colors['destructive']
                ax.scatter([center_x], [center_y], [activation], 
                          s=abs(activation)*200, c=color, alpha=0.9)
        
        ax.set_title('🌊 3D Wave Interference Field', fontsize=14, fontweight='bold')
        ax.set_xlabel('Symbolic Space X')
        ax.set_ylabel('Symbolic Space Y')
        ax.set_zlabel('Activation Amplitude')
        
    def visualize_consciousness_spiral(self, metrics):
        """Consciousness as a spiral through phase space"""
        ax = self.axes['consciousness_spiral']
        ax.clear()
        
        if not metrics:
            return
            
        # Create consciousness spiral
        theta = np.linspace(0, 4*np.pi, len(metrics))
        r = np.array([m.get('awareness', 0) for m in metrics])
        
        # Plot spiral with color gradient
        colors = plt.cm.viridis(np.linspace(0, 1, len(r)))
        ax.scatter(theta, r, c=colors, s=50, alpha=0.8)
        
        # Add consciousness "attractor"
        if len(metrics) > 10:
            recent_r = r[-10:]
            recent_theta = theta[-10:]
            ax.plot(recent_theta, recent_r, 'w-', linewidth=3, alpha=0.7)
        
        ax.set_title('🧠 Consciousness Spiral', fontsize=14, fontweight='bold')
        ax.set_ylim(0, 2)
        
    def visualize_harmony_waves(self, harmony_data):
        """Musical harmony through wave interference"""
        ax = self.axes['harmony_waves']
        ax.clear()
        
        t = np.linspace(0, 2*np.pi, 1000)
        
        # Base wave (C note)
        c_freq = 261.63
        c_wave = np.sin(c_freq * t / 100)
        ax.plot(t, c_wave, color=self.colors['neural'], linewidth=2, alpha=0.7, label='C note')
        
        # Harmony wave (G note)
        g_freq = 392.00
        g_wave = np.sin(g_freq * t / 100)
        ax.plot(t, g_wave, color=self.colors['harmonic'], linewidth=2, alpha=0.7, label='G note')
        
        # Interference pattern
        interference = c_wave + g_wave
        ax.plot(t, interference, color=self.colors['constructive'], linewidth=3, 
                alpha=0.9, label='Harmony')
        
        ax.set_title('🎵 Musical Harmony Waves', fontsize=12, fontweight='bold')
        ax.set_xlabel('Time')
        ax.set_ylabel('Amplitude')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
    def visualize_phase_space(self, wave_data):
        """Phase space visualization"""
        ax = self.axes['phase_space']
        ax.clear()
        
        if not wave_data:
            return
        
        # Create phase space plot
        phases = []
        frequencies = []
        amplitudes = []
        
        for symbol, activation in wave_data.items():
            if abs(activation) > 0.1:
                phase = (hash(symbol) % 360) * np.pi / 180
                freq = 1.0 + abs(activation)
                amp = abs(activation)
                
                phases.append(phase)
                frequencies.append(freq)
                amplitudes.append(amp * 100)
        
        if phases:
            scatter = ax.scatter(phases, frequencies, s=amplitudes, 
                               c=amplitudes, cmap='plasma', alpha=0.8)
            ax.set_title('⚡ Phase Space Dynamics', fontsize=12, fontweight='bold')
            ax.set_xlabel('Phase')
            ax.set_ylabel('Frequency')
            
    def visualize_resonance_coupling(self, resonance_data):
        """Resonance coupling network"""
        ax = self.axes['resonance_coupling']
        ax.clear()
        
        if not resonance_data:
            return
        
        # Create network of resonant connections
        for i, pattern in enumerate(resonance_data[-10:]):  # Show last 10 patterns
            if 'symbols' in pattern and len(pattern['symbols']) >= 2:
                # Position nodes
                x1, y1 = i * 0.3, np.sin(i * 0.5)
                x2, y2 = i * 0.3 + 0.1, np.cos(i * 0.5)
                
                # Draw connection
                interference = pattern.get('interference', 0)
                color = self.colors['constructive'] if interference > 0 else self.colors['destructive']
                linewidth = abs(interference) * 5
                
                ax.plot([x1, x2], [y1, y2], color=color, linewidth=linewidth, alpha=0.7)
                ax.scatter([x1, x2], [y1, y2], s=50, c=color, alpha=0.9)
        
        ax.set_title('🔗 Resonance Coupling', fontsize=12, fontweight='bold')
        ax.set_xlim(-0.5, 3)
        ax.set_ylim(-2, 2)
        
    def visualize_temporal_flow(self, temporal_data):
        """Temporal flow visualization"""
        ax = self.axes['temporal_flow']
        ax.clear()
        
        if not temporal_data:
            return
        
        # Create flowing temporal patterns
        t = np.linspace(0, 10, 200)
        flow_patterns = []
        
        for i, data in enumerate(temporal_data[-5:]):  # Last 5 experiences
            amplitude = data.get('amplitude', 0.5)
            frequency = data.get('frequency', 1.0)
            phase = data.get('phase', 0)
            
            pattern = amplitude * np.sin(frequency * t + phase + time.time())
            flow_patterns.append(pattern)
            
            color = plt.cm.viridis(i / 5)
            ax.plot(t, pattern, color=color, linewidth=2, alpha=0.7)
        
        ax.set_title('⏰ Temporal Flow', fontsize=12, fontweight='bold')
        ax.set_xlabel('Time')
        ax.set_ylabel('Activation')
        
    def visualize_neural_field(self, activation_field):
        """Neural field visualization"""
        ax = self.axes['neural_field']
        ax.clear()
        
        if not activation_field:
            return
        
        # Create 2D neural field
        field_size = 20
        field = np.zeros((field_size, field_size))
        
        # Map symbols to field positions
        for symbol, activation in activation_field.items():
            x = hash(symbol) % field_size
            y = hash(symbol + 'y') % field_size
            field[y, x] = activation
        
        # Apply Gaussian blur for realistic neural field
        from scipy.ndimage import gaussian_filter
        field_smooth = gaussian_filter(field, sigma=1.0)
        
        # Create stunning heatmap
        im = ax.imshow(field_smooth, cmap='plasma', aspect='auto', 
                      interpolation='bilinear', alpha=0.8)
        
        # Add contour lines
        ax.contour(field_smooth, levels=10, colors='white', alpha=0.3, linewidths=0.5)
        
        ax.set_title('🧠 Neural Activation Field', fontsize=12, fontweight='bold')
        ax.set_xlabel('Neural Space X')
        ax.set_ylabel('Neural Space Y')
        
    def visualize_memory_consolidation(self, memory_patterns):
        """Memory consolidation visualization"""
        ax = self.axes['memory_consolidation']
        ax.clear()
        
        if not memory_patterns:
            return
        
        # Create memory consolidation visualization
        x = np.arange(len(memory_patterns))
        strengths = [abs(p.get('interference', 0)) for p in memory_patterns]
        
        # Color by resonance type
        colors = []
        for pattern in memory_patterns:
            resonance_type = pattern.get('resonance_type', 'harmonic')
            colors.append(self.colors.get(resonance_type, '#ffffff'))
        
        bars = ax.bar(x, strengths, color=colors, alpha=0.8)
        
        # Add glow effect
        for bar, strength in zip(bars, strengths):
            if strength > 0.5:  # Strong memories glow
                bar.set_edgecolor('white')
                bar.set_linewidth(2)
        
        ax.set_title('💭 Memory Consolidation', fontsize=12, fontweight='bold')
        ax.set_xlabel('Memory Pattern')
        ax.set_ylabel('Consolidation Strength')
        
    def update_all_visualizations(self):
        """Update all visualizations with current engine state"""
        if not self.engine:
            return
            
        # Get current cognitive state
        state = self.engine.get_cognitive_state()
        activation_field = state.get('activation_field', {})
        recent_resonance = state.get('recent_resonance', [])
        
        # Update each visualization
        self.visualize_wave_interference_3d(activation_field)
        
        # Create consciousness metrics
        consciousness_metric = {
            'awareness': len(activation_field) / 50.0,  # Normalize by max symbols
            'coherence': state.get('resonance_patterns', 0) / 100.0,
            'complexity': state.get('active_symbol_count', 0) / 30.0
        }
        self.consciousness_metrics.append(consciousness_metric)
        
        self.visualize_consciousness_spiral(list(self.consciousness_metrics))
        self.visualize_harmony_waves(activation_field)
        self.visualize_phase_space(activation_field)
        self.visualize_resonance_coupling(recent_resonance)
        
        # Create temporal data
        temporal_data = [
            {'amplitude': np.random.random(), 'frequency': 1 + np.random.random(), 
             'phase': np.random.random() * 2 * np.pi}
            for _ in range(10)
        ]
        self.visualize_temporal_flow(temporal_data)
        
        self.visualize_neural_field(activation_field)
        self.visualize_memory_consolidation(recent_resonance)
        
    def run_live_visualization(self, test_function=None):
        """Run live visualization with optional test function"""
        self.setup_master_display()
        self.running = True
        
        def update_frame(frame):
            if not self.running:
                return
                
            # Run test function if provided
            if test_function:
                test_function(self.engine)
            
            # Update all visualizations
            self.update_all_visualizations()
            
            # Update figure
            self.fig.canvas.draw()
            
        # Create animation
        anim = animation.FuncAnimation(self.fig, update_frame, 
                                     interval=100, blit=False)
        
        plt.tight_layout()
        plt.show()
        
        return anim
        
    def create_static_showcase(self):
        """Create a static showcase of all visualizations"""
        self.setup_master_display()
        
        # Generate sample data
        sample_activation = {
            'harmony': 0.8, 'dissonance': -0.6, 'resonance': 0.9,
            'phase': 0.4, 'amplitude': 0.7, 'frequency': 0.5,
            'constructive': 0.8, 'destructive': -0.4, 'neural': 0.6
        }
        
        sample_resonance = [
            {'symbols': ['harmony', 'resonance'], 'interference': 0.8, 'resonance_type': 'constructive'},
            {'symbols': ['phase', 'amplitude'], 'interference': 0.6, 'resonance_type': 'harmonic'},
            {'symbols': ['dissonance', 'clash'], 'interference': -0.7, 'resonance_type': 'destructive'}
        ]
        
        # Update visualizations with sample data
        self.visualize_wave_interference_3d(sample_activation)
        self.visualize_harmony_waves(sample_activation)
        self.visualize_phase_space(sample_activation)
        self.visualize_resonance_coupling(sample_resonance)
        self.visualize_neural_field(sample_activation)
        self.visualize_memory_consolidation(sample_resonance)
        
        # Add some consciousness metrics
        for i in range(50):
            metric = {
                'awareness': 0.5 + 0.3 * np.sin(i * 0.2),
                'coherence': 0.4 + 0.2 * np.cos(i * 0.15),
                'complexity': 0.6 + 0.3 * np.sin(i * 0.3)
            }
            self.consciousness_metrics.append(metric)
        
        self.visualize_consciousness_spiral(list(self.consciousness_metrics))
        
        # Create temporal data
        temporal_data = [
            {'amplitude': 0.5 + 0.3 * np.sin(i), 'frequency': 1 + 0.5 * np.cos(i), 
             'phase': i * 0.3}
            for i in range(20)
        ]
        self.visualize_temporal_flow(temporal_data)
        
        plt.tight_layout()
        plt.savefig('wave_cognition_showcase.png', dpi=300, bbox_inches='tight')
        plt.show()


def run_visual_wave_tests():
    """Run wave tests with ultimate visual accompaniment"""
    print("🌊 LAUNCHING ULTIMATE WAVE VISUALIZATION SUITE 🌊")
    print("=" * 70)
    
    viz = WaveVisualizationSuite()
    
    def test_sequence(engine):
        """Test sequence for live visualization"""
        # Musical harmony test
        engine.live_experience(
            visual=["piano", "C", "G"],
            auditory=["harmony", "consonance"],
            mood=0.8, arousal=0.6, attention=0.9,
            goals=["listen"], satisfaction=0.9
        )
        
        time.sleep(0.1)
        
        # Rotation test
        engine.live_experience(
            visual=["dot", "rotating", "clockwise"],
            auditory=["motion"],
            mood=0.5, arousal=0.7, attention=0.8,
            goals=["track"]
        )
        
        time.sleep(0.1)
        
        # Resonance test
        engine.live_experience(
            visual=["tuning", "forks", "resonating"],
            auditory=["amplified", "frequency"],
            mood=0.7, arousal=0.8, attention=0.9,
            goals=["observe"], satisfaction=0.8
        )
    
    # Run live visualization
    print("Starting live wave visualization...")
    viz.run_live_visualization(test_sequence)


if __name__ == "__main__":
    # Check if we want live or static visualization
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--static":
        print("Creating static showcase...")
        viz = WaveVisualizationSuite()
        viz.create_static_showcase()
    else:
        run_visual_wave_tests() 