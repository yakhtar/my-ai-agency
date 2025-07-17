#!/usr/bin/env python3
"""
🎭 Your First MCP Server - Joke Generator
Built by Yasser Akhtar as his first Claude Code learning exercise!

This is a simple MCP server that tells jokes.
It's designed to help you understand MCP basics in a fun way.
"""

import json
import random
from typing import Dict, List, Any
from datetime import datetime
import argparse

class JokeMCP:
    """
    🎭 Your First MCP Server - A Simple Joke Generator
    
    This is your first step into the world of MCP servers!
    It's simple, fun, and teaches you the basic structure.
    """
    
    def __init__(self):
        self.name = "joke_mcp"
        self.version = "1.0.0"
        self.creator = "Yasser Akhtar"
        
        # Collection of jokes for different categories
        self.jokes = {
            "programming": [
                "Why do programmers prefer dark mode? Because light attracts bugs! 🐛",
                "How many programmers does it take to change a light bulb? None, that's a hardware problem! 💡",
                "Why did the programmer quit his job? He didn't get arrays! 😄",
                "What do you call a programmer from Finland? Nerdic! 🇫🇮",
                "Why don't programmers like nature? It has too many bugs! 🌲🐛"
            ],
            
            "ai": [
                "Why did the AI break up with the database? It couldn't handle the relationship! 💔",
                "What do you call an AI that sings? A neural network! 🎵",
                "Why don't AI systems ever get tired? They run on infinite loops! ♾️",
                "What's an AI's favorite type of music? Algo-rhythm! 🎶",
                "Why did the machine learning model go to therapy? It had too many issues to resolve! 🤖"
            ],
            
            "business": [
                "Why don't entrepreneurs ever get cold? They're always networking! 🌐",
                "What do you call a business that's always busy? A buzz-iness! 🐝",
                "Why did the consultant bring a ladder to the meeting? To reach new heights! 🪜",
                "What's a marketer's favorite type of tea? Proper-tea! 🍵",
                "Why do accountants make good comedians? They know how to balance the books! 📚"
            ],
            
            "general": [
                "Why don't scientists trust atoms? Because they make up everything! ⚛️",
                "What do you call a bear with no teeth? A gummy bear! 🐻",
                "Why did the coffee file a police report? It got mugged! ☕",
                "What do you call a fish wearing a crown? A king fish! 👑🐟",
                "Why don't eggs tell jokes? They'd crack each other up! 🥚"
            ]
        }
    
    def get_server_info(self) -> Dict[str, Any]:
        """Get information about this MCP server"""
        return {
            "name": self.name,
            "version": self.version,
            "creator": self.creator,
            "description": "A simple joke generator MCP server for learning",
            "created_as": "First MCP server learning exercise",
            "capabilities": [
                "tell_random_joke",
                "tell_category_joke", 
                "list_categories",
                "get_joke_stats"
            ],
            "joke_categories": list(self.jokes.keys()),
            "total_jokes": sum(len(jokes) for jokes in self.jokes.values()),
            "learning_objective": "Understand basic MCP server structure and JSON responses"
        }
    
    def tell_random_joke(self) -> Dict[str, Any]:
        """
        🎲 Tell a random joke from any category
        
        This is the main function of our MCP server.
        It randomly selects a joke and returns it in JSON format.
        """
        
        # Pick a random category
        category = random.choice(list(self.jokes.keys()))
        
        # Pick a random joke from that category
        joke = random.choice(self.jokes[category])
        
        return {
            "joke": joke,
            "category": category,
            "told_at": datetime.now().isoformat(),
            "message": "Hope this made you smile! 😊",
            "your_achievement": "🎉 You just used your first MCP server!"
        }
    
    def tell_category_joke(self, category: str) -> Dict[str, Any]:
        """
        🎯 Tell a joke from a specific category
        
        This shows how MCP servers can take parameters
        and customize their responses based on input.
        """
        
        if category not in self.jokes:
            return {
                "error": f"Sorry, I don't have jokes for '{category}'",
                "available_categories": list(self.jokes.keys()),
                "suggestion": "Try 'programming', 'ai', 'business', or 'general'"
            }
        
        joke = random.choice(self.jokes[category])
        
        return {
            "joke": joke,
            "category": category,
            "told_at": datetime.now().isoformat(),
            "message": f"Here's a {category} joke for you! 😄",
            "learning_note": "Notice how the MCP server handled your specific request!"
        }
    
    def list_categories(self) -> Dict[str, Any]:
        """
        📝 List all available joke categories
        
        This shows how MCP servers can provide information
        about their capabilities.
        """
        
        category_info = {}
        for category, jokes in self.jokes.items():
            category_info[category] = {
                "joke_count": len(jokes),
                "sample_joke": jokes[0]  # Show first joke as sample
            }
        
        return {
            "available_categories": list(self.jokes.keys()),
            "category_details": category_info,
            "total_jokes": sum(len(jokes) for jokes in self.jokes.values()),
            "usage_tip": "Use 'tell_category_joke' with any category name",
            "learning_note": "This shows how MCP servers can be self-documenting!"
        }
    
    def get_joke_stats(self) -> Dict[str, Any]:
        """
        📊 Get statistics about the joke collection
        
        This demonstrates how MCP servers can analyze
        and report on their data.
        """
        
        stats = {
            "total_jokes": sum(len(jokes) for jokes in self.jokes.values()),
            "categories": len(self.jokes),
            "breakdown": {category: len(jokes) for category, jokes in self.jokes.items()},
            "largest_category": max(self.jokes.keys(), key=lambda k: len(self.jokes[k])),
            "server_created": "Learning exercise for Yasser Akhtar",
            "fun_fact": "This is your first step into MCP server development!"
        }
        
        return stats
    
    def celebrate_first_mcp(self) -> Dict[str, Any]:
        """
        🎉 Celebrate creating your first MCP server!
        
        This is a special function to celebrate your achievement.
        """
        
        return {
            "congratulations": "🎉 Congratulations, Yasser! You just built your first MCP server!",
            "achievement_unlocked": "MCP Server Developer",
            "what_you_learned": [
                "✅ Basic MCP server structure",
                "✅ JSON responses and data formatting",
                "✅ Function organization and documentation",
                "✅ Error handling and user feedback",
                "✅ Self-documenting code practices"
            ],
            "next_steps": [
                "Try running different commands to see how it works",
                "Look at the code to understand the structure",
                "Think about what other MCP servers you could build",
                "Share your achievement - you're now a Claude Code developer!"
            ],
            "motivational_message": "Every expert was once a beginner. You just took your first step into the world of Claude Code development!",
            "your_potential": "With your 15+ years of experience, you're going to build amazing AI solutions!"
        }

def main():
    """Main function to run your first MCP server"""
    parser = argparse.ArgumentParser(description="🎭 Your First MCP Server - Joke Generator")
    parser.add_argument("--command", choices=["info", "joke", "category", "categories", "stats", "celebrate"], 
                       default="joke", help="What would you like to do?")
    parser.add_argument("--category", help="Joke category (programming, ai, business, general)")
    
    args = parser.parse_args()
    
    # Initialize your joke MCP server
    joke_server = JokeMCP()
    
    print(f"🎭 {joke_server.name} v{joke_server.version}")
    print(f"👨‍💻 Created by: {joke_server.creator}")
    print(f"🎯 Your First MCP Server!")
    print("=" * 40)
    
    if args.command == "info":
        info = joke_server.get_server_info()
        print(json.dumps(info, indent=2))
    
    elif args.command == "joke":
        joke = joke_server.tell_random_joke()
        print(json.dumps(joke, indent=2))
    
    elif args.command == "category":
        if args.category:
            joke = joke_server.tell_category_joke(args.category)
            print(json.dumps(joke, indent=2))
        else:
            print("Please specify a category with --category")
            print("Available categories: programming, ai, business, general")
    
    elif args.command == "categories":
        categories = joke_server.list_categories()
        print(json.dumps(categories, indent=2))
    
    elif args.command == "stats":
        stats = joke_server.get_joke_stats()
        print(json.dumps(stats, indent=2))
    
    elif args.command == "celebrate":
        celebration = joke_server.celebrate_first_mcp()
        print(json.dumps(celebration, indent=2))
    
    print("\n🎉 Great job building your first MCP server!")
    print("🚀 You're now officially a Claude Code developer!")

if __name__ == "__main__":
    main()