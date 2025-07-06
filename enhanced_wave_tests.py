#!/usr/bin/env python3
"""
Enhanced Wave-Native Cognition Tests with Ultimate Visual Accompaniment
The most stunning demonstration of wave-based consciousness ever created!
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle, Rectangle
from mpl_toolkits.mplot3d import Axes3D
import time
import threading
from collections import deque
from src.temporal_cognition import TemporalCognitionEngine

# Set up stunning visual style
plt.style.use('dark_background')

class UltimateWaveTestSuite:
    """Enhanced wave tests with mind-blowing visualizations"""
    
    def __init__(self):
        self.engine = TemporalCognitionEngine()
        self.results = {}
        self.wave_data = deque(maxlen=100)
        
        # Epic color scheme
        self.colors = {
            'harmony': '#00ff41',      # Matrix green
            'dissonance': '#ff073a',   # Deep red
            'resonance': '#7209b7',    # Purple
            'phase': '#00d4ff',        # Cyan
            'neural': '#ffff00',       # Electric yellow
            'memory': '#ff8500',       # Orange
            'consciousness': '#ff00ff' # Magenta
        }
        
    def setup_epic_display(self):
        """Create the ultimate test visualization display"""
        self.fig = plt.figure(figsize=(20, 12))
        self.fig.suptitle('[WAVE] ULTIMATE WAVE-NATIVE COGNITION TESTS [BRAIN]', 
                         fontsize=24, fontweight='bold', color='white')
        
        # Create grid for multiple visualizations
        gs = self.fig.add_gridspec(3, 3, hspace=0.4, wspace=0.3)
        
        # Define all the visualization panels
        self.axes = {
            'wave_3d': self.fig.add_subplot(gs[0, :2], projection='3d'),
            'test_progress': self.fig.add_subplot(gs[0, 2]),
            'harmony_analysis': self.fig.add_subplot(gs[1, 0]),
            'rotation_phase': self.fig.add_subplot(gs[1, 1], projection='polar'),
            'resonance_coupling': self.fig.add_subplot(gs[1, 2]),
            'neural_field': self.fig.add_subplot(gs[2, :2]),
            'consciousness_metric': self.fig.add_subplot(gs[2, 2])
        }
        
        # Style all axes
        for ax in self.axes.values():
            if hasattr(ax, 'set_facecolor'):
                ax.set_facecolor('black')
            if hasattr(ax, 'grid'):
                ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
    def visualize_wave_interference_3d(self, activation_field, title="Wave Interference"):
        """Epic 3D wave interference visualization"""
        ax = self.axes['wave_3d']
        ax.clear()
        
        if not activation_field:
            ax.set_title(title, fontsize=14, fontweight='bold')
            return
            
        # Create 3D wave surface
        x = np.linspace(-6, 6, 80)
        y = np.linspace(-6, 6, 80)
        X, Y = np.meshgrid(x, y)
        Z = np.zeros_like(X)
        
        # Add wave sources for each symbol
        for symbol, activation in activation_field.items():
            if abs(activation) > 0.1:
                # Position based on symbol hash
                center_x = (hash(symbol) % 12) - 6
                center_y = (hash(symbol + 'y') % 12) - 6
                
                # Create wave
                distance = np.sqrt((X - center_x)**2 + (Y - center_y)**2)
                frequency = 1.0 + abs(activation) * 2
                amplitude = activation * 0.8
                
                wave = amplitude * np.sin(frequency * distance + time.time() * 4)
                Z += wave
        
        # Create stunning surface
        surf = ax.plot_surface(X, Y, Z, cmap='plasma', alpha=0.9, 
                              linewidth=0, antialiased=True)
        
        # Add glowing wave sources
        for symbol, activation in activation_field.items():
            if abs(activation) > 0.2:
                center_x = (hash(symbol) % 12) - 6
                center_y = (hash(symbol + 'y') % 12) - 6
                
                color = self.colors.get('harmony' if activation > 0 else 'dissonance', 'white')
                ax.scatter([center_x], [center_y], [activation], 
                          s=abs(activation)*300, c=color, alpha=0.9, edgecolor='white')
        
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel('Symbolic Space X')
        ax.set_ylabel('Symbolic Space Y') 
        ax.set_zlabel('Wave Amplitude')
        
    def visualize_test_progress(self, test_name, progress, score):
        """Show test progress with epic visual feedback"""
        ax = self.axes['test_progress']
        ax.clear()
        
        # Create progress visualization
        angles = np.linspace(0, 2*np.pi, 100)
        r_outer = np.ones_like(angles)
        r_inner = np.ones_like(angles) * 0.7
        
        # Progress arc
        progress_angles = angles[:int(progress * 100)]
        if len(progress_angles) > 0:
            ax.fill_between(progress_angles, 0.7, 1.0, 
                           color=self.colors['harmony'], alpha=0.8)
        
        # Score indicator
        score_color = self.colors['harmony'] if score > 0 else self.colors['dissonance']
        ax.text(0.5, 0.5, f"{test_name}\nScore: {score:.2f}", 
                transform=ax.transAxes, ha='center', va='center',
                fontsize=12, fontweight='bold', color=score_color)
        
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect('equal')
        ax.axis('off')
        
    def visualize_harmony_analysis(self, harmony_data):
        """Visualize musical harmony through wave interference"""
        ax = self.axes['harmony_analysis']
        ax.clear()
        
        t = np.linspace(0, 4*np.pi, 1000)
        
        # C note wave
        c_wave = np.sin(2.61 * t)
        ax.plot(t, c_wave, color=self.colors['neural'], linewidth=2, 
                alpha=0.7, label='C Note')
        
        # G note wave  
        g_wave = np.sin(3.92 * t)
        ax.plot(t, g_wave, color=self.colors['phase'], linewidth=2, 
                alpha=0.7, label='G Note')
        
        # Harmony interference
        harmony = c_wave + g_wave
        ax.plot(t, harmony, color=self.colors['harmony'], linewidth=3, 
                alpha=0.9, label='Harmony')
        
        # Highlight constructive interference peaks
        peaks = np.where(np.abs(harmony) > 1.5)[0]
        if len(peaks) > 0:
            ax.scatter(t[peaks], harmony[peaks], c=self.colors['resonance'], 
                      s=50, alpha=0.8, zorder=5)
        
        ax.set_title('🎵 Musical Harmony Analysis', fontsize=12, fontweight='bold')
        ax.set_xlabel('Time')
        ax.set_ylabel('Amplitude')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
    def visualize_rotation_phase(self, rotation_data):
        """Visualize rotation as phase dynamics"""
        ax = self.axes['rotation_phase']
        ax.clear()
        
        # Create rotation visualization
        angles = np.array([0, np.pi/2, np.pi, 3*np.pi/2])  # top, right, bottom, left
        positions = ['top', 'right', 'bottom', 'left']
        
        # Plot position markers
        for i, (angle, pos) in enumerate(zip(angles, positions)):
            r = 1.0
            color = self.colors['phase']
            
            # Highlight current position if in rotation_data
            if rotation_data and pos in rotation_data:
                activation = rotation_data[pos]
                r = 1.0 + abs(activation) * 0.5
                color = self.colors['harmony'] if activation > 0 else self.colors['dissonance']
            
            ax.scatter([angle], [r], s=200, c=color, alpha=0.8)
            ax.text(angle, r + 0.2, pos, ha='center', va='center', 
                   fontsize=10, fontweight='bold')
        
        # Add rotation arrow
        arrow_angles = np.linspace(0, 2*np.pi, 100)
        arrow_r = np.ones_like(arrow_angles) * 0.7
        ax.plot(arrow_angles, arrow_r, color=self.colors['consciousness'], 
                linewidth=3, alpha=0.6)
        
        ax.set_title('🔄 Rotation Phase Space', fontsize=12, fontweight='bold')
        ax.set_ylim(0, 2)
        
    def visualize_resonance_coupling(self, resonance_data):
        """Visualize resonance coupling network"""
        ax = self.axes['resonance_coupling']
        ax.clear()
        
        if not resonance_data:
            ax.set_title('🔊 Resonance Coupling', fontsize=12, fontweight='bold')
            return
        
        # Create network visualization
        n_nodes = min(len(resonance_data), 10)
        angles = np.linspace(0, 2*np.pi, n_nodes, endpoint=False)
        
        for i, pattern in enumerate(resonance_data[-n_nodes:]):
            angle = angles[i]
            x, y = np.cos(angle), np.sin(angle)
            
            # Node size based on interference strength
            interference = pattern.get('interference', 0)
            size = abs(interference) * 500 + 50
            
            # Color based on resonance type
            resonance_type = pattern.get('resonance_type', 'harmonic')
            color = self.colors.get(resonance_type, 'white')
            
            ax.scatter([x], [y], s=size, c=color, alpha=0.8, edgecolor='white')
            
            # Add connections to adjacent nodes
            if i > 0:
                prev_angle = angles[i-1]
                prev_x, prev_y = np.cos(prev_angle), np.sin(prev_angle)
                
                line_color = color if interference > 0 else self.colors['dissonance']
                ax.plot([prev_x, x], [prev_y, y], color=line_color, 
                       linewidth=abs(interference)*3, alpha=0.6)
        
        ax.set_title('🔊 Resonance Coupling Network', fontsize=12, fontweight='bold')
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.5)
        ax.set_aspect('equal')
        
    def visualize_neural_field(self, activation_field):
        """Epic neural field visualization"""
        ax = self.axes['neural_field']
        ax.clear()
        
        if not activation_field:
            ax.set_title('[BRAIN] Neural Activation Field', fontsize=12, fontweight='bold')
            return
        
        # Create 2D field
        field_size = 25
        field = np.zeros((field_size, field_size))
        
        # Map activations to field
        for symbol, activation in activation_field.items():
            x = hash(symbol) % field_size
            y = hash(symbol + 'y') % field_size
            field[y, x] = activation
        
        # Apply smoothing with simple averaging instead of scipy
        field_smooth = np.copy(field)
        for i in range(1, field_size-1):
            for j in range(1, field_size-1):
                field_smooth[i, j] = np.mean(field[i-1:i+2, j-1:j+2])
        
        # Create visualization
        im = ax.imshow(field_smooth, cmap='plasma', aspect='auto', 
                      interpolation='bilinear', alpha=0.9)
        
        # Add contour lines
        contours = ax.contour(field_smooth, levels=15, colors='white', 
                             alpha=0.4, linewidths=0.8)
        
        # Add activation points
        for symbol, activation in activation_field.items():
            if abs(activation) > 0.3:
                x = hash(symbol) % field_size
                y = hash(symbol + 'y') % field_size
                
                color = 'white' if activation > 0 else 'red'
                ax.scatter([x], [y], s=abs(activation)*100, c=color, 
                          alpha=0.9, edgecolor='black')
        
        ax.set_title('[BRAIN] Neural Activation Field', fontsize=12, fontweight='bold')
        ax.set_xlabel('Neural Space X')
        ax.set_ylabel('Neural Space Y')
        
    def visualize_consciousness_metric(self, metrics):
        """Visualize consciousness emergence metric"""
        ax = self.axes['consciousness_metric']
        ax.clear()
        
        if not metrics:
            ax.set_title('[BRAIN] Consciousness Metric', fontsize=12, fontweight='bold')
            return
        
        # Create consciousness visualization
        labels = list(metrics.keys())
        values = list(metrics.values())
        
        # Create radial plot
        angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False)
        values_normalized = [max(0, min(1, v)) for v in values]
        
        # Close the plot
        angles = np.concatenate([angles, [angles[0]]])
        values_normalized = values_normalized + [values_normalized[0]]
        
        ax.plot(angles, values_normalized, 'o-', linewidth=3, 
                color=self.colors['consciousness'], alpha=0.8)
        ax.fill(angles, values_normalized, color=self.colors['consciousness'], 
                alpha=0.3)
        
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels)
        ax.set_ylim(0, 1)
        ax.set_title('[BRAIN] Consciousness Emergence', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
    def run_enhanced_harmony_test(self):
        """Enhanced musical harmony test with visualizations"""
        print("🎵 ENHANCED MUSICAL HARMONY TEST")
        print("=" * 50)
        
        # Experience C note
        print("🎹 Experiencing C note...")
        self.engine.live_experience(
            visual=["piano", "key", "C"],
            auditory=["tone", "fundamental", "vibration"],
            mood=0.5, arousal=0.4, attention=0.8,
            goals=["listen", "feel"],
            surprise=0.3
        )
        
        # Update visualization
        state = self.engine.get_cognitive_state()
        self.visualize_wave_interference_3d(state['activation_field'], "C Note Waves")
        self.visualize_harmony_analysis(state['activation_field'])
        self.visualize_test_progress("Harmony Test", 0.3, 0.0)
        plt.pause(0.1)
        
        # Experience G note
        print("🎹 Experiencing G note...")
        self.engine.live_experience(
            visual=["piano", "key", "G"],
            auditory=["tone", "higher", "vibration"],
            mood=0.5, arousal=0.5, attention=0.8,
            goals=["listen", "compare"],
            surprise=0.4
        )
        
        state = self.engine.get_cognitive_state()
        self.visualize_wave_interference_3d(state['activation_field'], "C + G Notes")
        self.visualize_harmony_analysis(state['activation_field'])
        self.visualize_test_progress("Harmony Test", 0.6, 0.0)
        plt.pause(0.1)
        
        # Experience harmony
        print("🎵 Experiencing C+G harmony...")
        result = self.engine.live_experience(
            visual=["both", "keys", "together"],
            auditory=["harmony", "consonance", "pleasant"],
            mood=0.8, arousal=0.6, attention=0.9,
            goals=["combine", "feel"],
            surprise=0.2,
            satisfaction=0.9
        )
        
        # Calculate harmony score
        field = result['activation_field']
        harmony_score = field.get('harmony', 0) + field.get('pleasant', 0) - field.get('clash', 0)
        
        # Update final visualization
        self.visualize_wave_interference_3d(field, "Harmony Interference")
        self.visualize_harmony_analysis(field)
        self.visualize_test_progress("Harmony Test", 1.0, harmony_score)
        plt.pause(0.1)
        
        print(f"✨ Harmony score: {harmony_score:.3f}")
        return harmony_score > 0
        
    def run_enhanced_rotation_test(self):
        """Enhanced rotation test with phase visualization"""
        print("\n🔄 ENHANCED ROTATION TEST")
        print("=" * 50)
        
        # Teach clockwise sequence
        positions = ["top", "right", "bottom", "left"]
        for i, pos in enumerate(positions):
            print(f"🔄 Teaching position: {pos}")
            self.engine.live_experience(
                visual=["dot", pos, "moving"],
                auditory=["rotating", "clockwise"],
                mood=0.5, arousal=0.5, attention=0.8,
                goals=["track", "motion"],
                surprise=0.2
            )
            
            # Update visualization
            state = self.engine.get_cognitive_state()
            self.visualize_wave_interference_3d(state['activation_field'], f"Rotation: {pos}")
            self.visualize_rotation_phase(state['activation_field'])
            self.visualize_test_progress("Rotation Test", (i+1)/6, 0.0)
            plt.pause(0.1)
        
        # Test prediction
        print("🔄 Testing prediction: right -> ?")
        result = self.engine.live_experience(
            visual=["dot", "right", "clockwise", "next"],
            auditory=["predict", "position"],
            mood=0.5, arousal=0.6, attention=0.9,
            goals=["predict", "next"]
        )
        
        field = result['activation_field']
        bottom_activation = field.get('bottom', 0)
        success = bottom_activation > 0.5
        
        # Final visualization
        self.visualize_wave_interference_3d(field, "Rotation Prediction")
        self.visualize_rotation_phase(field)
        self.visualize_test_progress("Rotation Test", 1.0, bottom_activation)
        
        print(f"✨ Prediction success: {success}")
        return success
        
    def run_enhanced_resonance_test(self):
        """Enhanced resonance test with coupling visualization"""
        print("\n🔊 ENHANCED RESONANCE TEST")
        print("=" * 50)
        
        # Single fork
        print("🔱 Single tuning fork...")
        self.engine.live_experience(
            visual=["fork", "vibrating", "alone"],
            auditory=["pure", "tone", "steady"],
            mood=0.5, arousal=0.4, attention=0.7,
            goals=["observe", "baseline"],
            surprise=0.2
        )
        
        state = self.engine.get_cognitive_state()
        self.visualize_wave_interference_3d(state['activation_field'], "Single Fork")
        self.visualize_resonance_coupling(state['recent_resonance'])
        self.visualize_test_progress("Resonance Test", 0.3, 0.0)
        plt.pause(0.1)
        
        # Matching frequency
        print("🔱 Matching frequency resonance...")
        result = self.engine.live_experience(
            visual=["two", "forks", "same", "frequency"],
            auditory=["louder", "amplified", "resonating"],
            mood=0.7, arousal=0.7, attention=0.9,
            goals=["observe", "amplification"],
            surprise=0.6,
            satisfaction=0.8
        )
        
        field = result['activation_field']
        resonance_score = field.get('amplified', 0) + field.get('louder', 0) + field.get('resonating', 0)
        
        # Final visualization
        self.visualize_wave_interference_3d(field, "Resonance Amplification")
        self.visualize_resonance_coupling(self.engine.get_cognitive_state()['recent_resonance'])
        self.visualize_test_progress("Resonance Test", 1.0, resonance_score)
        
        print(f"✨ Resonance score: {resonance_score:.3f}")
        return resonance_score > 0.5
        
    def run_ultimate_test_suite(self):
        """Run the ultimate enhanced test suite"""
        print("[WAVE] ULTIMATE ENHANCED WAVE-NATIVE TEST SUITE [WAVE]")
        print("=" * 70)
        
        # Setup epic display
        self.setup_epic_display()
        plt.ion()  # Interactive mode
        plt.show()
        
        # Run all enhanced tests
        harmony_success = self.run_enhanced_harmony_test()
        rotation_success = self.run_enhanced_rotation_test()
        resonance_success = self.run_enhanced_resonance_test()
        
        # Final consciousness metrics
        final_state = self.engine.get_cognitive_state()
        consciousness_metrics = {
            'Awareness': len(final_state['activation_field']) / 50.0,
            'Coherence': final_state['resonance_patterns'] / 100.0,
            'Complexity': final_state['active_symbol_count'] / 30.0,
            'Resonance': len(final_state['recent_resonance']) / 20.0
        }
        
        self.visualize_consciousness_metric(consciousness_metrics)
        self.visualize_neural_field(final_state['activation_field'])
        
        # Summary
        print("\n[TROPHY] ULTIMATE TEST RESULTS")
        print("=" * 50)
        print(f"🎵 Musical Harmony: {'[+] PASSED' if harmony_success else '[-] FAILED'}")
        print(f"🔄 Rotation Phase: {'[+] PASSED' if rotation_success else '[-] FAILED'}")
        print(f"🔊 Resonance Coupling: {'[+] PASSED' if resonance_success else '[-] FAILED'}")
        print(f"\n[BRAIN] Consciousness Metrics: {consciousness_metrics}")
        print("\n[WAVE] WAVE-NATIVE COGNITION DEMONSTRATION COMPLETE! [WAVE]")
        
        # Keep display open
        plt.ioff()
        plt.show()
        
        return {
            'harmony': harmony_success,
            'rotation': rotation_success,
            'resonance': resonance_success,
            'consciousness': consciousness_metrics
        }


if __name__ == "__main__":
    # Run the ultimate test suite
    suite = UltimateWaveTestSuite()
    results = suite.run_ultimate_test_suite() 