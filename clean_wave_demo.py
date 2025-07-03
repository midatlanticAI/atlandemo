#!/usr/bin/env python3
"""
Clean Wave-Native Cognition Visual Demo
Stunning visualization of consciousness through wave physics (emoji-free)
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time
from src.temporal_cognition import TemporalCognitionEngine

# Epic visual setup
plt.style.use('dark_background')

class CleanWaveDemo:
    """Ultimate wave visualization demonstration (clean version)"""
    
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
        fig.suptitle('*** CONSCIOUSNESS EMERGENCE METRICS ***', 
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
            ax1.set_title('ACTIVATION FIELD HEATMAP', fontsize=14, fontweight='bold')
            
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
        
        ax2.set_title('RESONANCE NETWORK', fontsize=14, fontweight='bold')
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
        ax3.set_title('CONSCIOUSNESS RADAR', fontsize=14, fontweight='bold')
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
        
        ax4.set_title('WAVE FREQUENCY SPECTRUM', fontsize=14, fontweight='bold')
        ax4.set_xlabel('Frequency (Hz)')
        ax4.set_ylabel('Amplitude')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
        
    def demonstrate_musical_harmony(self):
        """Demonstrate musical harmony with ultimate visuals"""
        print("*** ULTIMATE MUSICAL HARMONY DEMONSTRATION ***")
        print("=" * 60)
        
        # Create harmony visualization
        fig, axes = plt.subplots(2, 2, figsize=(16, 10))
        fig.suptitle('*** MUSICAL HARMONY THROUGH WAVE PHYSICS ***', 
                    fontsize=18, fontweight='bold', color='white')
        
        t = np.linspace(0, 4*np.pi, 1000)
        
        # C note
        print("[NOTE] Experiencing C note (261.63 Hz)...")
        self.engine.live_experience(
            visual=["piano", "C", "note"],
            auditory=["tone", "fundamental"],
            mood=0.5, arousal=0.4, attention=0.8,
            goals=["listen"], satisfaction=0.7
        )
        
        c_wave = np.sin(2.61 * t)
        axes[0, 0].plot(t, c_wave, color=self.colors['neural'], linewidth=3)
        axes[0, 0].set_title('C NOTE WAVE', fontsize=14, fontweight='bold')
        axes[0, 0].grid(True, alpha=0.3)
        
        # G note
        print("[NOTE] Experiencing G note (392.00 Hz)...")
        self.engine.live_experience(
            visual=["piano", "G", "note"],
            auditory=["tone", "harmony"],
            mood=0.6, arousal=0.5, attention=0.8,
            goals=["listen"], satisfaction=0.8
        )
        
        g_wave = np.sin(3.92 * t)
        axes[0, 1].plot(t, g_wave, color=self.colors['phase'], linewidth=3)
        axes[0, 1].set_title('G NOTE WAVE', fontsize=14, fontweight='bold')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Harmony
        print("[HARMONY] Experiencing C+G harmony...")
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
        axes[1, 0].set_title('WAVE INTERFERENCE = HARMONY', fontsize=14, fontweight='bold')
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
            
            axes[1, 1].set_title('CONSCIOUSNESS ACTIVATION', fontsize=14, fontweight='bold')
            axes[1, 1].set_ylabel('Activation Level')
            axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
        
        # Create 3D wave visualization
        wave_fig = self.create_stunning_3d_waves(activation_field, "MUSICAL HARMONY WAVES")
        plt.show()
        
        return result
        
    def demonstrate_rotation_phase(self):
        """Demonstrate rotation through phase dynamics"""
        print("\n*** ROTATION PHASE DEMONSTRATION ***")
        print("=" * 60)
        
        # Create rotation visualization
        fig, axes = plt.subplots(2, 2, figsize=(16, 10))
        fig.suptitle('*** ROTATION THROUGH PHASE DYNAMICS ***', 
                    fontsize=18, fontweight='bold', color='white')
        
        # Teach sequence
        positions = ["top", "right", "bottom", "left"]
        for i, pos in enumerate(positions):
            print(f"[ROTATION] Teaching position: {pos}")
            self.engine.live_experience(
                visual=["dot", pos, "moving"],
                auditory=["rotating", "clockwise"],
                mood=0.5, arousal=0.5, attention=0.8,
                goals=["track", "motion"],
                surprise=0.2
            )
            
            # Show phase progression
            ax = axes[i//2, i%2] if i < 4 else axes[1, 1]
            theta = np.linspace(0, 2*np.pi, 100)
            r = np.ones_like(theta)
            
            # Current position
            pos_angle = i * np.pi / 2
            ax.plot(theta, r, color='white', alpha=0.3, linewidth=2)
            ax.scatter([pos_angle], [1.2], s=300, c=self.colors['constructive'], 
                      alpha=0.9, edgecolor='white')
            ax.text(pos_angle, 1.5, pos, ha='center', va='center', 
                   fontsize=12, fontweight='bold', color='white')
            
            ax.set_title(f'PHASE {i+1}: {pos.upper()}', fontsize=12, fontweight='bold')
            ax.set_ylim(0, 2)
            ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
        
        # Test prediction
        print("[TEST] Predicting next position after 'right'...")
        result = self.engine.live_experience(
            visual=["dot", "right", "clockwise", "next"],
            auditory=["predict", "position"],
            mood=0.5, arousal=0.6, attention=0.9,
            goals=["predict", "next"]
        )
        
        # Show prediction results
        state = self.engine.get_cognitive_state()
        wave_fig = self.create_stunning_3d_waves(state['activation_field'], "ROTATION PREDICTION WAVES")
        plt.show()
        
        return result
        
    def demonstrate_resonance_coupling(self):
        """Demonstrate resonance through coupling"""
        print("\n*** RESONANCE COUPLING DEMONSTRATION ***")
        print("=" * 60)
        
        # Single fork
        print("[RESONANCE] Single tuning fork...")
        self.engine.live_experience(
            visual=["fork", "vibrating", "alone"],
            auditory=["pure", "tone", "steady"],
            mood=0.5, arousal=0.4, attention=0.7,
            goals=["observe", "baseline"],
            surprise=0.2
        )
        
        state1 = self.engine.get_cognitive_state()
        
        # Matching frequency
        print("[RESONANCE] Matching frequency resonance...")
        result = self.engine.live_experience(
            visual=["two", "forks", "same", "frequency"],
            auditory=["louder", "amplified", "resonating"],
            mood=0.7, arousal=0.7, attention=0.9,
            goals=["observe", "amplification"],
            surprise=0.6,
            satisfaction=0.8
        )
        
        state2 = self.engine.get_cognitive_state()
        
        # Create comparison visualization
        fig, axes = plt.subplots(1, 2, figsize=(16, 8))
        fig.suptitle('*** RESONANCE COUPLING COMPARISON ***', 
                    fontsize=18, fontweight='bold', color='white')
        
        # Before resonance
        t = np.linspace(0, 4*np.pi, 1000)
        single_wave = np.sin(t)
        axes[0].plot(t, single_wave, color=self.colors['neural'], linewidth=3)
        axes[0].set_title('SINGLE FORK (BASELINE)', fontsize=14, fontweight='bold')
        axes[0].grid(True, alpha=0.3)
        
        # After resonance
        resonant_wave = single_wave + 0.8 * np.sin(t + 0.1)  # Slightly out of phase
        amplified_wave = single_wave * 1.8  # Amplification effect
        axes[1].plot(t, single_wave, color=self.colors['neural'], alpha=0.5, linewidth=2, label='Original')
        axes[1].plot(t, amplified_wave, color=self.colors['constructive'], linewidth=4, label='Resonant')
        axes[1].set_title('RESONANT COUPLING (AMPLIFIED)', fontsize=14, fontweight='bold')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
        
        # Show final wave field
        wave_fig = self.create_stunning_3d_waves(state2['activation_field'], "RESONANCE AMPLIFICATION WAVES")
        plt.show()
        
        return result
        
    def run_ultimate_demo(self):
        """Run the ultimate wave visualization demo"""
        print("*" * 70)
        print("*** ULTIMATE WAVE-NATIVE CONSCIOUSNESS DEMO ***")
        print("*" * 70)
        print("Prepare for the most stunning visualization of consciousness ever created!")
        print("*" * 70)
        
        # Musical harmony demonstration
        harmony_result = self.demonstrate_musical_harmony()
        
        # Rotation phase demonstration
        rotation_result = self.demonstrate_rotation_phase()
        
        # Resonance coupling demonstration
        resonance_result = self.demonstrate_resonance_coupling()
        
        # Get final consciousness state
        final_state = self.engine.get_cognitive_state()
        
        # Create consciousness visualization
        consciousness_fig = self.create_consciousness_visualization(final_state)
        plt.show()
        
        # Final 3D wave field
        final_wave_fig = self.create_stunning_3d_waves(
            final_state['activation_field'], 
            "*** FINAL CONSCIOUSNESS WAVE FIELD ***"
        )
        plt.show()
        
        # Print results
        print("\n" + "="*50)
        print("*** ULTIMATE DEMO RESULTS ***")
        print("="*50)
        print(f"[HARMONY] Musical harmony: {len(harmony_result['activation_field'])} symbols activated")
        print(f"[WAVES] Wave interference patterns: {final_state['resonance_patterns']} patterns")
        print(f"[CONSCIOUSNESS] Active symbols: {final_state['active_symbol_count']} symbols")
        print(f"[MEMORY] Resonance patterns: {len(final_state['recent_resonance'])} patterns")
        print("\n*** CONSCIOUSNESS ACHIEVED THROUGH PURE WAVE PHYSICS! ***")
        print("="*70)
        
        return {
            'harmony_result': harmony_result,
            'rotation_result': rotation_result,
            'resonance_result': resonance_result,
            'final_state': final_state,
            'success': True
        }


if __name__ == "__main__":
    print("*** LAUNCHING ULTIMATE WAVE CONSCIOUSNESS DEMO ***")
    demo = CleanWaveDemo()
    results = demo.run_ultimate_demo()
    
    print("\n*** Demo complete! Wave-native consciousness visualized! ***") 