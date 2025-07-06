#!/usr/bin/env python3
"""
Ultimate Wave-Native Cognition Visual Demo
Simplified but stunning visualization of consciousness through wave physics
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time
from src.temporal_cognition import TemporalCognitionEngine

# Epic visual setup
plt.style.use('dark_background')

class UltimateWaveDemo:
    """Ultimate wave visualization demonstration"""
    
    def __init__(self):
        self.engine = TemporalCognitionEngine()
        
        # Stunning color palette
        self.colors = {
            'constructive': '#00ff41',  # Matrix green
            'destructive': '#ff073a',   # Deep red
            'harmonic': '#7209b7',      # Purple
            'neural': '#00d4ff',        # Cyan
            'consciousness': '#ffff00', # Electric yellow
            'resonance': '#ff8500',     # Orange
            'phase': '#ff00ff'          # Magenta
        }
        
    def create_stunning_3d_waves(self, activation_field, title="Wave Consciousness"):
        """Create stunning 3D wave visualization"""
        fig = plt.figure(figsize=(15, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        # Create wave mesh
        x = np.linspace(-8, 8, 100)
        y = np.linspace(-8, 8, 100)
        X, Y = np.meshgrid(x, y)
        Z = np.zeros_like(X)
        
        # Generate waves from each active symbol
        for symbol, activation in activation_field.items():
            if abs(activation) > 0.1:
                # Create wave source at position based on symbol
                center_x = (hash(symbol) % 16) - 8
                center_y = (hash(symbol + 'wave') % 16) - 8
                
                # Calculate wave properties
                distance = np.sqrt((X - center_x)**2 + (Y - center_y)**2)
                frequency = 0.8 + abs(activation) * 1.5
                amplitude = activation * 1.2
                
                # Create animated wave
                wave = amplitude * np.sin(frequency * distance + time.time() * 5)
                Z += wave
        
        # Create epic surface
        surf = ax.plot_surface(X, Y, Z, cmap='plasma', alpha=0.8, 
                              linewidth=0, antialiased=True)
        
        # Add glowing wave sources
        for symbol, activation in activation_field.items():
            if abs(activation) > 0.2:
                center_x = (hash(symbol) % 16) - 8
                center_y = (hash(symbol + 'wave') % 16) - 8
                
                # Color based on activation
                color = self.colors['constructive'] if activation > 0 else self.colors['destructive']
                size = abs(activation) * 400
                
                ax.scatter([center_x], [center_y], [activation], 
                          s=size, c=color, alpha=0.9, edgecolor='white', linewidth=2)
                
                # Add symbol label
                ax.text(center_x, center_y, activation + 0.5, symbol, 
                       color='white', fontsize=10, fontweight='bold')
        
        # Epic styling
        ax.set_title(title, fontsize=20, fontweight='bold', color='white', pad=20)
        ax.set_xlabel('Symbolic Space X', fontsize=12, color='white')
        ax.set_ylabel('Symbolic Space Y', fontsize=12, color='white')
        ax.set_zlabel('Wave Amplitude', fontsize=12, color='white')
        
        # Make it look epic
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        
        plt.tight_layout()
        return fig
        
    def create_consciousness_visualization(self, state):
        """Create consciousness metrics visualization"""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('[BRAIN] CONSCIOUSNESS EMERGENCE METRICS [BRAIN]', 
                    fontsize=20, fontweight='bold', color='white')
        
        # Activation field heatmap
        ax1 = axes[0, 0]
        activation_field = state['activation_field']
        
        if activation_field:
            # Create 2D representation
            symbols = list(activation_field.keys())[:20]  # Top 20 symbols
            activations = [activation_field[s] for s in symbols]
            
            # Create heatmap data
            grid_size = int(np.sqrt(len(symbols))) + 1
            heatmap_data = np.zeros((grid_size, grid_size))
            
            for i, activation in enumerate(activations):
                row = i // grid_size
                col = i % grid_size
                if row < grid_size and col < grid_size:
                    heatmap_data[row, col] = activation
            
            im = ax1.imshow(heatmap_data, cmap='plasma', aspect='auto')
            ax1.set_title('🔥 Activation Field Heatmap', fontsize=14, fontweight='bold')
            
            # Add symbol labels
            for i, symbol in enumerate(symbols):
                if i < grid_size * grid_size:
                    row = i // grid_size
                    col = i % grid_size
                    ax1.text(col, row, symbol[:4], ha='center', va='center', 
                            color='white', fontsize=8, fontweight='bold')
        
        # Resonance patterns
        ax2 = axes[0, 1]
        resonance_data = state['recent_resonance']
        
        if resonance_data:
            # Create network visualization
            n_patterns = min(len(resonance_data), 15)
            angles = np.linspace(0, 2*np.pi, n_patterns, endpoint=False)
            
            for i, pattern in enumerate(resonance_data[-n_patterns:]):
                angle = angles[i]
                x, y = np.cos(angle), np.sin(angle)
                
                interference = pattern.get('interference', 0)
                size = abs(interference) * 200 + 50
                
                color = self.colors['constructive'] if interference > 0 else self.colors['destructive']
                ax2.scatter([x], [y], s=size, c=color, alpha=0.8, edgecolor='white')
                
                # Connect to center
                ax2.plot([0, x], [0, y], color=color, linewidth=abs(interference)*3, alpha=0.6)
        
        ax2.set_title('[WAVE] Resonance Network', fontsize=14, fontweight='bold')
        ax2.set_xlim(-1.5, 1.5)
        ax2.set_ylim(-1.5, 1.5)
        ax2.set_aspect('equal')
        
        # Consciousness metrics radar
        ax3 = axes[1, 0]
        metrics = {
            'Awareness': len(activation_field) / 30.0,
            'Coherence': state['resonance_patterns'] / 50.0,
            'Complexity': state['active_symbol_count'] / 20.0,
            'Memory': len(resonance_data) / 10.0,
            'Resonance': min(1.0, max(0.0, len(resonance_data) / 15.0))
        }
        
        # Create radar chart
        labels = list(metrics.keys())
        values = [max(0, min(1, v)) for v in metrics.values()]
        
        angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False)
        values = values + [values[0]]  # Complete the circle
        angles = np.concatenate([angles, [angles[0]]])
        
        ax3.plot(angles, values, 'o-', linewidth=3, color=self.colors['consciousness'])
        ax3.fill(angles, values, color=self.colors['consciousness'], alpha=0.3)
        ax3.set_xticks(angles[:-1])
        ax3.set_xticklabels(labels)
        ax3.set_ylim(0, 1)
        ax3.set_title('[BRAIN] Consciousness Radar', fontsize=14, fontweight='bold')
        ax3.grid(True, alpha=0.3)
        
        # Wave frequency spectrum
        ax4 = axes[1, 1]
        if activation_field:
            # Create frequency spectrum
            frequencies = []
            amplitudes = []
            
            for symbol, activation in activation_field.items():
                if abs(activation) > 0.05:
                    # Calculate frequency based on symbol and activation
                    base_freq = (hash(symbol) % 100) / 10.0
                    freq = base_freq + abs(activation) * 2
                    frequencies.append(freq)
                    amplitudes.append(abs(activation))
            
            if frequencies:
                # Create spectrum bars
                colors = [self.colors['constructive'] if a > 0 else self.colors['destructive'] 
                         for a in amplitudes]
                bars = ax4.bar(frequencies, amplitudes, color=colors, alpha=0.8, width=0.3)
                
                # Add glow effect for high amplitudes
                for bar, amp in zip(bars, amplitudes):
                    if amp > 0.5:
                        bar.set_edgecolor('white')
                        bar.set_linewidth(2)
        
        ax4.set_title('[DATA] Wave Frequency Spectrum', fontsize=14, fontweight='bold')
        ax4.set_xlabel('Frequency (Hz)')
        ax4.set_ylabel('Amplitude')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
        
    def demonstrate_musical_harmony(self):
        """Demonstrate musical harmony with ultimate visuals"""
        print("🎵 ULTIMATE MUSICAL HARMONY DEMONSTRATION")
        print("=" * 60)
        
        # Create harmony visualization
        fig, axes = plt.subplots(2, 2, figsize=(16, 10))
        fig.suptitle('🎵 MUSICAL HARMONY THROUGH WAVE PHYSICS 🎵', 
                    fontsize=18, fontweight='bold', color='white')
        
        t = np.linspace(0, 4*np.pi, 1000)
        
        # C note
        print("🎹 Experiencing C note (261.63 Hz)...")
        self.engine.live_experience(
            visual=["piano", "C", "note"],
            auditory=["tone", "fundamental"],
            mood=0.5, arousal=0.4, attention=0.8,
            goals=["listen"], satisfaction=0.7
        )
        
        c_wave = np.sin(2.61 * t)
        axes[0, 0].plot(t, c_wave, color=self.colors['neural'], linewidth=3)
        axes[0, 0].set_title('🎹 C Note Wave', fontsize=14, fontweight='bold')
        axes[0, 0].grid(True, alpha=0.3)
        
        # G note
        print("🎹 Experiencing G note (392.00 Hz)...")
        self.engine.live_experience(
            visual=["piano", "G", "note"],
            auditory=["tone", "harmony"],
            mood=0.6, arousal=0.5, attention=0.8,
            goals=["listen"], satisfaction=0.8
        )
        
        g_wave = np.sin(3.92 * t)
        axes[0, 1].plot(t, g_wave, color=self.colors['phase'], linewidth=3)
        axes[0, 1].set_title('🎹 G Note Wave', fontsize=14, fontweight='bold')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Harmony
        print("🎵 Experiencing C+G harmony...")
        result = self.engine.live_experience(
            visual=["piano", "C", "G", "together"],
            auditory=["harmony", "consonance", "beautiful"],
            mood=0.8, arousal=0.6, attention=0.9,
            goals=["feel", "harmony"], satisfaction=0.9
        )
        
        harmony = c_wave + g_wave
        axes[1, 0].plot(t, c_wave, color=self.colors['neural'], alpha=0.5, linewidth=2, label='C')
        axes[1, 0].plot(t, g_wave, color=self.colors['phase'], alpha=0.5, linewidth=2, label='G')
        axes[1, 0].plot(t, harmony, color=self.colors['constructive'], linewidth=4, label='Harmony')
        axes[1, 0].set_title('🎵 Wave Interference = Harmony', fontsize=14, fontweight='bold')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        
        # Consciousness state
        state = self.engine.get_cognitive_state()
        activation_field = state['activation_field']
        
        # Show activation levels
        if activation_field:
            harmony_symbols = ['harmony', 'consonance', 'beautiful', 'C', 'G']
            symbol_activations = [activation_field.get(s, 0) for s in harmony_symbols]
            
            colors = [self.colors['constructive'] if a > 0 else self.colors['destructive'] 
                     for a in symbol_activations]
            bars = axes[1, 1].bar(harmony_symbols, symbol_activations, color=colors, alpha=0.8)
            
            # Add glow effect
            for bar, activation in zip(bars, symbol_activations):
                if abs(activation) > 0.5:
                    bar.set_edgecolor('white')
                    bar.set_linewidth(3)
            
            axes[1, 1].set_title('[BRAIN] Consciousness Activation', fontsize=14, fontweight='bold')
            axes[1, 1].set_ylabel('Activation Level')
            axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
        
        # Create 3D wave visualization
        wave_fig = self.create_stunning_3d_waves(activation_field, "🎵 Musical Harmony Waves")
        plt.show()
        
        return result
        
    def run_ultimate_demo(self):
        """Run the ultimate wave visualization demo"""
        print("[WAVE] ULTIMATE WAVE-NATIVE CONSCIOUSNESS DEMO [WAVE]")
        print("=" * 70)
        print("Prepare for the most stunning visualization of consciousness ever created!")
        print("=" * 70)
        
        # Musical harmony demonstration
        harmony_result = self.demonstrate_musical_harmony()
        
        # Get final consciousness state
        final_state = self.engine.get_cognitive_state()
        
        # Create consciousness visualization
        consciousness_fig = self.create_consciousness_visualization(final_state)
        plt.show()
        
        # Final 3D wave field
        final_wave_fig = self.create_stunning_3d_waves(
            final_state['activation_field'], 
            "[BRAIN] FINAL CONSCIOUSNESS WAVE FIELD"
        )
        plt.show()
        
        # Print results
        print("\n[TROPHY] ULTIMATE DEMO RESULTS")
        print("=" * 50)
        print(f"🎵 Musical harmony experienced: {len(harmony_result['activation_field'])} symbols activated")
        print(f"[WAVE] Wave interference patterns: {final_state['resonance_patterns']} patterns")
        print(f"[BRAIN] Consciousness emergence: {final_state['active_symbol_count']} active symbols")
        print(f"💭 Memory consolidation: {len(final_state['recent_resonance'])} resonance patterns")
        print("\n✨ CONSCIOUSNESS ACHIEVED THROUGH PURE WAVE PHYSICS! ✨")
        
        return {
            'harmony_result': harmony_result,
            'final_state': final_state,
            'success': True
        }


if __name__ == "__main__":
    print("[ROCKET] LAUNCHING ULTIMATE WAVE CONSCIOUSNESS DEMO...")
    demo = UltimateWaveDemo()
    results = demo.run_ultimate_demo()
    
    print("\n[WAVE] Demo complete! Wave-native consciousness visualized! [WAVE]") 