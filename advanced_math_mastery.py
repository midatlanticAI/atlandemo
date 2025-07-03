#!/usr/bin/env python3
"""
Advanced Mathematical Mastery
The next phase: developing flexibility, creativity, and advanced mathematical thinking.
Building on solid foundations to achieve true mathematical mastery.
"""

import time
from src.temporal_cognition import TemporalCognitionEngine


def teach_flexible_thinking(engine):
    """Phase 6: Developing flexible mathematical thinking."""
    print("🤸 PHASE 6: DEVELOPING FLEXIBLE THINKING")
    print("=" * 60)
    
    # Multiple solution strategies
    print("\n📚 Multiple ways to solve the same problem...")
    multiple_strategies = [
        # 8 + 7 in different ways
        (["8", "+", "7"], ["count", "on", "from", "8"], ["8", "9", "10", "11", "12", "13", "14", "15"], "8+7 by counting on"),
        (["8", "+", "7"], ["make", "10", "first"], ["8", "+", "2", "+", "5", "=", "10", "+", "5", "=", "15"], "8+7 by making 10"),
        (["8", "+", "7"], ["double", "strategy"], ["7", "+", "7", "+", "1", "=", "14", "+", "1", "=", "15"], "8+7 using doubles"),
        (["8", "+", "7"], ["break", "apart"], ["8", "+", "5", "+", "2", "=", "13", "+", "2", "=", "15"], "8+7 by breaking apart"),
        
        # 15 - 6 in different ways
        (["15", "-", "6"], ["count", "back"], ["15", "14", "13", "12", "11", "10", "9"], "15-6 by counting back"),
        (["15", "-", "6"], ["count", "up"], ["6", "7", "8", "9", "10", "11", "12", "13", "14", "15"], "15-6 by counting up"),
        (["15", "-", "6"], ["use", "addition"], ["6", "+", "?", "=", "15"], "15-6 using addition"),
        (["15", "-", "6"], ["break", "apart"], ["15", "-", "5", "-", "1", "=", "10", "-", "1", "=", "9"], "15-6 by breaking apart"),
        
        # 9 + 9 in different ways
        (["9", "+", "9"], ["double", "fact"], ["9", "+", "9", "=", "18"], "9+9 as double"),
        (["9", "+", "9"], ["near", "10"], ["10", "+", "10", "-", "2", "=", "20", "-", "2", "=", "18"], "9+9 using 10s"),
        (["9", "+", "9"], ["break", "apart"], ["9", "+", "1", "+", "8", "=", "10", "+", "8", "=", "18"], "9+9 by breaking apart"),
    ]
    
    for i, (problem, strategy_name, solution, description) in enumerate(multiple_strategies, 1):
        print(f"   Experience {i}: {description}")
        engine.live_experience(
            visual=problem + strategy_name + solution,
            auditory=["flexible", "multiple", "ways", "choose"],
            mood=0.4, arousal=0.8, attention=0.9,
            goals=["flexible", "creative", "choose"], surprise=0.6, satisfaction=0.8
        )
        time.sleep(0.03)
    
    # Problem-solving reasoning
    print("\n📚 Developing problem-solving reasoning...")
    reasoning_experiences = [
        # Which strategy is best?
        (["8", "+", "2", "vs", "8", "+", "7"], ["easy", "vs", "hard"], "8+2 is easier than 8+7"),
        (["count", "on", "1", "vs", "count", "on", "5"], ["efficient", "vs", "slow"], "count on small numbers"),
        (["make", "10", "when", "close"], ["strategy", "choice"], "make 10 when numbers are close"),
        (["use", "doubles", "when", "same"], ["strategy", "choice"], "use doubles when numbers are same"),
        
        # Estimation and reasonableness
        (["8", "+", "7", "about", "15"], ["estimate", "reasonable"], "8+7 is about 15"),
        (["15", "-", "6", "about", "9"], ["estimate", "reasonable"], "15-6 is about 9"),
        (["9", "+", "9", "about", "18"], ["estimate", "reasonable"], "9+9 is about 18"),
        (["20", "-", "3", "about", "17"], ["estimate", "reasonable"], "20-3 is about 17"),
        
        # Checking answers
        (["8", "+", "7", "=", "15"], ["check", "8", "+", "8", "-", "1"], "check 8+7 using 8+8-1"),
        (["15", "-", "6", "=", "9"], ["check", "9", "+", "6", "=", "15"], "check 15-6 using 9+6"),
        (["12", "+", "5", "=", "17"], ["check", "17", "-", "5", "=", "12"], "check 12+5 using 17-5"),
    ]
    
    for i, (problem, reasoning, description) in enumerate(reasoning_experiences, 1):
        print(f"   Experience {i}: {description}")
        engine.live_experience(
            visual=problem + reasoning + ["reason", "think"],
            auditory=["reason", "think", "choose", "best"],
            mood=0.3, arousal=0.9, attention=0.9,
            goals=["reason", "think", "judge"], surprise=0.7, satisfaction=0.8
        )
        time.sleep(0.03)
    
    print(f"\n✅ Flexible thinking development complete")


def teach_advanced_patterns(engine):
    """Phase 7: Advanced pattern recognition and algebraic thinking."""
    print("\n\n🔢 PHASE 7: ADVANCED PATTERNS AND ALGEBRAIC THINKING")
    print("=" * 60)
    
    # Growing patterns
    print("\n📚 Understanding growing patterns...")
    growing_patterns = [
        # Linear growth
        (["1", "3", "5", "7", "9"], ["add", "2", "each", "time"], "odd numbers grow by 2"),
        (["2", "4", "6", "8", "10"], ["add", "2", "each", "time"], "even numbers grow by 2"),
        (["3", "6", "9", "12", "15"], ["add", "3", "each", "time"], "multiples of 3 grow by 3"),
        (["5", "10", "15", "20", "25"], ["add", "5", "each", "time"], "multiples of 5 grow by 5"),
        
        # Function patterns
        (["input", "1", "output", "3"], ["rule", "add", "2"], "function rule: add 2"),
        (["input", "2", "output", "4"], ["rule", "add", "2"], "function rule: add 2"),
        (["input", "3", "output", "5"], ["rule", "add", "2"], "function rule: add 2"),
        (["input", "4", "output", "6"], ["rule", "add", "2"], "function rule: add 2"),
        
        # Missing number patterns
        (["2", "4", "?", "8", "10"], ["missing", "6"], "missing number in even sequence"),
        (["1", "3", "5", "?", "9"], ["missing", "7"], "missing number in odd sequence"),
        (["5", "10", "?", "20", "25"], ["missing", "15"], "missing number in 5s sequence"),
        (["3", "6", "9", "?", "15"], ["missing", "12"], "missing number in 3s sequence"),
    ]
    
    for i, (pattern, rule, description) in enumerate(growing_patterns, 1):
        print(f"   Experience {i}: {description}")
        engine.live_experience(
            visual=pattern + rule + ["pattern", "rule"],
            auditory=["pattern", "rule", "predict", "extend"],
            mood=0.5, arousal=0.7, attention=0.8,
            goals=["pattern", "predict", "extend"], surprise=0.5, satisfaction=0.7
        )
        time.sleep(0.03)
    
    # Algebraic thinking
    print("\n📚 Developing algebraic thinking...")
    algebraic_thinking = [
        # Balance and equality
        (["5", "+", "3", "=", "4", "+", "?"], ["balance", "both", "sides"], "balance: 5+3 = 4+?"),
        (["7", "+", "2", "=", "?", "+", "1"], ["balance", "both", "sides"], "balance: 7+2 = ?+1"),
        (["10", "=", "6", "+", "?"], ["balance", "equality"], "balance: 10 = 6+?"),
        (["?", "+", "5", "=", "12"], ["balance", "equality"], "balance: ?+5 = 12"),
        
        # Variable thinking
        (["n", "+", "3", "=", "8"], ["n", "equals", "5"], "variable: n+3=8, so n=5"),
        (["x", "+", "7", "=", "10"], ["x", "equals", "3"], "variable: x+7=10, so x=3"),
        (["y", "-", "4", "=", "6"], ["y", "equals", "10"], "variable: y-4=6, so y=10"),
        (["z", "+", "z", "=", "14"], ["z", "equals", "7"], "variable: z+z=14, so z=7"),
        
        # Inverse operations
        (["if", "a", "+", "5", "=", "12"], ["then", "a", "=", "12", "-", "5"], "inverse: if a+5=12, then a=12-5"),
        (["if", "b", "-", "3", "=", "7"], ["then", "b", "=", "7", "+", "3"], "inverse: if b-3=7, then b=7+3"),
        (["if", "c", "+", "8", "=", "15"], ["then", "c", "=", "15", "-", "8"], "inverse: if c+8=15, then c=15-8"),
    ]
    
    for i, (equation, solution, description) in enumerate(algebraic_thinking, 1):
        print(f"   Experience {i}: {description}")
        engine.live_experience(
            visual=equation + solution + ["algebra", "solve"],
            auditory=["algebra", "solve", "unknown", "find"],
            mood=0.3, arousal=0.8, attention=0.9,
            goals=["algebra", "solve", "unknown"], surprise=0.6, satisfaction=0.8
        )
        time.sleep(0.03)
    
    print(f"\n✅ Advanced patterns and algebraic thinking complete")


def teach_word_problems(engine):
    """Phase 8: Mathematical modeling and word problems."""
    print("\n\n📝 PHASE 8: MATHEMATICAL MODELING AND WORD PROBLEMS")
    print("=" * 60)
    
    # Simple word problems
    print("\n📚 Solving simple word problems...")
    word_problems = [
        # Addition word problems
        (["Sarah", "has", "8", "apples"], ["Tom", "gives", "her", "5", "more"], ["8", "+", "5", "=", "13"], "Sarah has 8, gets 5 more"),
        (["There", "are", "6", "birds"], ["3", "more", "birds", "come"], ["6", "+", "3", "=", "9"], "6 birds, 3 more come"),
        (["I", "have", "7", "stickers"], ["I", "buy", "4", "more"], ["7", "+", "4", "=", "11"], "7 stickers, buy 4 more"),
        
        # Subtraction word problems
        (["There", "are", "12", "cookies"], ["We", "eat", "5", "cookies"], ["12", "-", "5", "=", "7"], "12 cookies, eat 5"),
        (["I", "have", "15", "pencils"], ["I", "give", "away", "6"], ["15", "-", "6", "=", "9"], "15 pencils, give away 6"),
        (["There", "are", "20", "students"], ["8", "students", "leave"], ["20", "-", "8", "=", "12"], "20 students, 8 leave"),
        
        # Comparison problems
        (["Sam", "has", "9", "marbles"], ["Lisa", "has", "5", "marbles"], ["9", "-", "5", "=", "4"], "Sam has 4 more than Lisa"),
        (["Red", "team", "scored", "14"], ["Blue", "team", "scored", "8"], ["14", "-", "8", "=", "6"], "Red scored 6 more than Blue"),
        (["Book", "A", "has", "25", "pages"], ["Book", "B", "has", "18", "pages"], ["25", "-", "18", "=", "7"], "Book A has 7 more pages"),
    ]
    
    for i, (situation, action, equation, description) in enumerate(word_problems, 1):
        print(f"   Experience {i}: {description}")
        engine.live_experience(
            visual=situation + action + equation + ["word", "problem"],
            auditory=["word", "problem", "story", "math"],
            mood=0.4, arousal=0.7, attention=0.9,
            goals=["story", "math", "solve"], surprise=0.5, satisfaction=0.8
        )
        time.sleep(0.03)
    
    # Multi-step problems
    print("\n📚 Solving multi-step problems...")
    multi_step_problems = [
        # Two-step problems
        (["I", "have", "10", "dollars"], ["I", "buy", "book", "for", "6", "dollars"], ["then", "buy", "pen", "for", "2", "dollars"], 
         ["10", "-", "6", "-", "2", "=", "2"], "10 dollars, buy book for 6, pen for 2"),
        
        (["There", "are", "8", "cats"], ["5", "more", "cats", "come"], ["then", "3", "cats", "leave"], 
         ["8", "+", "5", "-", "3", "=", "10"], "8 cats, 5 come, 3 leave"),
        
        (["Sarah", "has", "12", "stickers"], ["gives", "4", "to", "friend"], ["then", "gets", "7", "more"], 
         ["12", "-", "4", "+", "7", "=", "15"], "12 stickers, gives 4, gets 7"),
        
        # Planning problems
        (["need", "20", "chairs"], ["have", "8", "chairs"], ["how", "many", "more", "needed"], 
         ["20", "-", "8", "=", "12"], "need 20 chairs, have 8"),
        
        (["party", "for", "15", "people"], ["each", "person", "gets", "2", "cookies"], ["how", "many", "cookies", "total"], 
         ["15", "×", "2", "=", "30"], "15 people, 2 cookies each"),
    ]
    
    for i, (setup, action1, action2, equation, description) in enumerate(multi_step_problems, 1):
        print(f"   Experience {i}: {description}")
        engine.live_experience(
            visual=setup + action1 + action2 + equation + ["multi", "step"],
            auditory=["multi", "step", "plan", "solve"],
            mood=0.3, arousal=0.8, attention=0.9,
            goals=["plan", "multi", "step"], surprise=0.6, satisfaction=0.8
        )
        time.sleep(0.03)
    
    print(f"\n✅ Mathematical modeling and word problems complete")


def conduct_mastery_assessment(engine):
    """Comprehensive assessment of mathematical mastery."""
    print("\n\n🏆 MATHEMATICAL MASTERY ASSESSMENT")
    print("=" * 60)
    
    test_categories = [
        ("Flexibility", [
            (["9", "+", "6", "=", "?"], "Multiple strategies", "fifteen"),
            (["17", "-", "8", "=", "?"], "Flexible subtraction", "nine"),
            (["8", "+", "8", "+", "1", "=", "?"], "Double plus one", "seventeen"),
        ]),
        ("Patterns", [
            (["3", "6", "9", "?", "15"], "Number sequence", "twelve"),
            (["5", "+", "?", "=", "12"], "Missing addend", "seven"),
            (["n", "+", "4", "=", "11"], "Simple algebra", "seven"),
        ]),
        ("Word Problems", [
            (["Tom", "has", "13", "cards", "gives", "5", "away"], "Subtraction story", "eight"),
            (["8", "birds", "then", "6", "more", "come"], "Addition story", "fourteen"),
            (["need", "20", "chairs", "have", "12"], "Planning problem", "eight"),
        ]),
        ("Advanced", [
            (["7", "+", "5", "=", "6", "+", "?"], "Balance equation", "six"),
            (["15", "-", "?", "=", "8"], "Missing subtrahend", "seven"),
            (["double", "8", "plus", "3"], "Complex operation", "nineteen"),
        ]),
    ]
    
    all_results = []
    category_results = {}
    
    for category_name, tests in test_categories:
        print(f"\n🔍 {category_name.upper()} MASTERY")
        print("-" * 40)
        
        category_correct = 0
        category_total = len(tests)
        
        for i, (visual, description, expected) in enumerate(tests, 1):
            print(f"\n🧪 Test {i}: {description}")
            
            result = engine.live_experience(
                visual=visual,
                auditory=["test", "mastery", "demonstrate"],
                mood=0.3, arousal=0.9, attention=0.9,
                goals=["mastery", "demonstrate", "excel"], surprise=0.6, satisfaction=0.0
            )
            
            field = result['activation_field']
            expected_activation = field.get(expected, 0)
            
            print(f"   Expected '{expected}' activation: {expected_activation:.3f}")
            
            # Show mathematical reasoning
            math_activations = [(k, v) for k, v in field.items() 
                              if abs(v) > 0.5 and k not in [expected, "test", "mastery"]]
            if math_activations:
                print(f"   Mathematical reasoning: {math_activations[:4]}")
            
            success = abs(expected_activation) > 0.5
            if success:
                category_correct += 1
                print(f"   ✅ MASTERY: {description}")
            else:
                print(f"   ❌ DEVELOPING: {description}")
            
            all_results.append((f"{category_name}: {description}", success, expected_activation))
        
        category_results[category_name] = (category_correct, category_total)
        print(f"\n{category_name} Mastery: {category_correct}/{category_total} ({category_correct/category_total*100:.1f}%)")
    
    return all_results, category_results


def run_advanced_curriculum():
    """Run the advanced mathematical mastery curriculum."""
    print("🏆 ADVANCED MATHEMATICAL MASTERY")
    print("=" * 80)
    print("Developing flexibility, creativity, and advanced mathematical thinking")
    print("Building on solid foundations to achieve true mathematical mastery")
    print("=" * 80)
    
    start_time = time.time()
    
    # Create engine and establish foundation
    engine = TemporalCognitionEngine()
    
    # Quick foundation refresh
    print("🔄 REFRESHING MATHEMATICAL FOUNDATIONS...")
    foundation_refresh = [
        (["5", "+", "3", "=", "8"], ["foundation", "fact"], "5+3=8"),
        (["7", "+", "2", "=", "9"], ["foundation", "fact"], "7+2=9"),
        (["10", "-", "4", "=", "6"], ["foundation", "fact"], "10-4=6"),
        (["6", "+", "4", "=", "10"], ["foundation", "fact"], "6+4=10"),
        (["8", "+", "7", "=", "15"], ["foundation", "fact"], "8+7=15"),
    ]
    
    for i, (fact, label, description) in enumerate(foundation_refresh, 1):
        engine.live_experience(
            visual=fact + label,
            auditory=["foundation", "solid"],
            mood=0.8, arousal=0.4, attention=0.8,
            goals=["foundation", "solid"], surprise=0.1, satisfaction=0.9
        )
        time.sleep(0.01)
    
    # Advanced curriculum phases
    teach_flexible_thinking(engine)
    teach_advanced_patterns(engine)
    teach_word_problems(engine)
    
    # Mastery assessment
    all_results, category_results = conduct_mastery_assessment(engine)
    
    end_time = time.time()
    
    # Advanced mastery evaluation
    print("\n\n🏆 ADVANCED MASTERY EVALUATION")
    print("=" * 80)
    
    total_correct = sum(1 for _, success, _ in all_results if success)
    total_tests = len(all_results)
    mastery_percentage = total_correct / total_tests * 100
    
    print(f"\n📊 MASTERY RESULTS BY CATEGORY:")
    for category, (correct, total) in category_results.items():
        percentage = correct / total * 100
        if percentage >= 80:
            status = "🏆 MASTERY"
        elif percentage >= 60:
            status = "🎯 PROFICIENT"
        elif percentage >= 40:
            status = "📈 DEVELOPING"
        else:
            status = "⚠️ EMERGING"
        print(f"   {status} {category}: {correct}/{total} ({percentage:.1f}%)")
    
    print(f"\n🏆 OVERALL MATHEMATICAL MASTERY:")
    print(f"   Advanced mastery: {total_correct}/{total_tests} ({mastery_percentage:.1f}%)")
    print(f"   Development time: {end_time - start_time:.2f} seconds")
    
    # Final cognitive state
    final_state = engine.get_cognitive_state()
    print(f"\n🧠 ADVANCED COGNITIVE STATE:")
    print(f"   Total mathematical experiences: {final_state['total_experiences']}")
    print(f"   Active mathematical concepts: {final_state['active_symbol_count']}")
    print(f"   Complex resonance patterns: {final_state['resonance_patterns']}")
    print(f"   Advanced consolidation cycles: {final_state['replay_cycles']}")
    
    # Mastery level assessment
    print(f"\n🎓 MATHEMATICAL MASTERY LEVEL:")
    
    if mastery_percentage >= 85:
        print(f"   🌟 MATHEMATICAL EXPERT!")
        print(f"   Your cognitive apprentice has achieved advanced mathematical mastery!")
        print(f"   They demonstrate flexible thinking, creative problem-solving,")
        print(f"   and sophisticated mathematical reasoning. Ready for advanced topics!")
        
    elif mastery_percentage >= 75:
        print(f"   🏆 MATHEMATICAL PROFICIENCY!")
        print(f"   Your cognitive apprentice shows strong mathematical competence!")
        print(f"   They can solve complex problems and think flexibly.")
        print(f"   Ready for more advanced mathematical challenges!")
        
    elif mastery_percentage >= 65:
        print(f"   🎯 SOLID MATHEMATICAL FOUNDATION!")
        print(f"   Your cognitive apprentice has good mathematical understanding!")
        print(f"   They show emerging flexibility and problem-solving skills.")
        print(f"   Continue developing advanced thinking strategies!")
        
    elif mastery_percentage >= 50:
        print(f"   📈 DEVELOPING MATHEMATICAL THINKING!")
        print(f"   Your cognitive apprentice shows mathematical progress!")
        print(f"   Basic skills are solid, advanced skills are emerging.")
        print(f"   Focus on flexibility and creative problem-solving!")
        
    else:
        print(f"   ⚠️ MATHEMATICAL FOUNDATIONS NEED STRENGTHENING")
        print(f"   Your cognitive apprentice needs more foundational work.")
        print(f"   Return to basic concepts and build more systematically.")
        print(f"   Every mathematical journey requires solid foundations!")
    
    # Progress analysis
    print(f"\n📈 MATHEMATICAL DEVELOPMENT ANALYSIS:")
    flexibility_score = category_results.get("Flexibility", (0, 1))[0] / category_results.get("Flexibility", (0, 1))[1]
    patterns_score = category_results.get("Patterns", (0, 1))[0] / category_results.get("Patterns", (0, 1))[1]
    word_problems_score = category_results.get("Word Problems", (0, 1))[0] / category_results.get("Word Problems", (0, 1))[1]
    advanced_score = category_results.get("Advanced", (0, 1))[0] / category_results.get("Advanced", (0, 1))[1]
    
    print(f"   🤸 Flexible Thinking: {flexibility_score:.1%}")
    print(f"   🔢 Pattern Recognition: {patterns_score:.1%}")
    print(f"   📝 Word Problems: {word_problems_score:.1%}")
    print(f"   🧠 Advanced Reasoning: {advanced_score:.1%}")
    
    # Next steps
    print(f"\n🚀 NEXT STEPS FOR MATHEMATICAL MASTERY:")
    if mastery_percentage >= 75:
        print(f"   • Explore advanced topics: fractions, decimals, geometry")
        print(f"   • Develop mathematical proof and reasoning skills")
        print(f"   • Apply mathematics to real-world problem solving")
        print(f"   • Begin algebraic and geometric thinking")
    elif mastery_percentage >= 60:
        print(f"   • Strengthen flexible thinking strategies")
        print(f"   • Practice more complex word problems")
        print(f"   • Develop algebraic reasoning skills")
        print(f"   • Build pattern recognition abilities")
    else:
        print(f"   • Reinforce foundational mathematical concepts")
        print(f"   • Practice basic problem-solving strategies")
        print(f"   • Develop number sense and computational fluency")
        print(f"   • Build confidence through successful experiences")
    
    print(f"\n🎓 The journey of mathematical mastery continues...")
    print(f"   Through temporal resonance and natural learning patterns,")
    print(f"   your cognitive apprentice grows in mathematical wisdom! 🌟")


if __name__ == "__main__":
    run_advanced_curriculum() 