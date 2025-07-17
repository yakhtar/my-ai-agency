#!/usr/bin/env python3
"""
📅 Daily Action Tracker for AI Agency Launch
Track your daily progress toward landing your first $10K+ client

This system keeps you accountable and focused on revenue-generating activities.
"""

import json
import sys
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime, timedelta
import argparse

class DailyActionTracker:
    """
    📅 Daily Action Tracker for AI Agency Success
    
    This system tracks your daily activities to ensure you're
    consistently working toward your first client.
    """
    
    def __init__(self):
        self.name = "daily_action_tracker"
        self.version = "1.0.0"
        self.consultant = "Yasser Akhtar"
        self.goal = "Land first $10K+ AI consulting client"
        self.timeline = "30 days"
        
        # Progress tracking
        self.progress_file = Path("daily_progress.json")
        self.progress_data = self.load_progress()
        
        # Today's action items
        self.todays_actions = self.get_todays_actions()
    
    def load_progress(self) -> Dict[str, Any]:
        """Load existing progress data"""
        if self.progress_file.exists():
            try:
                with open(self.progress_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            "start_date": datetime.now().isoformat(),
            "goal": self.goal,
            "timeline": self.timeline,
            "daily_logs": {},
            "contacts_made": 0,
            "demos_scheduled": 0,
            "proposals_sent": 0,
            "revenue_generated": 0,
            "confidence_level": 8
        }
    
    def save_progress(self):
        """Save progress data"""
        try:
            with open(self.progress_file, 'w') as f:
                json.dump(self.progress_data, f, indent=2)
        except Exception as e:
            print(f"⚠️ Couldn't save progress: {e}")
    
    def get_todays_actions(self) -> Dict[str, Any]:
        """Get today's specific action items"""
        today = datetime.now()
        day_number = (today - datetime.fromisoformat(self.progress_data["start_date"])).days + 1
        
        if day_number == 1:
            return {
                "day": 1,
                "focus": "Foundation Launch",
                "priority_actions": [
                    "🚀 Start Zaika AI demo server (python simple_zaika_deployment.py)",
                    "📧 Update LinkedIn profile with new AI consultant resume",
                    "📝 Create list of 20 professional contacts to reach out to",
                    "🎯 Research 5 local restaurants for potential demos",
                    "📚 Study SFMC for 1 hour (Email Studio fundamentals)"
                ],
                "outreach_targets": [
                    "Former colleagues who might need AI solutions",
                    "Professional contacts in target industries",
                    "Local business owners in your network",
                    "LinkedIn connections who run SMBs"
                ],
                "success_metrics": [
                    "Demo server running successfully",
                    "LinkedIn profile updated",
                    "5 meaningful conversations initiated",
                    "2 demo meetings scheduled",
                    "SFMC study session completed"
                ],
                "revenue_activities": [
                    "Identify 3 businesses that could use AI customer service",
                    "Practice demo presentation with Zaika bot",
                    "Draft outreach messages for different industries",
                    "Research pricing for each prospect type"
                ]
            }
        
        elif day_number <= 7:
            return {
                "day": day_number,
                "focus": "Network Activation & Demo Scheduling",
                "priority_actions": [
                    "📞 Contact 5 people from your professional network",
                    "📧 Send 3 personalized LinkedIn messages to prospects",
                    "🎬 Conduct 1-2 demo presentations",
                    "🔍 Research 3 new potential clients",
                    "📚 Continue SFMC study (30 minutes daily)"
                ],
                "outreach_targets": [
                    "Restaurant owners and managers",
                    "Professional services firms",
                    "Healthcare practice managers",
                    "E-commerce business owners"
                ],
                "success_metrics": [
                    "10 new contacts reached this week",
                    "3 demo presentations completed",
                    "2 qualified prospects identified",
                    "1 proposal request received"
                ],
                "revenue_activities": [
                    "Follow up on previous day's outreach",
                    "Qualify prospects for budget and timeline",
                    "Customize demo for each industry",
                    "Prepare proposals for interested prospects"
                ]
            }
        
        elif day_number <= 14:
            return {
                "day": day_number,
                "focus": "Demo Presentations & Proposal Generation",
                "priority_actions": [
                    "📊 Present 2-3 demos to qualified prospects",
                    "📋 Prepare custom proposals for interested clients",
                    "📞 Follow up on previous demos and conversations",
                    "🎯 Continue prospecting for pipeline development",
                    "📈 Track and analyze demo conversion rates"
                ],
                "success_metrics": [
                    "50% demo acceptance rate",
                    "2 proposals sent",
                    "1 client ready to sign",
                    "Pipeline of 5+ qualified prospects"
                ]
            }
        
        elif day_number <= 21:
            return {
                "day": day_number,
                "focus": "Closing & Contract Negotiation",
                "priority_actions": [
                    "💼 Present proposals to qualified prospects",
                    "🤝 Negotiate terms and handle objections",
                    "📑 Prepare contracts and agreements",
                    "🔄 Continue pipeline development",
                    "📊 Analyze and optimize sales process"
                ],
                "success_metrics": [
                    "First contract signed",
                    "Revenue target achieved",
                    "Referral system activated",
                    "Second client in pipeline"
                ]
            }
        
        else:
            return {
                "day": day_number,
                "focus": "Project Execution & Pipeline Management",
                "priority_actions": [
                    "⚙️ Begin first client project",
                    "🔄 Maintain prospect pipeline",
                    "📈 Document success metrics",
                    "🎯 Plan referral strategy",
                    "📚 Continue skill development"
                ],
                "success_metrics": [
                    "First project successfully launched",
                    "Client satisfaction > 90%",
                    "Referrals generated",
                    "Second client contracted"
                ]
            }
    
    def log_daily_activity(self, activities_completed: List[str], contacts_made: int, 
                          demos_scheduled: int, revenue_generated: float, 
                          confidence_level: int, notes: str = "") -> Dict[str, Any]:
        """Log daily activities and progress"""
        
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Update daily log
        self.progress_data["daily_logs"][today] = {
            "date": today,
            "activities_completed": activities_completed,
            "contacts_made": contacts_made,
            "demos_scheduled": demos_scheduled,
            "revenue_generated": revenue_generated,
            "confidence_level": confidence_level,
            "notes": notes,
            "logged_at": datetime.now().isoformat()
        }
        
        # Update cumulative metrics
        self.progress_data["contacts_made"] += contacts_made
        self.progress_data["demos_scheduled"] += demos_scheduled
        self.progress_data["revenue_generated"] += revenue_generated
        self.progress_data["confidence_level"] = confidence_level
        
        self.save_progress()
        
        # Calculate progress metrics
        days_active = len(self.progress_data["daily_logs"])
        total_contacts = self.progress_data["contacts_made"]
        total_demos = self.progress_data["demos_scheduled"]
        total_revenue = self.progress_data["revenue_generated"]
        
        return {
            "day_logged": today,
            "activities_completed": len(activities_completed),
            "daily_metrics": {
                "contacts_made": contacts_made,
                "demos_scheduled": demos_scheduled,
                "revenue_generated": revenue_generated,
                "confidence_level": confidence_level
            },
            "cumulative_metrics": {
                "days_active": days_active,
                "total_contacts": total_contacts,
                "total_demos": total_demos,
                "total_revenue": total_revenue,
                "avg_contacts_per_day": round(total_contacts / days_active, 1) if days_active > 0 else 0,
                "demo_conversion_rate": round((total_demos / total_contacts) * 100, 1) if total_contacts > 0 else 0
            },
            "progress_assessment": self.assess_progress(),
            "tomorrow_focus": self.get_tomorrow_focus()
        }
    
    def assess_progress(self) -> Dict[str, Any]:
        """Assess current progress toward goal"""
        
        days_active = len(self.progress_data["daily_logs"])
        total_contacts = self.progress_data["contacts_made"]
        total_demos = self.progress_data["demos_scheduled"]
        total_revenue = self.progress_data["revenue_generated"]
        
        # Progress assessment
        if total_revenue >= 10000:
            status = "🎉 GOAL ACHIEVED!"
            message = "Congratulations! You've achieved your $10K+ client goal!"
        elif total_revenue >= 5000:
            status = "🚀 EXCELLENT PROGRESS"
            message = "You're well on your way to your goal!"
        elif total_demos >= 3:
            status = "📈 GOOD MOMENTUM"
            message = "Good demo activity - focus on closing!"
        elif total_contacts >= 20:
            status = "📞 BUILDING PIPELINE"
            message = "Great outreach volume - increase demo conversions!"
        elif days_active >= 7:
            status = "⚠️ NEEDS ACCELERATION"
            message = "Increase daily activity levels to hit your goal!"
        else:
            status = "🎯 GETTING STARTED"
            message = "Stay consistent with daily actions!"
        
        return {
            "status": status,
            "message": message,
            "days_active": days_active,
            "goal_progress": round((total_revenue / 10000) * 100, 1),
            "recommendations": self.get_recommendations()
        }
    
    def get_recommendations(self) -> List[str]:
        """Get personalized recommendations based on progress"""
        
        total_contacts = self.progress_data["contacts_made"]
        total_demos = self.progress_data["demos_scheduled"]
        total_revenue = self.progress_data["revenue_generated"]
        
        recommendations = []
        
        if total_contacts < 10:
            recommendations.append("📞 Increase outreach volume - aim for 5+ contacts daily")
        
        if total_demos < 3:
            recommendations.append("🎬 Focus on demo scheduling - that's where deals happen")
        
        if total_demos > 0 and total_revenue == 0:
            recommendations.append("💼 Improve demo-to-close conversion - practice objection handling")
        
        if total_revenue == 0 and len(self.progress_data["daily_logs"]) > 14:
            recommendations.append("🎯 Reassess target market - maybe focus on warmer prospects")
        
        recommendations.append("🌟 Your Zaika demo is your secret weapon - use it in every conversation!")
        
        return recommendations
    
    def get_tomorrow_focus(self) -> List[str]:
        """Get tomorrow's focus areas"""
        
        tomorrow_day = len(self.progress_data["daily_logs"]) + 1
        tomorrow_actions = self.get_todays_actions()
        
        return [
            f"📅 Day {tomorrow_day}: {tomorrow_actions['focus']}",
            "🎯 Priority: " + tomorrow_actions["priority_actions"][0],
            "📊 Track: Contacts made, demos scheduled, revenue generated",
            "🚀 Remember: Every conversation is an opportunity!"
        ]
    
    def get_weekly_summary(self) -> Dict[str, Any]:
        """Get weekly progress summary"""
        
        # Get last 7 days of data
        recent_logs = list(self.progress_data["daily_logs"].values())[-7:]
        
        if not recent_logs:
            return {"message": "No activity logged yet this week"}
        
        week_contacts = sum(log.get("contacts_made", 0) for log in recent_logs)
        week_demos = sum(log.get("demos_scheduled", 0) for log in recent_logs)
        week_revenue = sum(log.get("revenue_generated", 0) for log in recent_logs)
        
        return {
            "week_summary": {
                "days_active": len(recent_logs),
                "contacts_made": week_contacts,
                "demos_scheduled": week_demos,
                "revenue_generated": week_revenue,
                "avg_confidence": round(sum(log.get("confidence_level", 0) for log in recent_logs) / len(recent_logs), 1)
            },
            "weekly_goals": {
                "contacts_target": 25,
                "demos_target": 5,
                "revenue_target": 5000
            },
            "performance": {
                "contacts_performance": f"{(week_contacts/25)*100:.1f}%",
                "demos_performance": f"{(week_demos/5)*100:.1f}%",
                "revenue_performance": f"{(week_revenue/5000)*100:.1f}%"
            }
        }

def main():
    """Run the daily action tracker"""
    parser = argparse.ArgumentParser(description="📅 Daily Action Tracker")
    parser.add_argument("--command", choices=["today", "log", "progress", "weekly"], 
                       default="today", help="What to do")
    parser.add_argument("--activities", nargs="+", help="Activities completed today")
    parser.add_argument("--contacts", type=int, default=0, help="Contacts made today")
    parser.add_argument("--demos", type=int, default=0, help="Demos scheduled today")
    parser.add_argument("--revenue", type=float, default=0, help="Revenue generated today")
    parser.add_argument("--confidence", type=int, default=8, help="Confidence level (1-10)")
    parser.add_argument("--notes", default="", help="Additional notes")
    
    args = parser.parse_args()
    
    # Initialize tracker
    tracker = DailyActionTracker()
    
    print(f"📅 {tracker.name} v{tracker.version}")
    print(f"👨‍💼 Consultant: {tracker.consultant}")
    print(f"🎯 Goal: {tracker.goal}")
    print(f"⏰ Timeline: {tracker.timeline}")
    print("=" * 50)
    
    if args.command == "today":
        print("📋 Today's Action Plan:")
        print(json.dumps(tracker.todays_actions, indent=2))
    
    elif args.command == "log":
        if args.activities:
            result = tracker.log_daily_activity(
                args.activities, args.contacts, args.demos, 
                args.revenue, args.confidence, args.notes
            )
            print("✅ Daily Activity Logged:")
            print(json.dumps(result, indent=2))
        else:
            print("Please provide activities with --activities")
    
    elif args.command == "progress":
        assessment = tracker.assess_progress()
        print("📊 Progress Assessment:")
        print(json.dumps(assessment, indent=2))
    
    elif args.command == "weekly":
        summary = tracker.get_weekly_summary()
        print("📈 Weekly Summary:")
        print(json.dumps(summary, indent=2))
    
    print("\n🚀 Stay consistent! Your first $10K client is within reach!")

if __name__ == "__main__":
    main()