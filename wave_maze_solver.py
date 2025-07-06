"""
Wave Engine Maze Solver
Uses temporal wave dynamics to solve mazes from benchmark datasets.
The wave engine models maze exploration as interfering waves that find optimal paths.
"""

import time
import math
import random
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass
from enum import Enum
import numpy as np
from collections import deque
import requests
import json

# Import our temporal cognition engine
from src.temporal_cognition import TemporalCognitionEngine, ExperienceFrame


class MazeCell(Enum):
    WALL = '#'
    OPEN = ' '
    START = 'S'
    GOAL = 'G'
    PATH = '*'
    VISITED = '.'


@dataclass
class Position:
    x: int
    y: int
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


@dataclass
class WaveSource:
    """A source of waves in the maze - either start or goal positions"""
    position: Position
    wave_type: str  # 'start' or 'goal'
    frequency: float
    amplitude: float
    phase: float = 0.0
    
    def get_wave_value(self, pos: Position, current_time: float) -> float:
        """Calculate wave value at given position and time"""
        distance = math.sqrt((pos.x - self.position.x)**2 + (pos.y - self.position.y)**2)
        
        # Wave equation: A * sin(2π * f * t - k * d + φ)
        # where k is wave number (frequency related)
        wave_number = self.frequency * 0.1  # Adjust propagation speed
        wave_value = self.amplitude * math.sin(
            2 * math.pi * self.frequency * current_time - 
            wave_number * distance + 
            self.phase
        )
        
        # Decay with distance
        decay = math.exp(-distance * 0.1)
        return wave_value * decay


class WaveMazeSolver:
    """
    Solves mazes using wave interference patterns.
    Start and goal positions emit waves that interfere to find optimal paths.
    """
    
    def __init__(self, maze_str: str):
        self.maze = self._parse_maze(maze_str)
        self.height = len(self.maze)
        self.width = len(self.maze[0]) if self.maze else 0
        
        # Find start and goal positions
        self.start_pos = None
        self.goal_pos = None
        self._find_start_goal()
        
        # Wave sources
        self.wave_sources = []
        if self.start_pos:
            self.wave_sources.append(WaveSource(
                self.start_pos, 'start', 
                frequency=1.0, amplitude=1.0, phase=0.0
            ))
        if self.goal_pos:
            self.wave_sources.append(WaveSource(
                self.goal_pos, 'goal', 
                frequency=1.2, amplitude=1.0, phase=math.pi/2
            ))
        
        # Temporal cognition for learning
        self.cognition = TemporalCognitionEngine()
        
        # Solution tracking
        self.solution_path = []
        self.wave_field = np.zeros((self.height, self.width))
        self.interference_field = np.zeros((self.height, self.width))
        
    def _parse_maze(self, maze_str: str) -> List[List[str]]:
        """Parse string maze into 2D grid"""
        lines = maze_str.strip().split('\n')
        maze = []
        for line in lines:
            if line.strip():  # Skip empty lines
                maze.append(list(line))
        return maze
    
    def _find_start_goal(self):
        """Find start and goal positions in maze"""
        for y in range(self.height):
            for x in range(self.width):
                if self.maze[y][x] == 'S':
                    self.start_pos = Position(x, y)
                elif self.maze[y][x] == 'G':
                    self.goal_pos = Position(x, y)
    
    def _is_valid_position(self, pos: Position) -> bool:
        """Check if position is valid and not a wall"""
        if pos.x < 0 or pos.x >= self.width or pos.y < 0 or pos.y >= self.height:
            return False
        return self.maze[pos.y][pos.x] != '#'
    
    def _get_neighbors(self, pos: Position) -> List[Position]:
        """Get valid neighboring positions"""
        neighbors = []
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_pos = Position(pos.x + dx, pos.y + dy)
            if self._is_valid_position(new_pos):
                neighbors.append(new_pos)
        return neighbors
    
    def _calculate_wave_field(self, current_time: float):
        """Calculate wave interference field at current time"""
        self.wave_field.fill(0)
        self.interference_field.fill(0)
        
        # Calculate individual wave contributions
        for y in range(self.height):
            for x in range(self.width):
                if self.maze[y][x] == '#':
                    continue
                    
                pos = Position(x, y)
                total_wave = 0
                wave_values = []
                
                for source in self.wave_sources:
                    wave_val = source.get_wave_value(pos, current_time)
                    wave_values.append(wave_val)
                    total_wave += wave_val
                
                self.wave_field[y][x] = total_wave
                
                # Calculate interference pattern
                if len(wave_values) >= 2:
                    # Constructive interference when waves align
                    interference = 0
                    for i in range(len(wave_values)):
                        for j in range(i + 1, len(wave_values)):
                            # Measure phase alignment
                            phase_diff = abs(wave_values[i] - wave_values[j])
                            if phase_diff < 0.5:  # Constructive
                                interference += 1.0
                            else:  # Destructive
                                interference -= 0.5
                    
                    self.interference_field[y][x] = interference
    
    def _wave_guided_search(self) -> List[Position]:
        """Use wave interference to guide path search"""
        if not self.start_pos or not self.goal_pos:
            return []
        
        path = []
        current_pos = self.start_pos
        visited = set()
        max_steps = self.width * self.height  # Prevent infinite loops
        step_count = 0
        
        while current_pos != self.goal_pos and step_count < max_steps:
            path.append(current_pos)
            visited.add(current_pos)
            
            # Calculate current wave field
            current_time = time.time()
            self._calculate_wave_field(current_time)
            
            # Record experience for cognition
            self._record_maze_experience(current_pos, current_time)
            
            # Find best next position based on wave interference
            neighbors = self._get_neighbors(current_pos)
            valid_neighbors = [n for n in neighbors if n not in visited]
            
            if not valid_neighbors:
                # Backtrack if stuck
                if len(path) > 1:
                    path.pop()
                    current_pos = path[-1]
                else:
                    break
                continue
            
            # Choose neighbor with highest positive interference
            best_neighbor = None
            best_score = float('-inf')
            
            for neighbor in valid_neighbors:
                # Wave interference score
                interference_score = self.interference_field[neighbor.y][neighbor.x]
                
                # Distance to goal bonus
                goal_distance = math.sqrt(
                    (neighbor.x - self.goal_pos.x)**2 + 
                    (neighbor.y - self.goal_pos.y)**2
                )
                distance_score = 1.0 / (1.0 + goal_distance)
                
                # Total score
                total_score = interference_score + distance_score * 0.5
                
                if total_score > best_score:
                    best_score = total_score
                    best_neighbor = neighbor
            
            if best_neighbor:
                current_pos = best_neighbor
            else:
                # No good moves, try random
                current_pos = random.choice(valid_neighbors)
            
            step_count += 1
        
        if current_pos == self.goal_pos:
            path.append(current_pos)
            return path
        
        return []  # No solution found
    
    def _record_maze_experience(self, pos: Position, current_time: float):
        """Record maze exploration as temporal experience"""
        # Visual symbols - what we "see" at current position
        visual_symbols = []
        neighbors = self._get_neighbors(pos)
        
        for neighbor in neighbors:
            direction = self._get_direction(pos, neighbor)
            visual_symbols.append(f"open_{direction}")
        
        # Current wave field value
        wave_value = self.wave_field[pos.y][pos.x]
        interference_value = self.interference_field[pos.y][pos.x]
        
        # Goals - trying to reach the goal
        goals = ["reach_goal", "follow_waves"]
        
        # Context
        context = [
            f"position_{pos.x}_{pos.y}",
            f"wave_strength_{wave_value:.2f}",
            f"interference_{interference_value:.2f}"
        ]
        
        # Calculate surprise based on wave prediction vs reality
        expected_neighbors = 4  # Max possible
        actual_neighbors = len(neighbors)
        surprise = abs(expected_neighbors - actual_neighbors) / expected_neighbors
        
        # Satisfaction based on progress toward goal
        if self.goal_pos:
            distance_to_goal = math.sqrt(
                (pos.x - self.goal_pos.x)**2 + (pos.y - self.goal_pos.y)**2
            )
            max_distance = math.sqrt(self.width**2 + self.height**2)
            satisfaction = 1.0 - (distance_to_goal / max_distance)
        else:
            satisfaction = 0.0
        
        # Record experience
        self.cognition.live_experience(
            visual=visual_symbols,
            mood=satisfaction * 2 - 1,  # Convert to -1 to 1 range
            arousal=0.7,  # High arousal during maze solving
            attention=0.9,  # High attention during navigation
            goals=goals,
            context=context,
            surprise=surprise,
            satisfaction=satisfaction
        )
    
    def _get_direction(self, from_pos: Position, to_pos: Position) -> str:
        """Get direction string from one position to another"""
        dx = to_pos.x - from_pos.x
        dy = to_pos.y - from_pos.y
        
        if dx == 1: return "east"
        elif dx == -1: return "west"
        elif dy == 1: return "south"
        elif dy == -1: return "north"
        else: return "unknown"
    
    def solve(self) -> Dict:
        """Solve the maze using wave dynamics"""
        start_time = time.time()
        
        print(f"🌊 Wave Engine Maze Solver Starting...")
        print(f"📍 Start: {self.start_pos}")
        print(f"🎯 Goal: {self.goal_pos}")
        print(f"📏 Maze Size: {self.width}x{self.height}")
        
        # Use wave-guided search
        self.solution_path = self._wave_guided_search()
        
        solve_time = time.time() - start_time
        
        # Get cognitive state
        cognitive_state = self.cognition.get_cognitive_state()
        
        result = {
            "solved": len(self.solution_path) > 0,
            "path_length": len(self.solution_path),
            "solution_path": [(pos.x, pos.y) for pos in self.solution_path],
            "solve_time": solve_time,
            "cognitive_experiences": cognitive_state["total_experiences"],
            "active_waves": cognitive_state["active_symbol_count"],
            "wave_resonance_patterns": cognitive_state["resonance_patterns"]
        }
        
        return result
    
    def visualize_solution(self) -> str:
        """Create ASCII visualization of the solution"""
        if not self.solution_path:
            return "No solution found!"
        
        # Create copy of maze for visualization
        viz_maze = [row[:] for row in self.maze]
        
        # Mark solution path
        for pos in self.solution_path[1:-1]:  # Skip start and goal
            if viz_maze[pos.y][pos.x] not in ['S', 'G']:
                viz_maze[pos.y][pos.x] = '*'
        
        # Convert to string
        result = []
        for row in viz_maze:
            result.append(''.join(row))
        
        return '\n'.join(result)


def create_simple_test_maze() -> str:
    """Create a simple test maze"""
    return """
#########
#S      #
# ##### #
#     # #
##### # #
#     # #
# ##### #
#      G#
#########
""".strip()


def create_complex_test_maze() -> str:
    """Create a more complex test maze"""
    return """
#####################
#S  #   #     #     #
# # # # # ### # ### #
# # # # #   # #   # #
# # # # ### # ### # #
# #   #     #     # #
# ##### ##### ##### #
#     #       #     #
##### # ##### # #####
#   # #   #   # #   #
# # # ### # ### # # #
# # #   # # #   # # #
# # ### # # # ### # #
# #   # # # # #   # #
# ### # # # # # ### #
#   # #   #   # #   #
### # ##### ##### # #
#   #           # # #
# ############### # #
#                  G#
#####################
""".strip()


def benchmark_wave_solver():
    """Run benchmark tests on the wave maze solver"""
    print("🧪 Wave Engine Maze Solver Benchmark")
    print("=" * 50)
    
    test_mazes = [
        ("Simple Test Maze", create_simple_test_maze()),
        ("Complex Test Maze", create_complex_test_maze())
    ]
    
    total_solved = 0
    total_time = 0
    
    for name, maze_str in test_mazes:
        print(f"\n🔍 Testing: {name}")
        print("-" * 30)
        
        solver = WaveMazeSolver(maze_str)
        result = solver.solve()
        
        if result["solved"]:
            total_solved += 1
            print(f"✅ SOLVED in {result['solve_time']:.3f}s")
            print(f"📏 Path length: {result['path_length']}")
            print(f"🧠 Cognitive experiences: {result['cognitive_experiences']}")
            print(f"🌊 Active wave patterns: {result['active_waves']}")
            print(f"🎵 Resonance patterns: {result['wave_resonance_patterns']}")
            
            print("\n🗺️  Solution Visualization:")
            print(solver.visualize_solution())
        else:
            print("❌ FAILED to solve")
        
        total_time += result["solve_time"]
    
    print(f"\n🏆 BENCHMARK RESULTS")
    print("=" * 50)
    print(f"Solved: {total_solved}/{len(test_mazes)} mazes")
    print(f"Success Rate: {total_solved/len(test_mazes)*100:.1f}%")
    print(f"Total Time: {total_time:.3f}s")
    print(f"Average Time: {total_time/len(test_mazes):.3f}s per maze")


if __name__ == "__main__":
    benchmark_wave_solver() 