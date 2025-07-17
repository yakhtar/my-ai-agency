#!/usr/bin/env python3
"""
🔍 Advanced Customer Data Analyzer MCP Server
Built by Yasser Akhtar for AI Agency client projects

This MCP server demonstrates advanced data analysis capabilities
that you can offer to clients for business intelligence.
"""

import json
import sys
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime, timedelta
import argparse
import re
from collections import Counter, defaultdict
import statistics

class CustomerDataAnalyzerMCP:
    """
    🔍 Advanced Customer Data Analyzer
    
    This MCP server showcases sophisticated data analysis capabilities
    that demonstrate your value to potential AI consulting clients.
    
    Key Features:
    - Customer behavior pattern analysis
    - Revenue optimization insights
    - Predictive analytics for business growth
    - Automated reporting and recommendations
    """
    
    def __init__(self, data_directory: str = "customer_data"):
        self.name = "customer_data_analyzer"
        self.version = "2.0.0"
        self.created_by = "Yasser Akhtar - AI Agency"
        self.data_dir = Path(data_directory)
        
        # Ensure data directory exists
        self.data_dir.mkdir(exist_ok=True)
        
        # Load sample data if available
        self.customer_data = self.load_sample_data()
    
    def load_sample_data(self) -> Dict[str, Any]:
        """Load sample customer data for demonstration"""
        
        sample_data_file = self.data_dir / "sample_customers.json"
        
        if sample_data_file.exists():
            try:
                with open(sample_data_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        # Generate sample data for demonstration
        sample_data = {
            "customers": [
                {
                    "customer_id": "C001",
                    "name": "Sarah Johnson",
                    "email": "sarah.j@email.com",
                    "signup_date": "2024-01-15",
                    "last_activity": "2024-07-10",
                    "total_spent": 1250.00,
                    "order_count": 8,
                    "average_order_value": 156.25,
                    "preferred_categories": ["electronics", "home"],
                    "location": "New York",
                    "customer_segment": "high_value"
                },
                {
                    "customer_id": "C002", 
                    "name": "Mike Chen",
                    "email": "mike.chen@email.com",
                    "signup_date": "2024-02-20",
                    "last_activity": "2024-07-15",
                    "total_spent": 450.00,
                    "order_count": 3,
                    "average_order_value": 150.00,
                    "preferred_categories": ["books", "electronics"],
                    "location": "California",
                    "customer_segment": "medium_value"
                },
                {
                    "customer_id": "C003",
                    "name": "Lisa Rodriguez",
                    "email": "lisa.r@email.com", 
                    "signup_date": "2024-03-10",
                    "last_activity": "2024-07-16",
                    "total_spent": 2100.00,
                    "order_count": 12,
                    "average_order_value": 175.00,
                    "preferred_categories": ["fashion", "beauty", "home"],
                    "location": "Texas",
                    "customer_segment": "high_value"
                },
                {
                    "customer_id": "C004",
                    "name": "David Kim",
                    "email": "david.k@email.com",
                    "signup_date": "2024-04-05",
                    "last_activity": "2024-06-20",
                    "total_spent": 180.00,
                    "order_count": 2,
                    "average_order_value": 90.00,
                    "preferred_categories": ["sports"],
                    "location": "Washington",
                    "customer_segment": "low_value"
                },
                {
                    "customer_id": "C005",
                    "name": "Emma Wilson",
                    "email": "emma.w@email.com",
                    "signup_date": "2024-05-12",
                    "last_activity": "2024-07-14",
                    "total_spent": 890.00,
                    "order_count": 6,
                    "average_order_value": 148.33,
                    "preferred_categories": ["books", "home", "electronics"],
                    "location": "Florida",
                    "customer_segment": "medium_value"
                }
            ],
            "transactions": [
                {"customer_id": "C001", "date": "2024-07-01", "amount": 125.00, "category": "electronics"},
                {"customer_id": "C001", "date": "2024-07-05", "amount": 89.99, "category": "home"},
                {"customer_id": "C002", "date": "2024-07-10", "amount": 150.00, "category": "electronics"},
                {"customer_id": "C003", "date": "2024-07-12", "amount": 200.00, "category": "fashion"},
                {"customer_id": "C005", "date": "2024-07-14", "amount": 75.50, "category": "books"}
            ]
        }
        
        # Save sample data
        with open(sample_data_file, 'w') as f:
            json.dump(sample_data, f, indent=2)
        
        return sample_data
    
    def get_server_info(self) -> Dict[str, Any]:
        """Get server information and capabilities"""
        return {
            "name": self.name,
            "version": self.version,
            "created_by": self.created_by,
            "description": "Advanced customer data analyzer for business intelligence",
            "capabilities": [
                "customer_segmentation",
                "lifetime_value_analysis", 
                "churn_prediction",
                "revenue_optimization",
                "behavioral_insights",
                "predictive_analytics",
                "automated_reporting"
            ],
            "business_value": [
                "Identify high-value customers for targeted marketing",
                "Predict customer churn before it happens",
                "Optimize pricing and product recommendations",
                "Automate customer insights and reporting",
                "Increase customer lifetime value"
            ],
            "sample_data_loaded": len(self.customer_data.get("customers", [])),
            "learning_objective": "Showcase advanced data analysis for client consulting"
        }
    
    def analyze_customer_segments(self) -> Dict[str, Any]:
        """
        🎯 Analyze customer segments for targeted marketing
        
        This analysis helps businesses understand their customer base
        and create targeted marketing campaigns.
        """
        
        customers = self.customer_data.get("customers", [])
        
        if not customers:
            return {"error": "No customer data available for analysis"}
        
        # Segment analysis
        segments = defaultdict(list)
        total_customers = len(customers)
        
        for customer in customers:
            segment = customer.get("customer_segment", "unknown")
            segments[segment].append(customer)
        
        # Calculate segment metrics
        segment_analysis = {}
        total_revenue = sum(c.get("total_spent", 0) for c in customers)
        
        for segment, segment_customers in segments.items():
            segment_revenue = sum(c.get("total_spent", 0) for c in segment_customers)
            avg_order_value = statistics.mean([c.get("average_order_value", 0) for c in segment_customers])
            avg_order_count = statistics.mean([c.get("order_count", 0) for c in segment_customers])
            
            segment_analysis[segment] = {
                "customer_count": len(segment_customers),
                "percentage_of_base": round((len(segment_customers) / total_customers) * 100, 1),
                "total_revenue": round(segment_revenue, 2),
                "revenue_percentage": round((segment_revenue / total_revenue) * 100, 1),
                "avg_order_value": round(avg_order_value, 2),
                "avg_order_count": round(avg_order_count, 1),
                "revenue_per_customer": round(segment_revenue / len(segment_customers), 2)
            }
        
        # Business recommendations
        recommendations = []
        
        # Find most valuable segment
        most_valuable = max(segment_analysis.keys(), key=lambda s: segment_analysis[s]["revenue_percentage"])
        recommendations.append(f"🎯 Focus marketing budget on {most_valuable} segment (generates {segment_analysis[most_valuable]['revenue_percentage']}% of revenue)")
        
        # Find growth opportunities
        for segment, data in segment_analysis.items():
            if data["customer_count"] > 0 and data["avg_order_value"] < 150:
                recommendations.append(f"💡 {segment} segment has potential for order value increase (currently ${data['avg_order_value']})")
        
        return {
            "analysis_date": datetime.now().isoformat(),
            "total_customers": total_customers,
            "total_revenue": round(total_revenue, 2),
            "segment_breakdown": segment_analysis,
            "key_insights": [
                f"Top revenue segment: {most_valuable}",
                f"Average customer value: ${round(total_revenue/total_customers, 2)}",
                f"Most segments analyzed: {len(segment_analysis)}"
            ],
            "business_recommendations": recommendations,
            "next_actions": [
                "Create targeted campaigns for high-value segments",
                "Develop retention strategies for medium-value customers",
                "Implement upselling for low-value segments"
            ]
        }
    
    def predict_customer_churn(self) -> Dict[str, Any]:
        """
        ⚠️ Predict which customers are likely to churn
        
        This predictive analysis helps businesses retain customers
        before they leave.
        """
        
        customers = self.customer_data.get("customers", [])
        
        if not customers:
            return {"error": "No customer data available for churn analysis"}
        
        churn_analysis = {
            "high_risk": [],
            "medium_risk": [],
            "low_risk": []
        }
        
        current_date = datetime.now()
        
        for customer in customers:
            # Calculate days since last activity
            last_activity = datetime.fromisoformat(customer.get("last_activity", "2024-01-01"))
            days_inactive = (current_date - last_activity).days
            
            # Calculate customer metrics
            total_spent = customer.get("total_spent", 0)
            order_count = customer.get("order_count", 0)
            avg_order_value = customer.get("average_order_value", 0)
            
            # Churn risk scoring
            risk_score = 0
            risk_factors = []
            
            # Inactivity risk
            if days_inactive > 60:
                risk_score += 30
                risk_factors.append(f"Inactive for {days_inactive} days")
            elif days_inactive > 30:
                risk_score += 15
                risk_factors.append(f"Inactive for {days_inactive} days")
            
            # Low engagement risk
            if order_count < 3:
                risk_score += 20
                risk_factors.append("Low order frequency")
            
            # Low value risk
            if avg_order_value < 100:
                risk_score += 15
                risk_factors.append("Low average order value")
            
            # Total spent risk
            if total_spent < 200:
                risk_score += 10
                risk_factors.append("Low total spending")
            
            # Categorize risk
            customer_risk = {
                "customer_id": customer["customer_id"],
                "name": customer["name"],
                "risk_score": risk_score,
                "risk_factors": risk_factors,
                "days_inactive": days_inactive,
                "total_spent": total_spent,
                "recommended_action": ""
            }
            
            if risk_score >= 50:
                customer_risk["recommended_action"] = "Immediate intervention required - personal outreach"
                churn_analysis["high_risk"].append(customer_risk)
            elif risk_score >= 25:
                customer_risk["recommended_action"] = "Send targeted retention campaign"
                churn_analysis["medium_risk"].append(customer_risk)
            else:
                customer_risk["recommended_action"] = "Monitor and maintain regular engagement"
                churn_analysis["low_risk"].append(customer_risk)
        
        # Calculate summary metrics
        total_customers = len(customers)
        high_risk_count = len(churn_analysis["high_risk"])
        medium_risk_count = len(churn_analysis["medium_risk"])
        
        return {
            "analysis_date": datetime.now().isoformat(),
            "total_customers_analyzed": total_customers,
            "churn_risk_summary": {
                "high_risk": {
                    "count": high_risk_count,
                    "percentage": round((high_risk_count / total_customers) * 100, 1)
                },
                "medium_risk": {
                    "count": medium_risk_count,
                    "percentage": round((medium_risk_count / total_customers) * 100, 1)
                },
                "low_risk": {
                    "count": len(churn_analysis["low_risk"]),
                    "percentage": round((len(churn_analysis["low_risk"]) / total_customers) * 100, 1)
                }
            },
            "detailed_analysis": churn_analysis,
            "immediate_actions": [
                f"Contact {high_risk_count} high-risk customers within 24 hours",
                f"Launch retention campaign for {medium_risk_count} medium-risk customers",
                "Implement automated engagement monitoring"
            ],
            "business_impact": f"Retaining high-risk customers could save ${sum(c['total_spent'] for c in churn_analysis['high_risk']):.2f} in potential lost revenue"
        }
    
    def optimize_revenue_opportunities(self) -> Dict[str, Any]:
        """
        💰 Identify revenue optimization opportunities
        
        This analysis helps businesses increase revenue from
        existing customers through strategic recommendations.
        """
        
        customers = self.customer_data.get("customers", [])
        transactions = self.customer_data.get("transactions", [])
        
        if not customers:
            return {"error": "No customer data available for revenue optimization"}
        
        # Analyze customer spending patterns
        customer_metrics = {}
        for customer in customers:
            customer_id = customer["customer_id"]
            customer_metrics[customer_id] = {
                "name": customer["name"],
                "total_spent": customer.get("total_spent", 0),
                "order_count": customer.get("order_count", 0),
                "avg_order_value": customer.get("average_order_value", 0),
                "preferred_categories": customer.get("preferred_categories", []),
                "segment": customer.get("customer_segment", "unknown")
            }
        
        # Calculate category performance
        category_revenue = defaultdict(float)
        category_orders = defaultdict(int)
        
        for transaction in transactions:
            category = transaction.get("category", "unknown")
            amount = transaction.get("amount", 0)
            category_revenue[category] += amount
            category_orders[category] += 1
        
        # Revenue optimization opportunities
        opportunities = []
        
        # 1. Upselling opportunities
        for customer_id, metrics in customer_metrics.items():
            if metrics["avg_order_value"] < 150 and metrics["order_count"] > 3:
                potential_increase = (150 - metrics["avg_order_value"]) * metrics["order_count"]
                opportunities.append({
                    "type": "upselling",
                    "customer_id": customer_id,
                    "customer_name": metrics["name"],
                    "current_aov": metrics["avg_order_value"],
                    "potential_revenue_increase": round(potential_increase, 2),
                    "recommendation": f"Offer premium products or bundles to increase AOV from ${metrics['avg_order_value']:.2f} to $150"
                })
        
        # 2. Cross-selling opportunities
        all_categories = set(category_revenue.keys())
        for customer_id, metrics in customer_metrics.items():
            customer_categories = set(metrics["preferred_categories"])
            unexplored_categories = all_categories - customer_categories
            
            if unexplored_categories and metrics["total_spent"] > 300:
                opportunities.append({
                    "type": "cross_selling",
                    "customer_id": customer_id,
                    "customer_name": metrics["name"],
                    "current_categories": list(customer_categories),
                    "suggested_categories": list(unexplored_categories),
                    "potential_revenue_increase": round(metrics["avg_order_value"] * 0.5, 2),
                    "recommendation": f"Introduce {', '.join(list(unexplored_categories)[:2])} products to expand purchase categories"
                })
        
        # 3. Frequency optimization
        for customer_id, metrics in customer_metrics.items():
            if metrics["order_count"] < 5 and metrics["avg_order_value"] > 120:
                annual_potential = metrics["avg_order_value"] * 12
                current_annual = metrics["total_spent"]
                potential_increase = annual_potential - current_annual
                
                opportunities.append({
                    "type": "frequency_increase",
                    "customer_id": customer_id,
                    "customer_name": metrics["name"],
                    "current_frequency": metrics["order_count"],
                    "target_frequency": 12,
                    "potential_revenue_increase": round(potential_increase, 2),
                    "recommendation": "Implement subscription or loyalty program to increase purchase frequency"
                })
        
        # Calculate total potential revenue
        total_potential = sum(opp.get("potential_revenue_increase", 0) for opp in opportunities)
        
        # Prioritize opportunities
        opportunities.sort(key=lambda x: x.get("potential_revenue_increase", 0), reverse=True)
        
        return {
            "analysis_date": datetime.now().isoformat(),
            "total_customers_analyzed": len(customers),
            "revenue_opportunities": opportunities[:10],  # Top 10 opportunities
            "opportunity_summary": {
                "upselling_opportunities": len([o for o in opportunities if o["type"] == "upselling"]),
                "cross_selling_opportunities": len([o for o in opportunities if o["type"] == "cross_selling"]),
                "frequency_opportunities": len([o for o in opportunities if o["type"] == "frequency_increase"])
            },
            "total_potential_revenue": round(total_potential, 2),
            "category_performance": {
                category: {
                    "revenue": round(revenue, 2),
                    "orders": category_orders[category],
                    "avg_order_value": round(revenue / category_orders[category], 2) if category_orders[category] > 0 else 0
                }
                for category, revenue in category_revenue.items()
            },
            "strategic_recommendations": [
                "Focus on upselling to customers with high order frequency but low AOV",
                "Implement cross-selling campaigns for high-value customers",
                "Create loyalty programs to increase purchase frequency",
                "Optimize product bundling for highest-revenue categories"
            ]
        }
    
    def generate_executive_report(self) -> Dict[str, Any]:
        """
        📊 Generate comprehensive executive report
        
        This creates a high-level summary perfect for
        business stakeholders and decision makers.
        """
        
        # Get all analyses
        segments = self.analyze_customer_segments()
        churn = self.predict_customer_churn()
        revenue_ops = self.optimize_revenue_opportunities()
        
        customers = self.customer_data.get("customers", [])
        
        if not customers:
            return {"error": "No customer data available for executive report"}
        
        # Calculate key metrics
        total_customers = len(customers)
        total_revenue = sum(c.get("total_spent", 0) for c in customers)
        avg_customer_value = total_revenue / total_customers if total_customers > 0 else 0
        
        # Executive summary
        executive_summary = {
            "report_date": datetime.now().isoformat(),
            "reporting_period": "Current customer base analysis",
            "key_metrics": {
                "total_customers": total_customers,
                "total_revenue": round(total_revenue, 2),
                "average_customer_value": round(avg_customer_value, 2),
                "customer_segments": len(segments.get("segment_breakdown", {}))
            },
            "critical_findings": [
                f"🎯 {churn['churn_risk_summary']['high_risk']['count']} customers at high risk of churn",
                f"💰 ${revenue_ops.get('total_potential_revenue', 0):.2f} in identified revenue opportunities",
                f"📈 {segments['segment_breakdown'].get('high_value', {}).get('customer_count', 0)} high-value customers generating significant revenue"
            ],
            "immediate_actions_required": [
                "Implement customer retention program for high-risk customers",
                "Launch upselling campaign for medium-value customers",
                "Optimize product recommendations for cross-selling"
            ],
            "financial_impact": {
                "potential_revenue_increase": revenue_ops.get("total_potential_revenue", 0),
                "churn_prevention_value": sum(c.get("total_spent", 0) for c in churn.get("detailed_analysis", {}).get("high_risk", [])),
                "roi_estimate": "300-500% ROI on targeted retention and growth campaigns"
            },
            "recommendations": [
                "Invest in customer success team for high-value segment",
                "Implement automated churn prediction monitoring",
                "Create personalized marketing campaigns by segment",
                "Develop loyalty program to increase customer lifetime value"
            ]
        }
        
        return {
            "executive_summary": executive_summary,
            "detailed_analyses": {
                "customer_segmentation": segments,
                "churn_prediction": churn,
                "revenue_optimization": revenue_ops
            },
            "next_steps": [
                "Schedule monthly customer health reviews",
                "Implement recommended retention strategies",
                "Track revenue optimization results",
                "Expand data collection for deeper insights"
            ],
            "report_generated_by": self.created_by,
            "consultation_note": "This analysis demonstrates the type of business intelligence Yasser's AI agency can provide to clients"
        }

def main():
    """Run the advanced customer data analyzer"""
    parser = argparse.ArgumentParser(description="🔍 Advanced Customer Data Analyzer MCP Server")
    parser.add_argument("--command", choices=["info", "segments", "churn", "revenue", "report"], 
                       default="info", help="Analysis to run")
    parser.add_argument("--data-dir", default="customer_data", help="Customer data directory")
    
    args = parser.parse_args()
    
    # Initialize analyzer
    analyzer = CustomerDataAnalyzerMCP(args.data_dir)
    
    print(f"🔍 {analyzer.name} v{analyzer.version}")
    print(f"👨‍💼 Created by: {analyzer.created_by}")
    print(f"📊 Advanced Customer Intelligence")
    print("=" * 50)
    
    if args.command == "info":
        info = analyzer.get_server_info()
        print(json.dumps(info, indent=2))
    
    elif args.command == "segments":
        analysis = analyzer.analyze_customer_segments()
        print(json.dumps(analysis, indent=2))
    
    elif args.command == "churn":
        analysis = analyzer.predict_customer_churn()
        print(json.dumps(analysis, indent=2))
    
    elif args.command == "revenue":
        analysis = analyzer.optimize_revenue_opportunities()
        print(json.dumps(analysis, indent=2))
    
    elif args.command == "report":
        report = analyzer.generate_executive_report()
        print(json.dumps(report, indent=2))
    
    print("\n🎯 This analysis demonstrates the AI consulting value you can provide to clients!")
    print("💼 Perfect for showcasing your data analysis capabilities!")

if __name__ == "__main__":
    main()