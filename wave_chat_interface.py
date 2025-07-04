#!/usr/bin/env python3
"""
Interactive Wave Chat Interface
Real-time conversational interface for the wave-based text engine
"""

import sys
import time
import json
from datetime import datetime
from wave_text_engine import WaveTextEngine

class WaveChatInterface:
    """Interactive chat interface for the wave text engine"""
    
    def __init__(self):
        self.engine = WaveTextEngine()
        self.user_id = "user"
        self.session_start = time.time()
        self.commands = {
            '/help': self.show_help,
            '/summary': self.show_conversation_summary,
            '/explain': self.explain_last_response,
            '/wave': self.show_wave_state,
            '/save': self.save_conversation,
            '/load': self.load_conversation,
            '/reset': self.reset_conversation,
            '/quit': self.quit_chat,
            '/exit': self.quit_chat
        }
        
        print("🌊 WAVE CHAT INTERFACE 🌊")
        print("=" * 50)
        print("Welcome to the Wave-Based Conversational AI!")
        print("Type '/help' for commands or just start chatting.")
        print("Type '/quit' or '/exit' to end the conversation.")
        print("=" * 50)
    
    def show_help(self):
        """Show help information"""
        print("\n🔧 Available Commands:")
        print("  /help     - Show this help message")
        print("  /summary  - Show conversation summary")
        print("  /explain  - Explain the wave reasoning behind last response")
        print("  /wave     - Show current wave state")
        print("  /save     - Save conversation to file")
        print("  /load     - Load conversation from file")
        print("  /reset    - Reset conversation history")
        print("  /quit     - End the conversation")
        print("\n💡 Tips:")
        print("  - Ask questions to see wave-based reasoning")
        print("  - Make statements to see wave pattern analysis")
        print("  - The AI learns from your conversation style")
        print("  - Wave interference creates unique responses")
        print()
    
    def show_conversation_summary(self):
        """Show conversation summary"""
        summary = self.engine.get_conversation_summary()
        
        print("\n📊 Conversation Summary:")
        print("-" * 30)
        
        if "message" in summary:
            print(summary["message"])
            return
        
        print(f"Total turns: {summary['total_turns']}")
        print(f"Session duration: {time.time() - self.session_start:.1f} seconds")
        
        print("\nConversation types:")
        for conv_type, count in summary['conversation_types'].items():
            print(f"  {conv_type}: {count}")
        
        print("\nTop discussion topics:")
        for topic, count in summary['top_topics'][:5]:
            print(f"  {topic}: {count} mentions")
        
        # Show wave state
        wave_state = summary.get('recent_wave_state', {})
        if wave_state:
            print(f"\nWave state:")
            print(f"  Active symbols: {wave_state.get('active_symbol_count', 0)}")
            print(f"  Total experiences: {wave_state.get('total_experiences', 0)}")
            print(f"  Resonance patterns: {wave_state.get('resonance_patterns', 0)}")
        
        print()
    
    def explain_last_response(self):
        """Explain the wave reasoning behind the last response"""
        explanation = self.engine.explain_last_response()
        print(f"\n🌊 Wave Reasoning Explanation:")
        print("-" * 30)
        print(explanation)
        print()
    
    def show_wave_state(self):
        """Show current wave state"""
        wave_state = self.engine.wave_engine.get_cognitive_state()
        
        print(f"\n🌊 Current Wave State:")
        print("-" * 30)
        print(f"Active symbols: {wave_state.get('active_symbol_count', 0)}")
        print(f"Total experiences: {wave_state.get('total_experiences', 0)}")
        print(f"Resonance patterns: {wave_state.get('resonance_patterns', 0)}")
        print(f"Replay cycles: {wave_state.get('replay_cycles', 0)}")
        
        # Show current activation field
        activation_field = wave_state.get('activation_field', {})
        if activation_field:
            print(f"\nCurrent activations:")
            sorted_activations = sorted(activation_field.items(), key=lambda x: abs(x[1]), reverse=True)
            for symbol, activation in sorted_activations[:5]:
                direction = "+" if activation > 0 else "-"
                strength = "Strong" if abs(activation) > 0.5 else "Moderate" if abs(activation) > 0.2 else "Weak"
                print(f"  {symbol}: {direction}{abs(activation):.3f} ({strength})")
        
        print()
    
    def save_conversation(self):
        """Save conversation to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"wave_conversation_{timestamp}.json"
        
        try:
            conversation_data = {
                'session_info': {
                    'user_id': self.user_id,
                    'start_time': self.session_start,
                    'end_time': time.time(),
                    'duration': time.time() - self.session_start
                },
                'conversation_history': self.engine.conversation_history,
                'conversation_summary': self.engine.get_conversation_summary(),
                'wave_state': self.engine.wave_engine.get_cognitive_state()
            }
            
            with open(filename, 'w') as f:
                json.dump(conversation_data, f, indent=2, default=str)
            
            print(f"\n💾 Conversation saved to: {filename}")
            print()
            
        except Exception as e:
            print(f"\n❌ Error saving conversation: {e}")
            print()
    
    def load_conversation(self):
        """Load conversation from file"""
        print("\n📁 Available conversation files:")
        import os
        files = [f for f in os.listdir('.') if f.startswith('wave_conversation_') and f.endswith('.json')]
        
        if not files:
            print("No saved conversations found.")
            print()
            return
        
        for i, filename in enumerate(files[:5]):  # Show last 5 files
            print(f"  {i+1}. {filename}")
        
        try:
            choice = input("\nEnter file number to load (or press Enter to cancel): ").strip()
            if not choice:
                return
            
            file_index = int(choice) - 1
            if 0 <= file_index < len(files):
                filename = files[file_index]
                
                with open(filename, 'r') as f:
                    conversation_data = json.load(f)
                
                # Restore conversation history
                self.engine.conversation_history = conversation_data.get('conversation_history', [])
                print(f"\n✅ Conversation loaded from: {filename}")
                print(f"Restored {len(self.engine.conversation_history)} conversation turns")
                print()
            else:
                print("Invalid file number.")
                print()
                
        except (ValueError, FileNotFoundError, json.JSONDecodeError) as e:
            print(f"\n❌ Error loading conversation: {e}")
            print()
    
    def reset_conversation(self):
        """Reset conversation history"""
        confirm = input("\n⚠️  Are you sure you want to reset the conversation? (y/N): ").strip().lower()
        if confirm in ['y', 'yes']:
            self.engine.conversation_history = []
            self.engine.user_context = {}
            print("\n🔄 Conversation history reset.")
            print()
        else:
            print("\n❌ Reset cancelled.")
            print()
    
    def quit_chat(self):
        """End the conversation"""
        print("\n👋 Thanks for chatting with the Wave Engine!")
        
        # Show final summary
        summary = self.engine.get_conversation_summary()
        if "message" not in summary:
            print(f"We had {summary['total_turns']} turns of conversation.")
            print(f"Session duration: {time.time() - self.session_start:.1f} seconds")
        
        # Ask if user wants to save
        save_choice = input("\nWould you like to save this conversation? (y/N): ").strip().lower()
        if save_choice in ['y', 'yes']:
            self.save_conversation()
        
        print("Goodbye! 🌊")
        sys.exit(0)
    
    def process_input(self, user_input: str):
        """Process user input (command or chat message)"""
        if user_input.startswith('/'):
            # Handle command
            command = user_input.split()[0]
            if command in self.commands:
                self.commands[command]()
            else:
                print(f"Unknown command: {command}")
                print("Type '/help' for available commands.")
        else:
            # Handle chat message
            if user_input.strip():
                print("🤖 ", end="", flush=True)
                response = self.engine.chat(user_input, self.user_id)
                print(response)
            print()
    
    def run(self):
        """Main chat loop"""
        try:
            while True:
                try:
                    user_input = input("👤 ").strip()
                    if user_input:
                        self.process_input(user_input)
                
                except KeyboardInterrupt:
                    print("\n\n🛑 Chat interrupted by user.")
                    self.quit_chat()
                
                except EOFError:
                    print("\n\n🛑 Chat ended.")
                    self.quit_chat()
        
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            print("Chat session ended.")

def main():
    """Main function to start the chat interface"""
    interface = WaveChatInterface()
    interface.run()

if __name__ == "__main__":
    main() 