"""
Wave Engine Bitcoin Mining Experiment
Theoretical exploration of using wave interference patterns for cryptocurrency mining.
This is more of a thought experiment than practical mining!
"""

import hashlib
import time
import random
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import numpy as np
from collections import deque

# Import our temporal cognition engine
from src.temporal_cognition import TemporalCognitionEngine, ExperienceFrame


@dataclass
class BitcoinBlock:
    """Simplified Bitcoin block structure"""
    index: int
    timestamp: float
    transactions: List[str]
    previous_hash: str
    nonce: int = 0
    target_difficulty: int = 4  # Number of leading zeros required
    
    def get_hash(self) -> str:
        """Calculate SHA-256 hash of block"""
        block_string = f"{self.index}{self.timestamp}{self.transactions}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def is_valid_proof(self) -> bool:
        """Check if current nonce produces valid proof of work"""
        hash_result = self.get_hash()
        return hash_result.startswith('0' * self.target_difficulty)
    
    def copy(self):
        """Create a copy of this block"""
        return BitcoinBlock(
            index=self.index,
            timestamp=self.timestamp,
            transactions=self.transactions.copy(),
            previous_hash=self.previous_hash,
            nonce=self.nonce,
            target_difficulty=self.target_difficulty
        )


class WaveHashMiner:
    """
    Experimental Bitcoin miner using wave interference patterns
    Instead of brute force, uses wave resonance to guide search
    """
    
    def __init__(self, difficulty: int = 4):
        self.difficulty = difficulty
        self.cognition = TemporalCognitionEngine()
        self.hash_wave_field = np.zeros(256)  # For 256-bit hashes
        self.nonce_resonance_map = {}
        self.best_candidates = deque(maxlen=100)
        
    def _hash_to_wave_pattern(self, hash_str: str) -> np.ndarray:
        """Convert hash string to wave pattern"""
        wave_pattern = np.zeros(256)
        
        # Convert hex hash to binary representation
        for i, char in enumerate(hash_str):
            if i >= 64:  # SHA-256 is 64 hex chars
                break
            hex_val = int(char, 16)
            # Create wave pattern based on hex value
            for bit in range(4):
                bit_val = (hex_val >> bit) & 1
                wave_pattern[i * 4 + bit] = bit_val
        
        return wave_pattern
    
    def _create_nonce_wave_sources(self, nonce: int) -> List[float]:
        """Create wave sources based on nonce value"""
        sources = []
        nonce_str = str(nonce)
        
        for i, digit in enumerate(nonce_str):
            digit_val = int(digit)
            # Create wave with frequency based on digit and position
            frequency = (digit_val + 1) * 0.1 * (i + 1)
            amplitude = digit_val / 9.0  # Normalize to 0-1
            sources.append(frequency * amplitude)
        
        return sources
    
    def _calculate_wave_interference(self, block: BitcoinBlock, nonce: int) -> float:
        """Calculate wave interference for given nonce"""
        # Get current hash
        block.nonce = nonce
        current_hash = block.get_hash()
        
        # Convert to wave pattern
        hash_wave = self._hash_to_wave_pattern(current_hash)
        
        # Create target wave pattern (lots of zeros at start)
        target_wave = np.zeros(256)
        target_wave[:self.difficulty * 4] = 1.0  # Want zeros here
        
        # Calculate interference between actual and target
        interference = np.dot(hash_wave, target_wave)
        
        # Lower interference means closer to target (more zeros)
        return -interference
    
    def _record_mining_experience(self, block: BitcoinBlock, nonce: int, 
                                 hash_result: str, is_valid: bool):
        """Record mining attempt as temporal experience"""
        # Visual symbols - what we "see" in the hash
        visual_symbols = []
        leading_zeros = 0
        for char in hash_result:
            if char == '0':
                leading_zeros += 1
            else:
                break
        
        visual_symbols.append(f"leading_zeros_{leading_zeros}")
        visual_symbols.append(f"hash_pattern_{hash_result[:8]}")
        
        # Calculate progress metrics
        progress = leading_zeros / self.difficulty
        surprise = 1.0 - progress  # High surprise when far from target
        satisfaction = 1.0 if is_valid else progress
        
        # Goals and context
        goals = ["find_valid_hash", "mine_bitcoin", "solve_puzzle"]
        context = [
            f"nonce_{nonce}",
            f"difficulty_{self.difficulty}",
            f"attempt_{len(self.best_candidates)}"
        ]
        
        # Record experience
        result = self.cognition.live_experience(
            visual=visual_symbols,
            mood=satisfaction * 2 - 1,  # Convert to -1 to 1
            arousal=0.8,  # High arousal during mining
            attention=0.9,  # High attention on hash patterns
            goals=goals,
            context=context,
            surprise=surprise,
            satisfaction=satisfaction
        )
        
        return result
    
    def wave_guided_mining(self, block: BitcoinBlock, max_attempts: int = 10000) -> Dict:
        """Mine using wave-guided search instead of brute force"""
        start_time = time.time()
        attempts = 0
        best_score = float('-inf')
        best_nonce = 0
        
        print(f"🌊 Wave-Guided Bitcoin Mining Started")
        print(f"🎯 Target: {self.difficulty} leading zeros")
        print(f"📊 Max attempts: {max_attempts}")
        
        while attempts < max_attempts:
            # Wave-guided nonce selection
            if attempts < 100:
                # Start with random exploration
                nonce = random.randint(0, 2**32 - 1)
            else:
                # Use wave interference to guide search
                base_nonce = best_nonce
                wave_sources = self._create_nonce_wave_sources(base_nonce)
                
                # Create variations based on wave patterns
                variation = int(sum(wave_sources) * 1000000)
                nonce = (base_nonce + variation) % (2**32)
            
            # Test this nonce
            block.nonce = nonce
            hash_result = block.get_hash()
            is_valid = block.is_valid_proof()
            
            # Calculate wave interference score
            interference_score = self._calculate_wave_interference(block, nonce)
            
            # Record experience
            self._record_mining_experience(block, nonce, hash_result, is_valid)
            
            # Update best candidate
            if interference_score > best_score:
                best_score = interference_score
                best_nonce = nonce
                
                leading_zeros = 0
                for char in hash_result:
                    if char == '0':
                        leading_zeros += 1
                    else:
                        break
                
                print(f"🎯 New best: nonce={nonce}, zeros={leading_zeros}, score={interference_score:.4f}")
            
            if is_valid:
                mining_time = time.time() - start_time
                print(f"✅ BLOCK MINED! 🎉")
                print(f"🔑 Winning nonce: {nonce}")
                print(f"#️⃣  Hash: {hash_result}")
                print(f"⏱️  Time: {mining_time:.2f}s")
                print(f"🔄 Attempts: {attempts + 1}")
                
                # Get cognitive insights
                cognitive_state = self.cognition.get_cognitive_state()
                
                return {
                    "success": True,
                    "nonce": nonce,
                    "hash": hash_result,
                    "attempts": attempts + 1,
                    "time": mining_time,
                    "hash_rate": attempts / mining_time,
                    "cognitive_experiences": cognitive_state["total_experiences"],
                    "wave_patterns": cognitive_state["active_symbol_count"],
                    "resonance_patterns": cognitive_state["resonance_patterns"]
                }
            
            attempts += 1
            
            # Progress update
            if attempts % 1000 == 0:
                elapsed = time.time() - start_time
                hash_rate = attempts / elapsed
                print(f"📊 Progress: {attempts}/{max_attempts} attempts, {hash_rate:.0f} H/s")
        
        mining_time = time.time() - start_time
        print(f"❌ Mining failed after {max_attempts} attempts")
        
        return {
            "success": False,
            "attempts": attempts,
            "time": mining_time,
            "hash_rate": attempts / mining_time,
            "best_nonce": best_nonce,
            "best_score": best_score
        }


class TraditionalMiner:
    """Traditional brute-force Bitcoin miner for comparison"""
    
    def __init__(self, difficulty: int = 4):
        self.difficulty = difficulty
    
    def brute_force_mining(self, block: BitcoinBlock, max_attempts: int = 10000) -> Dict:
        """Traditional brute-force mining"""
        start_time = time.time()
        
        print(f"⚡ Traditional Brute-Force Mining Started")
        print(f"🎯 Target: {self.difficulty} leading zeros")
        
        for nonce in range(max_attempts):
            block.nonce = nonce
            hash_result = block.get_hash()
            
            if block.is_valid_proof():
                mining_time = time.time() - start_time
                print(f"✅ BLOCK MINED! 🎉")
                print(f"🔑 Winning nonce: {nonce}")
                print(f"#️⃣  Hash: {hash_result}")
                print(f"⏱️  Time: {mining_time:.2f}s")
                print(f"🔄 Attempts: {nonce + 1}")
                
                return {
                    "success": True,
                    "nonce": nonce,
                    "hash": hash_result,
                    "attempts": nonce + 1,
                    "time": mining_time,
                    "hash_rate": nonce / mining_time
                }
            
            if nonce % 1000 == 0:
                elapsed = time.time() - start_time
                hash_rate = nonce / elapsed if elapsed > 0 else 0
                print(f"📊 Progress: {nonce}/{max_attempts} attempts, {hash_rate:.0f} H/s")
        
        mining_time = time.time() - start_time
        print(f"❌ Mining failed after {max_attempts} attempts")
        
        return {
            "success": False,
            "attempts": max_attempts,
            "time": mining_time,
            "hash_rate": max_attempts / mining_time
        }


def create_test_block() -> BitcoinBlock:
    """Create a test Bitcoin block"""
    return BitcoinBlock(
        index=1,
        timestamp=time.time(),
        transactions=["Alice sends 1 BTC to Bob", "Charlie sends 0.5 BTC to David"],
        previous_hash="0000000000000000000000000000000000000000000000000000000000000000",
        target_difficulty=4  # Start with easy difficulty
    )


def bitcoin_mining_showdown():
    """Epic showdown: Wave Engine vs Traditional Mining"""
    print("🏆 BITCOIN MINING SHOWDOWN: WAVE ENGINE VS TRADITIONAL")
    print("=" * 70)
    
    # Create test block
    test_block = create_test_block()
    max_attempts = 50000  # Reasonable for testing
    
    print(f"📦 Test Block:")
    print(f"   Index: {test_block.index}")
    print(f"   Transactions: {len(test_block.transactions)}")
    print(f"   Difficulty: {test_block.target_difficulty} leading zeros")
    print(f"   Max attempts: {max_attempts}")
    
    # Round 1: Traditional Mining
    print(f"\n🥊 ROUND 1: TRADITIONAL BRUTE-FORCE")
    print("-" * 40)
    traditional_miner = TraditionalMiner(test_block.target_difficulty)
    traditional_result = traditional_miner.brute_force_mining(test_block.copy(), max_attempts)
    
    # Round 2: Wave Engine Mining
    print(f"\n🥊 ROUND 2: WAVE ENGINE MINING")
    print("-" * 40)
    wave_miner = WaveHashMiner(test_block.target_difficulty)
    wave_result = wave_miner.wave_guided_mining(test_block.copy(), max_attempts)
    
    # Compare results
    print(f"\n🏆 FINAL RESULTS")
    print("=" * 70)
    
    print(f"Traditional Mining:")
    print(f"  Success: {traditional_result['success']}")
    print(f"  Attempts: {traditional_result['attempts']}")
    print(f"  Time: {traditional_result['time']:.2f}s")
    print(f"  Hash Rate: {traditional_result['hash_rate']:.0f} H/s")
    
    print(f"\nWave Engine Mining:")
    print(f"  Success: {wave_result['success']}")
    print(f"  Attempts: {wave_result['attempts']}")
    print(f"  Time: {wave_result['time']:.2f}s")
    print(f"  Hash Rate: {wave_result['hash_rate']:.0f} H/s")
    
    if 'cognitive_experiences' in wave_result:
        print(f"  Cognitive Experiences: {wave_result['cognitive_experiences']}")
        print(f"  Wave Patterns: {wave_result['wave_patterns']}")
    
    # Determine winner
    if traditional_result['success'] and wave_result['success']:
        if wave_result['time'] < traditional_result['time']:
            print(f"\n🎉 WAVE ENGINE WINS! {wave_result['time']:.2f}s vs {traditional_result['time']:.2f}s")
        else:
            print(f"\n🎉 TRADITIONAL WINS! {traditional_result['time']:.2f}s vs {wave_result['time']:.2f}s")
    elif wave_result['success']:
        print(f"\n🎉 WAVE ENGINE WINS! (Only successful method)")
    elif traditional_result['success']:
        print(f"\n🎉 TRADITIONAL WINS! (Only successful method)")
    else:
        print(f"\n🤝 TIE! (Both failed)")
    
    # Reality check
    print(f"\n💡 REALITY CHECK:")
    print(f"Real Bitcoin mining hash rates: ~100 TH/s (100,000,000,000,000 H/s)")
    print(f"Our experimental rates: ~{max(traditional_result['hash_rate'], wave_result['hash_rate']):.0f} H/s")
    print(f"We're about {100_000_000_000_000 / max(traditional_result['hash_rate'], wave_result['hash_rate']):.0e} times slower! 😅")


if __name__ == "__main__":
    bitcoin_mining_showdown() 