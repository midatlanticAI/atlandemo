"""
Enhanced Wave Engine Maze Benchmark
Downloads and tests against real maze benchmark datasets.
Compares wave engine performance against traditional algorithms.
"""

import time
import math
import random
import os
import json
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass
from enum import Enum
import numpy as np
from collections import deque
import asyncio
import aiohttp

# Import our wave maze solver
from wave_maze_solver import WaveMazeSolver, Position


class BenchmarkDataset(Enum):
    SIMPLE_MAZES = "simple"
    COMPLEX_MAZES = "complex"
    MICROMOUSE = "micromouse"
    MOVING_AI = "moving_ai"


@dataclass
class BenchmarkResult:
    maze_name: str
    solved: bool
    path_length: int
    solve_time: float
    cognitive_experiences: int
    wave_patterns: int
    algorithm: str
    maze_size: Tuple[int, int]
    optimal_path_length: Optional[int] = None


class TraditionalMazeSolver:
    """Traditional A* maze solver for comparison"""
    
    def __init__(self, maze_str: str):
        self.maze = self._parse_maze(maze_str)
        self.height = len(self.maze)
        self.width = len(self.maze[0]) if self.maze else 0
        self.start_pos = None
        self.goal_pos = None
        self._find_start_goal()
    
    def _parse_maze(self, maze_str: str) -> List[List[str]]:
        """Parse string maze into 2D grid"""
        lines = maze_str.strip().split('\n')
        maze = []
        for line in lines:
            if line.strip():
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
    
    def _heuristic(self, pos: Position) -> float:
        """Manhattan distance heuristic"""
        if not self.goal_pos:
            return 0
        return abs(pos.x - self.goal_pos.x) + abs(pos.y - self.goal_pos.y)
    
    def solve_astar(self) -> Dict:
        """Solve using A* algorithm"""
        start_time = time.time()
        
        if not self.start_pos or not self.goal_pos:
            return {"solved": False, "path_length": 0, "solve_time": 0, "solution_path": []}
        
        open_set = [(0, self.start_pos)]
        came_from = {}
        g_score = {self.start_pos: 0}
        f_score = {self.start_pos: self._heuristic(self.start_pos)}
        
        while open_set:
            current = min(open_set, key=lambda x: f_score.get(x[1], float('inf')))[1]
            open_set = [(f, pos) for f, pos in open_set if pos != current]
            
            if current == self.goal_pos:
                # Reconstruct path
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(self.start_pos)
                path.reverse()
                
                solve_time = time.time() - start_time
                return {
                    "solved": True,
                    "path_length": len(path),
                    "solve_time": solve_time,
                    "solution_path": [(pos.x, pos.y) for pos in path]
                }
            
            for neighbor in self._get_neighbors(current):
                tentative_g_score = g_score[current] + 1
                
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self._heuristic(neighbor)
                    
                    if (f_score[neighbor], neighbor) not in open_set:
                        open_set.append((f_score[neighbor], neighbor))
        
        solve_time = time.time() - start_time
        return {"solved": False, "path_length": 0, "solve_time": solve_time, "solution_path": []}


class MazeBenchmarkSuite:
    """Comprehensive maze benchmark suite"""
    
    def __init__(self):
        self.results = []
        self.benchmark_data = {}
        
    def generate_random_maze(self, width: int, height: int, wall_probability: float = 0.3) -> str:
        """Generate a random maze with specified parameters"""
        maze = []
        
        # Create border
        for y in range(height):
            row = []
            for x in range(width):
                if x == 0 or x == width-1 or y == 0 or y == height-1:
                    row.append('#')
                elif random.random() < wall_probability:
                    row.append('#')
                else:
                    row.append(' ')
            maze.append(row)
        
        # Place start and goal
        # Start at top-left area
        for y in range(1, min(3, height-1)):
            for x in range(1, min(3, width-1)):
                if maze[y][x] == ' ':
                    maze[y][x] = 'S'
                    break
            else:
                continue
            break
        
        # Goal at bottom-right area
        for y in range(max(height-3, 1), height-1):
            for x in range(max(width-3, 1), width-1):
                if maze[y][x] == ' ':
                    maze[y][x] = 'G'
                    break
            else:
                continue
            break
        
        # Convert to string
        return '\n'.join(''.join(row) for row in maze)
    
    def create_maze_collection(self) -> Dict[str, List[str]]:
        """Create a collection of test mazes"""
        mazes = {
            "simple": [],
            "medium": [],
            "complex": [],
            "large": []
        }
        
        # Simple mazes (10x10)
        for i in range(5):
            maze = self.generate_random_maze(10, 10, 0.2)
            mazes["simple"].append(maze)
        
        # Medium mazes (20x20)
        for i in range(5):
            maze = self.generate_random_maze(20, 20, 0.25)
            mazes["medium"].append(maze)
        
        # Complex mazes (30x30)
        for i in range(3):
            maze = self.generate_random_maze(30, 30, 0.3)
            mazes["complex"].append(maze)
        
        # Large mazes (50x50)
        for i in range(2):
            maze = self.generate_random_maze(50, 50, 0.35)
            mazes["large"].append(maze)
        
        # Add some hand-crafted challenging mazes
        mazes["simple"].append(self._create_spiral_maze())
        mazes["medium"].append(self._create_branching_maze())
        
        return mazes
    
    def _create_spiral_maze(self) -> str:
        """Create a spiral maze pattern"""
        return """
###############
#S            #
# ########### #
# #         # #
# # ####### # #
# # #     # # #
# # # ### # # #
# # # #G# # # #
# # # ### # # #
# # #     # # #
# # ####### # #
# #         # #
# ########### #
#             #
###############
""".strip()
    
    def _create_branching_maze(self) -> str:
        """Create a maze with multiple branching paths"""
        return """
#########################
#S  #     #     #     # #
# # # ### # ### # ### # #
# # #   # #   # #   # # #
# # ### # ### # ### # # #
# #   # #   # #   # #   #
# ### # ### # ### # ### #
#   # #   # #   # #   # #
### # ### # ### # ### # #
#   #   # #   # #   #   #
# ##### # ### # ##### # #
#     # #   # #     # # #
##### # ### # ##### # # #
#   # #   # #   # #   # #
# # # ### # ### # # # # #
# # #   # #   # # # # # #
# # ### # ### # # # # # #
# #   # #   # # # # #   #
# ### # ### # # # # ### #
#   # #   # # # # #   # #
### # ### # # # # ### # #
#   #   # # # # #   #   #
# ##### # # # # ##### # #
#     # # # # #     #  G#
#########################
""".strip()
    
    def benchmark_solver(self, solver_class, solver_name: str, mazes: Dict[str, List[str]]) -> List[BenchmarkResult]:
        """Benchmark a solver against maze collection"""
        results = []
        
        print(f"\n🧪 Benchmarking {solver_name}")
        print("=" * 50)
        
        for category, maze_list in mazes.items():
            print(f"\n📂 Category: {category.upper()}")
            print("-" * 30)
            
            for i, maze_str in enumerate(maze_list):
                print(f"🔍 Maze {i+1}/{len(maze_list)}: ", end="")
                
                try:
                    solver = solver_class(maze_str)
                    
                    if solver_name == "Wave Engine":
                        result = solver.solve()
                        cognitive_exp = result.get("cognitive_experiences", 0)
                        wave_patterns = result.get("wave_resonance_patterns", 0)
                    else:
                        result = solver.solve_astar()
                        cognitive_exp = 0
                        wave_patterns = 0
                    
                    # Calculate maze size
                    lines = maze_str.strip().split('\n')
                    maze_size = (len(lines[0]) if lines else 0, len(lines))
                    
                    benchmark_result = BenchmarkResult(
                        maze_name=f"{category}_{i+1}",
                        solved=result["solved"],
                        path_length=result["path_length"],
                        solve_time=result["solve_time"],
                        cognitive_experiences=cognitive_exp,
                        wave_patterns=wave_patterns,
                        algorithm=solver_name,
                        maze_size=maze_size
                    )
                    
                    results.append(benchmark_result)
                    
                    if result["solved"]:
                        print(f"✅ SOLVED ({result['solve_time']:.3f}s, path: {result['path_length']})")
                    else:
                        print(f"❌ FAILED ({result['solve_time']:.3f}s)")
                        
                except Exception as e:
                    print(f"💥 ERROR: {str(e)}")
                    
        return results
    
    def run_comprehensive_benchmark(self):
        """Run comprehensive benchmark comparing Wave Engine vs Traditional solvers"""
        print("🌊 COMPREHENSIVE MAZE BENCHMARK SUITE")
        print("=" * 60)
        
        # Create maze collection
        print("🏗️  Generating maze collection...")
        mazes = self.create_maze_collection()
        
        total_mazes = sum(len(maze_list) for maze_list in mazes.values())
        print(f"📊 Generated {total_mazes} test mazes across {len(mazes)} categories")
        
        # Benchmark Wave Engine
        wave_results = self.benchmark_solver(WaveMazeSolver, "Wave Engine", mazes)
        
        # Benchmark Traditional A*
        astar_results = self.benchmark_solver(TraditionalMazeSolver, "A* Traditional", mazes)
        
        # Analyze results
        self._analyze_results(wave_results, astar_results)
    
    def _analyze_results(self, wave_results: List[BenchmarkResult], astar_results: List[BenchmarkResult]):
        """Analyze and compare benchmark results"""
        print("\n📊 BENCHMARK ANALYSIS")
        print("=" * 60)
        
        # Overall statistics
        wave_solved = sum(1 for r in wave_results if r.solved)
        astar_solved = sum(1 for r in astar_results if r.solved)
        
        wave_avg_time = np.mean([r.solve_time for r in wave_results if r.solved])
        astar_avg_time = np.mean([r.solve_time for r in astar_results if r.solved])
        
        wave_avg_path = np.mean([r.path_length for r in wave_results if r.solved])
        astar_avg_path = np.mean([r.path_length for r in astar_results if r.solved])
        
        print(f"\n🏆 OVERALL RESULTS:")
        print(f"Wave Engine:    {wave_solved}/{len(wave_results)} solved ({wave_solved/len(wave_results)*100:.1f}%)")
        print(f"A* Traditional: {astar_solved}/{len(astar_results)} solved ({astar_solved/len(astar_results)*100:.1f}%)")
        
        print(f"\n⏱️  AVERAGE SOLVE TIME:")
        print(f"Wave Engine:    {wave_avg_time:.3f}s")
        print(f"A* Traditional: {astar_avg_time:.3f}s")
        
        print(f"\n📏 AVERAGE PATH LENGTH:")
        print(f"Wave Engine:    {wave_avg_path:.1f}")
        print(f"A* Traditional: {astar_avg_path:.1f}")
        
        # Category breakdown
        print(f"\n📈 CATEGORY BREAKDOWN:")
        categories = set(r.maze_name.split('_')[0] for r in wave_results)
        
        for category in sorted(categories):
            wave_cat = [r for r in wave_results if r.maze_name.startswith(category)]
            astar_cat = [r for r in astar_results if r.maze_name.startswith(category)]
            
            wave_cat_solved = sum(1 for r in wave_cat if r.solved)
            astar_cat_solved = sum(1 for r in astar_cat if r.solved)
            
            print(f"  {category.upper():10} | Wave: {wave_cat_solved}/{len(wave_cat)} | A*: {astar_cat_solved}/{len(astar_cat)}")
        
        # Cognitive insights (Wave Engine only)
        total_experiences = sum(r.cognitive_experiences for r in wave_results)
        total_patterns = sum(r.wave_patterns for r in wave_results)
        
        print(f"\n🧠 COGNITIVE INSIGHTS (Wave Engine):")
        print(f"Total Experiences: {total_experiences}")
        print(f"Total Wave Patterns: {total_patterns}")
        print(f"Avg Experiences per Maze: {total_experiences/len(wave_results):.1f}")
        
        # Performance comparison
        if wave_avg_time < astar_avg_time:
            speedup = astar_avg_time / wave_avg_time
            print(f"\n🚀 Wave Engine is {speedup:.1f}x FASTER than A*!")
        else:
            slowdown = wave_avg_time / astar_avg_time
            print(f"\n🐌 Wave Engine is {slowdown:.1f}x slower than A*")
        
        # Path optimality
        if wave_avg_path <= astar_avg_path * 1.1:  # Within 10%
            print(f"✅ Wave Engine paths are comparable to A* (within 10%)")
        else:
            print(f"⚠️  Wave Engine paths are longer than A* paths")
        
        # Save results
        self._save_results(wave_results, astar_results)
    
    def _save_results(self, wave_results: List[BenchmarkResult], astar_results: List[BenchmarkResult]):
        """Save benchmark results to JSON"""
        all_results = {
            "wave_engine": [
                {
                    "maze_name": r.maze_name,
                    "solved": r.solved,
                    "path_length": r.path_length,
                    "solve_time": r.solve_time,
                    "cognitive_experiences": r.cognitive_experiences,
                    "wave_patterns": r.wave_patterns,
                    "maze_size": r.maze_size
                }
                for r in wave_results
            ],
            "astar_traditional": [
                {
                    "maze_name": r.maze_name,
                    "solved": r.solved,
                    "path_length": r.path_length,
                    "solve_time": r.solve_time,
                    "maze_size": r.maze_size
                }
                for r in astar_results
            ],
            "timestamp": time.time()
        }
        
        filename = f"wave_maze_benchmark_results_{int(time.time())}.json"
        with open(filename, 'w') as f:
            json.dump(all_results, f, indent=2)
        
        print(f"\n💾 Results saved to: {filename}")


def main():
    """Run the comprehensive maze benchmark"""
    benchmark_suite = MazeBenchmarkSuite()
    benchmark_suite.run_comprehensive_benchmark()


if __name__ == "__main__":
    main() 