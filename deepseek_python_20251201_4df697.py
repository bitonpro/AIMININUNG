#!/usr/bin/env python3
"""
Abraham-AI - Jewish-Chinese Wisdom Fusion Engine
Main entry point for the application
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from core.abraham_ai_engine import AbrahamAIEngine
from chevruta.manager import ChevrutaManager
from utils.helpers import setup_logging, load_config

def main():
    """Main entry point for Abraham-AI"""
    
    print("=" * 60)
    print("🕊️  Abraham-AI: Jewish-Chinese Wisdom Fusion Engine")
    print("=" * 60)
    
    # Setup
    setup_logging()
    config = load_config()
    
    # Initialize components
    print("\n🚀 Initializing Abraham-AI Engine...")
    ai_engine = AbrahamAIEngine(config)
    
    print("\n👥 Initializing Chevruta Manager...")
    chevruta = ChevrutaManager(config.get("chevruta", {}))
    
    # Demo
    print("\n" + "=" * 60)
    print("🎯 Demonstration Mode")
    print("=" * 60)
    
    demo_questions = [
        "How can technology be both innovative and harmonious with nature?",
        "מהי הדרך לאזן בין קידמה טכנולוגית לשמירה על ערכים אנושיים?",
        "如何平衡技术创新与自然和谐？"
    ]
    
    for i, question in enumerate(demo_questions, 1):
        print(f"\n📝 Question {i}: {question}")
        print("-" * 40)
        
        # Process question
        response = ai_engine.process_question(question)
        
        # Display results
        print(f"🔍 Analysis Complete!")
        print(f"   • Balance Score: {response.balance_score:.2f}/1.0")
        print(f"   • Yin/Yang: {response.yin_yang_balance}")
        print(f"   • Wisdom Layers: {len(response.wisdom_layers)}")
        
        # Add to chevruta
        chevruta.add_wisdom_exchange(
            participant="Demo System",
            question=question,
            response=response
        )
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 System Summary")
    print("=" * 60)
    
    stats = chevruta.get_statistics()
    print(f"• Total Wisdom Exchanges: {stats['total_exchanges']}")
    print(f"• Jewish Insights: {stats['jewish_insights']}")
    print(f"• Chinese Insights: {stats['chinese_insights']}")
    print(f"• Fusion Insights: {stats['fusion_insights']}")
    
    print("\n" + "=" * 60)
    print("✅ Abraham-AI is ready!")
    print("🤝 Join the Chevruta Room and contribute your wisdom!")
    print("=" * 60)
    
    # Start interactive mode if requested
    if "--interactive" in sys.argv:
        interactive_mode(ai_engine, chevruta)
    
    return 0

def interactive_mode(ai_engine, chevruta):
    """Interactive command line interface"""
    print("\n💬 Interactive Mode (type 'exit' to quit)")
    print("-" * 40)
    
    while True:
        try:
            question = input("\n❓ Ask a question: ").strip()
            
            if question.lower() in ['exit', 'quit', 'q']:
                break
            
            if not question:
                continue
            
            # Process question
            response = ai_engine.process_question(question)
            
            # Display answer
            print(f"\n💡 Answer:")
            print(f"   {response.integrated_answer}")
            
            # Display wisdom layers
            print(f"\n📚 Wisdom Layers:")
            for layer, insight in response.wisdom_layers.items():
                print(f"   • {layer}: {insight}")
            
            # Ask if user wants to contribute
            contribute = input("\n📝 Would you like to add your own insight? (y/n): ")
            if contribute.lower() == 'y':
                name = input("Your name: ").strip() or "Anonymous"
                insight = input("Your insight: ").strip()
                
                chevruta.add_wisdom_exchange(
                    participant=name,
                    question=question,
                    response=response,
                    user_insight=insight
                )
                print("✅ Thank you! Your insight has been added.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Exiting interactive mode.")
            break
        except Exception as e:
            print(f"⚠️  Error: {e}")

if __name__ == "__main__":
    sys.exit(main())