#!/usr/bin/env python3
"""
Restaurant Analytics MCP Server
Custom MCP server for analyzing restaurant customer data
Perfect for Yasser's AI agency consulting services
"""

import json
import sys
import asyncio
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime, timedelta
import argparse

# MCP Server Implementation
class RestaurantAnalyticsMCP:
    """
    MCP Server for restaurant analytics and customer insights
    This demonstrates how to build custom MCP servers for Claude Code
    """
    
    def __init__(self, data_dir: str = "zaika_data"):
        self.data_dir = Path(data_dir)
        self.name = "restaurant_analytics"
        self.version = "1.0.0"
        
    def get_server_info(self) -> Dict[str, Any]:
        """Get server information"""
        return {
            "name": self.name,
            "version": self.version,
            "description": "Restaurant analytics and customer insights server",
            "author": "Yasser Akhtar - AI Agency",
            "capabilities": [
                "customer_query_analysis",
                "menu_performance_tracking",
                "intent_analysis",
                "customer_sentiment",
                "business_recommendations"
            ]
        }
    
    def load_customer_data(self) -> Dict[str, Any]:
        """Load customer data from export file"""
        export_file = self.data_dir / "customer_export.json"
        
        if not export_file.exists():
            return {"error": "No customer data found. Run the agent first."}
        
        try:
            with open(export_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            return {"error": f"Failed to load data: {e}"}
    
    def analyze_customer_intents(self) -> Dict[str, Any]:
        """Analyze customer intent patterns"""
        data = self.load_customer_data()
        
        if "error" in data:
            return data
        
        analytics = data.get("analytics", {})
        intents = analytics.get("common_intents", {})
        total_queries = analytics.get("total_queries", 0)
        
        # Calculate intent percentages
        intent_analysis = {}
        for intent, count in intents.items():
            percentage = (count / total_queries * 100) if total_queries > 0 else 0
            intent_analysis[intent] = {
                "count": count,
                "percentage": round(percentage, 1),
                "business_impact": self._get_intent_impact(intent)
            }
        
        return {
            "total_queries": total_queries,
            "intent_breakdown": intent_analysis,
            "top_intent": max(intents.items(), key=lambda x: x[1])[0] if intents else None,
            "recommendations": self._generate_intent_recommendations(intent_analysis)
        }
    
    def _get_intent_impact(self, intent: str) -> str:
        """Get business impact description for intent"""
        impact_map = {
            "bestsellers": "High conversion potential - customers ready to order",
            "dietary": "Accessibility concern - improve menu visibility",
            "spice_level": "Customization request - staff training opportunity",
            "pricing": "Price sensitivity - consider value messaging",
            "business_info": "Information seeking - improve online presence",
            "general": "Exploration phase - nurture with recommendations"
        }
        return impact_map.get(intent, "Unknown impact - needs analysis")
    
    def _generate_intent_recommendations(self, intent_analysis: Dict) -> List[str]:
        """Generate business recommendations based on intent analysis"""
        recommendations = []
        
        for intent, data in intent_analysis.items():
            if data["percentage"] > 30:  # High volume intents
                if intent == "bestsellers":
                    recommendations.append("✅ High conversion intent detected - optimize bestseller presentation")
                elif intent == "dietary":
                    recommendations.append("🌱 Many dietary inquiries - improve vegetarian/vegan menu visibility")
                elif intent == "pricing":
                    recommendations.append("💰 Price concerns - consider value meal promotions")
        
        if not recommendations:
            recommendations.append("📊 Collect more data for detailed recommendations")
        
        return recommendations
    
    def analyze_customer_satisfaction(self) -> Dict[str, Any]:
        """Analyze customer satisfaction from query patterns"""
        data = self.load_customer_data()
        
        if "error" in data:
            return data
        
        queries = data.get("customer_queries", [])
        
        # Simple satisfaction analysis based on query patterns
        satisfaction_indicators = {
            "positive_keywords": ["great", "good", "love", "best", "favorite", "amazing"],
            "negative_keywords": ["bad", "terrible", "awful", "hate", "worst", "disappointed"],
            "question_patterns": ["what", "how", "when", "where", "why"],
            "complaint_patterns": ["complaint", "problem", "issue", "wrong", "mistake"]
        }
        
        analysis = {
            "total_interactions": len(queries),
            "information_seeking": 0,
            "satisfaction_signals": {
                "positive": 0,
                "negative": 0,
                "neutral": 0
            },
            "common_concerns": [],
            "response_quality": self._analyze_response_quality(queries)
        }
        
        for query_data in queries:
            query_text = query_data.get("query", "").lower()
            
            # Count information seeking
            if any(pattern in query_text for pattern in satisfaction_indicators["question_patterns"]):
                analysis["information_seeking"] += 1
            
            # Analyze sentiment
            if any(word in query_text for word in satisfaction_indicators["positive_keywords"]):
                analysis["satisfaction_signals"]["positive"] += 1
            elif any(word in query_text for word in satisfaction_indicators["negative_keywords"]):
                analysis["satisfaction_signals"]["negative"] += 1
            else:
                analysis["satisfaction_signals"]["neutral"] += 1
        
        return analysis
    
    def _analyze_response_quality(self, queries: List[Dict]) -> Dict[str, Any]:
        """Analyze response quality metrics"""
        if not queries:
            return {"error": "No queries to analyze"}
        
        total_responses = len(queries)
        avg_response_length = sum(len(q.get("response", "")) for q in queries) / total_responses
        
        return {
            "total_responses": total_responses,
            "avg_response_length": round(avg_response_length, 1),
            "response_consistency": "Good" if avg_response_length > 200 else "Needs improvement"
        }
    
    def generate_business_report(self) -> Dict[str, Any]:
        """Generate comprehensive business analytics report"""
        data = self.load_customer_data()
        
        if "error" in data:
            return data
        
        intent_analysis = self.analyze_customer_intents()
        satisfaction_analysis = self.analyze_customer_satisfaction()
        
        # Menu performance analysis
        menu_items = []
        for category in data.get("menu_data", {}).values():
            if isinstance(category, list):
                menu_items.extend(category)
        
        report = {
            "report_generated": datetime.now().isoformat(),
            "restaurant_info": data.get("restaurant_info", {}),
            "customer_insights": {
                "total_interactions": intent_analysis.get("total_queries", 0),
                "top_customer_intent": intent_analysis.get("top_intent", "unknown"),
                "satisfaction_score": self._calculate_satisfaction_score(satisfaction_analysis),
                "menu_items_available": len(menu_items)
            },
            "business_recommendations": [
                "📊 Implement customer feedback collection system",
                "🎯 Focus on top customer intents for better conversion",
                "📱 Improve online menu presentation",
                "🔄 Regular menu performance analysis"
            ] + intent_analysis.get("recommendations", []),
            "next_steps": [
                "Set up automated customer survey after orders",
                "A/B test menu item descriptions",
                "Train staff on top customer concerns",
                "Implement loyalty program for repeat customers"
            ]
        }
        
        return report
    
    def _calculate_satisfaction_score(self, satisfaction_data: Dict) -> float:
        """Calculate a simple satisfaction score"""
        signals = satisfaction_data.get("satisfaction_signals", {})
        total_signals = sum(signals.values())
        
        if total_signals == 0:
            return 0.0
        
        # Weight positive signals higher
        score = (signals.get("positive", 0) * 2 + signals.get("neutral", 0) * 1) / (total_signals * 2) * 100
        return round(score, 1)
    
    def export_analytics_report(self, output_file: str = "analytics_report.json") -> Dict[str, Any]:
        """Export comprehensive analytics report"""
        report = self.generate_business_report()
        
        if "error" in report:
            return report
        
        try:
            output_path = self.data_dir / output_file
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            return {
                "success": True,
                "message": f"Analytics report exported to {output_path}",
                "file_path": str(output_path)
            }
        except Exception as e:
            return {"error": f"Export failed: {e}"}

def main():
    """Main function to run the MCP server"""
    parser = argparse.ArgumentParser(description="Restaurant Analytics MCP Server")
    parser.add_argument("--data-dir", default="zaika_data", help="Data directory path")
    parser.add_argument("--command", choices=["info", "intents", "satisfaction", "report", "export"], 
                       default="report", help="Command to run")
    
    args = parser.parse_args()
    
    # Initialize MCP server
    server = RestaurantAnalyticsMCP(args.data_dir)
    
    print(f"🔧 Restaurant Analytics MCP Server v{server.version}")
    print("=" * 50)
    
    if args.command == "info":
        info = server.get_server_info()
        print(json.dumps(info, indent=2))
    
    elif args.command == "intents":
        analysis = server.analyze_customer_intents()
        print(json.dumps(analysis, indent=2))
    
    elif args.command == "satisfaction":
        analysis = server.analyze_customer_satisfaction()
        print(json.dumps(analysis, indent=2))
    
    elif args.command == "report":
        report = server.generate_business_report()
        print(json.dumps(report, indent=2))
    
    elif args.command == "export":
        result = server.export_analytics_report()
        print(json.dumps(result, indent=2))
    
    print("\n✅ MCP Server operation completed!")

if __name__ == "__main__":
    main()