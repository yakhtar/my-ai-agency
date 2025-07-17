# Professional Zaika BBQ Grill AI Agent
# Elite Culinary Concierge System

import os
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Any, Type
import logging
from enum import Enum, auto
import urllib.parse
import difflib
import datetime

try:
    import anthropic
except ImportError:
    print("\n⚠️ Error: The 'anthropic' package is not installed. Please run 'pip install anthropic' and try again.")
    exit(1)

try:
    from dotenv import load_dotenv
except ImportError:
    print("\n⚠️ Error: The 'python-dotenv' package is not installed. Please run 'pip install python-dotenv' and try again.")
    exit(1)

# Optional: colorama for colored CLI output
try:
    from colorama import init as colorama_init, Fore, Style
    colorama_init()
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False
    class Fore:
        GREEN = ''
        CYAN = ''
        YELLOW = ''
        RED = ''
        RESET = ''
    class Style:
        BRIGHT = ''
        RESET_ALL = ''

# Optional: readline for command history
try:
    import readline
except ImportError:
    readline = None

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger("ZaikaBot")

# Load environment variables from .env file
env_path = Path(__file__).resolve().parent / '.env'
load_dotenv(dotenv_path=env_path)

class Intent(Enum):
    MENU_BROWSING = auto()
    BESTSELLERS = auto()
    DIETARY_SPECIFIC = auto()
    SPICE_CONCERN = auto()
    GROUP_DINING = auto()
    QUICK_SERVICE = auto()
    CULTURAL_CURIOSITY = auto()
    VALUE_SEEKING = auto()
    GENERAL_INQUIRY = auto()

class ZaikaAIAgent:
    # Centralized typo correction dictionary
    CORRECTIONS = {
        'biriyani': 'biryani', 'biriani': 'biryani', 'briyani': 'biryani',
        'kabob': 'kabab', 'kebab': 'kabab', 'kabeb': 'kabab',
        'tikka': 'tikka', 'tika': 'tikka', 'teeka': 'tikka',
        'naan': 'naan', 'nan': 'naan', 'nann': 'naan',
        'daal': 'dal', 'dhal': 'dal', 'dhaal': 'dal',
        'chiken': 'chicken', 'chikken': 'chicken', 'checken': 'chicken',
        'vegitarian': 'vegetarian', 'vegeterian': 'vegetarian',
        'spicey': 'spicy', 'spiccy': 'spicy',
        'protien': 'protein', 'protine': 'protein',
        'helathy': 'healthy', 'healty': 'healthy',
        'diabetik': 'diabetic', 'diabetic': 'diabetic',
        'wieght': 'weight', 'waight': 'weight',
        'recomend': 'recommend', 'recomendation': 'recommendation',
        'favrite': 'favorite', 'favourite': 'favorite'
    }

    ABOUT = (
        "Zaika is a family owned business in Edison, New Jersey, serving the finest Pakistani cuisine. "
        "From exquisitely spiced curries to a tantalizing BBQ mixed grill and sizzling Lamb Chops, each dish has forged its place in history. "
        "Zaika’s friendly atmosphere, attentive service, and affordable prices will keep you coming back again and again."
    )

    BUSINESS_HOURS = (
        "Monday – Thursday: 11am-10pm\n"
        "Friday – Sunday: 11am-10pm"
    )

    GOOGLE_PROFILE = {
        'name': 'Zaika BBQ & Grill',
        'category': 'Pakistani restaurant',
        'address': '1199 Amboy Ave, Edison, NJ 08837',
        'phone': '(732) 709-3700',
        'website': 'https://zaikabbqgrill.com/',
        'google_maps': 'https://goo.gl/maps/ZaikaBBQGrill',
        'hours': '11am–10pm daily',
        'price_range': '$$',
        'rating': 4.5,
        'review_count': 800,
        'social_media': {
            'facebook': 'https://facebook.com/zaikabbqgrill',
            'instagram': '@zaikabbqgrill'
        },
        'popular_for': [
            'Dine-in', 'Takeout', 'Delivery', 'Family-friendly', 'Vegetarian options'
        ],
        'popular_times': 'Busy on weekends, especially 6–8pm',
        'review_snippets': [
            'Amazing food and great service! The BBQ platter is a must-try.',
            'Authentic Pakistani flavors, generous portions, and friendly staff.',
            'Best biryani in Edison. Will definitely come back!',
            'Vegetarian options are delicious and filling.'
        ]
    }

    # Expanded mapping of user keywords to menu/dietary tags
    INTENT_KEYWORDS = {
        'vegetarian': ['veg', 'vegetarian', 'veggie', 'plant-based'],
        'vegan': ['vegan', 'plant-based', 'no dairy', 'no eggs'],
        'gluten-free': ['gluten free', 'gluten-free', 'no gluten'],
        'halal': ['halal'],
        'protein': ['protein', 'high protein', 'muscle', 'workout'],
        'low-carb': ['low carb', 'keto', 'no carbs', 'low sugar'],
        'spicy': ['spicy', 'hot', 'fire', 'chili', 'pepper'],
        'mild': ['mild', 'not spicy', 'kids', 'children', 'sensitive'],
        'seafood': ['fish', 'seafood', 'shrimp', 'prawn'],
        'meat': ['non-veg', 'meat', 'chicken', 'lamb', 'beef', 'goat', 'kabab', 'boti', 'chop', 'seekh', 'tikka', 'wings'],
        'dessert': ['dessert', 'sweet', 'mithai', 'kheer', 'gulab', 'jalebi', 'halwa', 'rasmalai'],
        'drink': ['drink', 'beverage', 'lassi', 'chai', 'tea', 'juice', 'soda', 'coffee', 'sharbat'],
        'bbq': ['bbq', 'barbecue', 'grill', 'tandoori', 'tandoor', 'smoked'],
        'biryani': ['biryani', 'rice', 'pulao'],
        'kids': ['kids', 'children', 'child', 'family', 'mild'],
        'healthy': ['healthy', 'light', 'low calorie', 'diet', 'fresh', 'salad', 'soup'],
        'family': ['family', 'group', 'sharing', 'platter', 'combo'],
        'nut-free': ['nut free', 'nut-free', 'no nuts', 'allergy'],
        'dairy-free': ['dairy free', 'dairy-free', 'no dairy', 'lactose'],
        'comfort': ['comfort', 'comfort food', 'home style', 'homestyle', 'classic', 'traditional'],
        'street': ['street food', 'chaat', 'pakora', 'samosa', 'roll', 'wrap'],
        'chef': ["chef's special", 'special', 'signature', 'exclusive'],
        'breakfast': ['breakfast', 'morning', 'paratha', 'chai', 'omelette'],
        'lunch': ['lunch', 'midday', 'noon'],
        'dinner': ['dinner', 'evening', 'night'],
        'brunch': ['brunch', 'late morning'],
        'appetizer': ['appetizer', 'starter', 'snack', 'small plate'],
        'soup': ['soup', 'shorba'],
        'salad': ['salad', 'greens'],
        'curry': ['curry', 'masala', 'korma', 'karahi'],
        'grill': ['grill', 'grilled', 'tandoor', 'bbq'],
        'rice': ['rice', 'biryani', 'pulao'],
        'bread': ['bread', 'naan', 'roti', 'paratha', 'kulcha'],
        'paratha': ['paratha'],
        'naan': ['naan'],
        'roti': ['roti'],
        'festive': ['festive', 'holiday', 'eid', 'ramadan', 'diwali', 'celebration', 'party', 'special occasion'],
        'seasonal': ['seasonal', 'season', 'fresh', 'in season'],
        'summer': ['summer', 'hot day', 'warm', 'sunny'],
        'winter': ['winter', 'cold', 'chilly', 'snow', 'rainy', 'monsoon'],
        'refreshing': ['refreshing', 'cooling', 'cold drink', 'iced'],
        'warming': ['warming', 'hot', 'spicy', 'comfort'],
        'hearty': ['hearty', 'rich', 'filling', 'robust'],
        'light': ['light', 'fresh', 'not heavy', 'simple'],
        'crunchy': ['crunchy', 'crispy'],
        'creamy': ['creamy', 'rich', 'smooth'],
        'tangy': ['tangy', 'sour', 'zesty'],
        'savory': ['savory', 'umami'],
        'sweet': ['sweet', 'dessert', 'mithai'],
    }

    def __init__(self, claude_client: Optional[Any] = None):
        """Initialize the professional Zaika AI Agent"""
        self.restaurant_name = "Zaika BBQ Grill"
        self.location = "1199 Amboy Ave, Edison, NJ 08837"
        self.phone = "(732) 709-3700"
        self.email = "zaika@zaikabbqgrill.com"
        self.cuisine_type = "Authentic Pakistani & Indian Cuisine"
        self.website = "https://zaikabbqgrill.com"
        self.instagram = "@zaikabbqgrill"
        self.business_hours = self.BUSINESS_HOURS
        self.about = self.ABOUT
        self.claude_client = claude_client or self._init_claude_client()
        self.menu_data = self._load_json_data('menu.json', self._default_menu_data())
        self.price_range = self.GOOGLE_PROFILE['price_range']
        self.rating = self.GOOGLE_PROFILE['rating']
        self.google_maps = self.GOOGLE_PROFILE['google_maps']
        self.review_count = self.GOOGLE_PROFILE['review_count']
        self.social_media = self.GOOGLE_PROFILE['social_media']
        self.popular_times = self.GOOGLE_PROFILE['popular_times']
        self.review_insights = self._load_json_data('reviews.json', self._default_review_insights())
        # Add Google review snippets to review_insights
        self.review_insights['top_praise'].extend(self.GOOGLE_PROFILE['review_snippets'])
        self.trending_dishes = self._load_json_data('trending.json', self._default_trending_dishes())

    def _init_claude_client(self):
        try:
            return anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        except Exception as e:
            logger.warning(f"Claude client initialization failed: {e}")
            return None

    def _load_json_data(self, filename: str, fallback):
        path = Path(__file__).resolve().parent / filename
        if path.exists():
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load {filename}: {e}")
        return fallback

    @staticmethod
    def _default_menu_data() -> Dict:
        return {
            'specialties': {
                'name': 'Our Specialties',
                'description': 'Signature dishes that define Zaika BBQ Grill',
                'items': [
                    {
                        'name': 'Goat Paya',
                        'description': 'Traditional slow-cooked goat trotters in a rich, spiced broth. A delicacy for special occasions.',
                    },
                    {
                        'name': 'Beef Seekh Kabab',
                        'description': 'Juicy, spiced ground beef skewers grilled to perfection in the tandoor.',
                    },
                    {
                        'name': 'Daal Makhni',
                        'description': 'Slow-simmered black lentils and kidney beans in rich, creamy tomato curry - a vegetarian masterpiece.',
                    },
                    {
                        'name': 'Chicken Kabab Roll',
                        'description': 'Tender chicken kabab wrapped in fresh naan with house sauces.',
                    },
                    {
                        'name': 'Lamb Chops',
                        'description': 'Sizzling lamb chops marinated in Zaika’s signature spices and grilled to perfection.',
                    },
                ]
            },
            'signature_bestsellers': {
                'name': 'Signature Bestsellers',
                'description': 'Our most beloved dishes that define the Zaika experience',
                'items': [
                    {
                        'name': "Zaika's Chicken Mix Grill",
                        'price': '$19.95',
                        'description': 'Our crown jewel: Six distinct BBQ preparations on one platter - achari boti, malai boti, tikka boti, seekh kabab, bihari, and hariyali boti',
                        'calories': 650,
                        'spice_level': 'medium',
                        'dietary': ['halal', 'protein-rich', 'keto-friendly'],
                        'prep_time': '25 min',
                        'instagram_mentions': 847,
                        'customer_sentiment': 'Most Instagrammed dish - guests love the variety and presentation',
                        'pairing_suggestion': 'Pairs beautifully with our cooling Mint Lassi and Garlic Naan'
                    },
                    {
                        'name': 'Chicken Biryani',
                        'price': '$12.60',
                        'description': 'Aromatic basmati rice layered with tender marinated chicken, slow-cooked with traditional spices',
                        'calories': 580,
                        'spice_level': 'medium',
                        'dietary': ['halal'],
                        'prep_time': '30 min',
                        'instagram_mentions': 623,
                        'customer_sentiment': 'Comfort food favorite - reminds guests of home cooking',
                        'pairing_suggestion': 'Complete meal on its own, enhanced with cooling Raita'
                    },
                    {
                        'name': 'Dal Makhni',
                        'price': '$12.60',
                        'description': 'Slow-simmered black lentils and kidney beans in rich, creamy tomato curry - a vegetarian masterpiece',
                        'calories': 320,
                        'spice_level': 'mild',
                        'dietary': ['vegetarian', 'protein-rich'],
                        'prep_time': '20 min',
                        'instagram_mentions': 412,
                        'customer_sentiment': 'Converts even the most devoted meat-lovers',
                        'pairing_suggestion': 'Essential with fresh Butter Naan for the authentic experience'
                    }
                ]
            },
            'clay_oven_bbq': {
                'name': 'Clay Oven BBQ Specialties',
                'description': 'Authentic tandoor cooking at 900°F for that distinctive smoky char',
                'items': [
                    {
                        'name': 'Chicken Malai Boti',
                        'price': '$15.75',
                        'description': 'Cream-marinated chicken breast cubes, mild and luxuriously tender',
                        'calories': 380,
                        'spice_level': 'mild',
                        'dietary': ['halal', 'protein-rich', 'keto-friendly'],
                        'prep_time': '20 min',
                        'customer_sentiment': 'Perfect for spice-sensitive palates and children',
                        'cultural_note': 'Malai means cream in Hindi - this dish showcases the gentle side of Pakistani cuisine'
                    },
                    {
                        'name': 'Chicken Tikka Boti',
                        'price': '$15.75',
                        'description': 'Bold, aromatic chicken breast cubes with traditional red spice marinade',
                        'calories': 350,
                        'spice_level': 'medium',
                        'dietary': ['halal', 'protein-rich', 'keto-friendly'],
                        'prep_time': '20 min',
                        'customer_sentiment': 'The classic that represents authentic Pakistani flavors',
                        'cultural_note': 'Tikka refers to pieces or chunks - this is the dish that made Pakistani cuisine famous worldwide'
                    }
                ]
            },
            'comfort_curries': {
                'name': 'Comfort Curries',
                'description': 'Soul-warming dishes that embody Pakistani hospitality',
                'items': [
                    {
                        'name': 'Palak Paneer',
                        'price': '$12.60',
                        'description': 'Fresh spinach curry with soft paneer cubes - nutrition meets indulgence',
                        'calories': 290,
                        'spice_level': 'mild-medium',
                        'dietary': ['vegetarian', 'iron-rich'],
                        'prep_time': '18 min',
                        'health_benefits': 'Rich in iron, folate, and plant-based protein',
                        'customer_sentiment': 'Parents love it - kids actually eat their greens!'
                    },
                    {
                        'name': 'Lahori Channa',
                        'price': '$12.60',
                        'description': 'Chickpeas in robust tomato-onion gravy with warming Lahori spices',
                        'calories': 250,
                        'spice_level': 'medium',
                        'dietary': ['vegetarian', 'vegan', 'protein-rich', 'fiber-rich'],
                        'prep_time': '15 min',
                        'cultural_note': 'Named after Lahore, the cultural heart of Punjab - a street food classic',
                        'health_benefits': 'High fiber, plant protein, supports digestive health'
                    }
                ]
            },
            'beverages': {
                'name': 'Traditional Beverages',
                'description': 'Refreshing drinks that complement our bold flavors',
                'items': [
                    {
                        'name': 'Mango Lassi',
                        'price': '$5.25',
                        'description': 'Creamy yogurt drink blended with sweet mango - our Instagram star',
                        'calories': 180,
                        'spice_level': 'none',
                        'dietary': ['vegetarian', 'probiotic', 'vitamin-c'],
                        'prep_time': '5 min',
                        'customer_sentiment': 'Perfect spice antidote and photo opportunity',
                        'health_benefits': 'Probiotics for gut health, natural cooling effect'
                    },
                    {
                        'name': 'Kashmiri Chai',
                        'price': '$4.20',
                        'description': 'Pink tea from the Kashmir valley - delicate, aromatic, and Instagram-worthy',
                        'calories': 80,
                        'spice_level': 'none',
                        'dietary': ['vegetarian', 'antioxidants'],
                        'prep_time': '8 min',
                        'cultural_note': 'Also called Pink Tea - a traditional welcome drink in Kashmiri homes'
                    }
                ]
            }
        }
    
    @staticmethod
    def _default_review_insights() -> Dict:
        return {
            'top_praise': [
                'Authentic flavors that transport you to Pakistan',
                'Generous portions that easily feed 2-3 people',
                'Clay oven cooking creates amazing smoky flavors',
                'Staff genuinely cares about dietary restrictions',
                'Best Pakistani food in Edison/Central NJ area',
                'This gem of a restaurant can really satisfy your cravings. All the items were placed on time and were fresh. Needless to say, I have added this place to my favorites already. — Mumtaz Burki',
                'It has been a long time since we had authentic Pakistani Cuisine. Visiting Zaika was a good choice we made one fine evening. This place serves delicious food. We felt at home by the amazing service of the friendly staff who were polite and never took a step back to explain all about their menu. — Jawaid Qayyum'
            ],
            'trending_compliments': [
                'Instagram-worthy presentation',
                'Mild options perfect for kids',
                'Great value for money',
                'Accommodating to spice preferences'
            ],
            'common_questions_resolved': [
                'Yes, all meat is certified halal',
                'We can adjust spice levels for any dish',
                'Large portions - perfect for sharing',
                'Extensive vegetarian menu available',
                'Clay oven gives unique smoky flavor you can\'t get at home'
            ]
        }
    
    @staticmethod
    def _default_trending_dishes() -> List[str]:
        return [
            "Zaika's Chicken Mix Grill",
            "Mango Lassi",
            "Chicken Biryani", 
            "Dal Makhni",
            "Garlic Naan"
        ]

    def correct_and_understand_query(self, query: str) -> str:
        """Advanced query correction and intent understanding"""
        normalized_query = query.lower().strip()
        for wrong, correct in self.CORRECTIONS.items():
            normalized_query = normalized_query.replace(wrong, correct)
        return normalized_query

    def extract_intent_tags(self, query: str) -> List[str]:
        """Extract likely intent tags from user query using fuzzy matching."""
        tags = set()
        query_lower = query.lower()
        words = re.findall(r'\w+', query_lower)
        for tag, keywords in self.INTENT_KEYWORDS.items():
            for kw in keywords:
                # Fuzzy match each keyword to words in query
                matches = difflib.get_close_matches(kw, words, n=1, cutoff=0.8)
                if matches or kw in query_lower:
                    tags.add(tag)
        return list(tags)

    def analyze_customer_intent(self, query: str) -> Dict[str, Any]:
        """Sophisticated intent analysis with fuzzy and synonym matching"""
        corrected_query = self.correct_and_understand_query(query)
        tags = self.extract_intent_tags(corrected_query)
        intent_map = {
            Intent.MENU_BROWSING: [
                'menu', 'what do you have', 'what do you serve', 'options', 'choices'
            ],
            Intent.BESTSELLERS: [
                'best', 'popular', 'recommend', 'signature', 'famous', 'bestseller',
                "what's good", 'trending', 'must try', 'specialty'
            ],
            Intent.DIETARY_SPECIFIC: sum(self.INTENT_KEYWORDS.values(), []),
            Intent.SPICE_CONCERN: self.INTENT_KEYWORDS['spicy'] + self.INTENT_KEYWORDS['mild'],
            Intent.GROUP_DINING: ['party', 'group', 'family', 'people', 'sharing', 'catering'],
            Intent.QUICK_SERVICE: ['quick', 'fast', 'takeout', 'pickup', 'rush', 'lunch break'],
            Intent.CULTURAL_CURIOSITY: ['pakistani', 'indian', 'authentic', 'traditional', 'culture', 'clay oven'],
            Intent.VALUE_SEEKING: ['cheap', 'affordable', 'budget', 'value', 'deal', 'price']
        }
        detected = {intent: any(word in corrected_query for word in words) for intent, words in intent_map.items()}
        primary_intent = next((intent for intent, found in detected.items() if found), Intent.GENERAL_INQUIRY)
        return {
            'corrected_query': corrected_query,
            'primary_intent': primary_intent,
            'all_intents': [intent for intent, found in detected.items() if found],
            'confidence': 'high' if sum(detected.values()) >= 2 else 'medium' if sum(detected.values()) == 1 else 'low',
            'tags': tags
        }

    def generate_sophisticated_response(self, query: str) -> str:
        """Generate contextually intelligent, warm responses"""
        analysis = self.analyze_customer_intent(query)
        intent = analysis['primary_intent']
        corrected_query = analysis['corrected_query']
        tags = analysis.get('tags', [])
        # Route to specialized handlers
        handler_map = {
            Intent.BESTSELLERS: self._handle_bestsellers_inquiry,
            Intent.DIETARY_SPECIFIC: lambda q: self._handle_dietary_inquiry(q, tags),
            Intent.SPICE_CONCERN: self._handle_spice_inquiry,
            Intent.GROUP_DINING: self._handle_group_dining,
            Intent.CULTURAL_CURIOSITY: self._handle_cultural_inquiry,
            Intent.VALUE_SEEKING: self._handle_value_inquiry,
            Intent.QUICK_SERVICE: self._handle_quick_service,
            Intent.MENU_BROWSING: self._handle_menu_browsing,
            Intent.GENERAL_INQUIRY: self._handle_general_inquiry
        }
        handler = handler_map.get(intent, self._handle_general_inquiry)
        return handler(corrected_query)

    def _handle_bestsellers_inquiry(self, query: str) -> str:
        """Handle requests for popular/recommended items"""
        return """🌟 **Our guests can't stop talking about these!**

**🥇 Zaika's Chicken Mix Grill** - $19.95
The dish that's broken our Instagram! Six different BBQ preparations on one platter — it's like a tasting menu of our entire clay oven expertise. Perfect for adventurous eaters or when you simply can't decide.

**🥈 Chicken Biryani** - $12.60  
This week's most reordered dish. Guests tell us it reminds them of their grandmother's cooking — aromatic, comforting, and generous enough to share (though you might not want to!).

**🥉 Dal Makhni** - $12.60
Even our most devoted carnivores order this. Slow-simmered for hours until it's pure velvet. One guest called it "vegetarian comfort food that makes you forget about meat."

**🔥 This week's Instagram favorite:** Our Mango Lassi is having a moment — that perfect golden color photographs beautifully, and it's the ideal cooling companion to our bolder flavors.

**🎯 Can't decide?** The Mix Grill + Biryani + Garlic Naan combo has been ordered together 89 times this month. There's clearly something magical about that combination!

What type of flavors usually excite your palate? I'd love to personalize this further! 😊"""

    def _handle_dietary_inquiry(self, query: str, tags: Optional[List[str]] = None) -> str:
        """Handle dietary and preference-based inquiries with context awareness and clarification."""
        tags = tags or []
        menu = self.menu_data
        weather = self.get_current_weather()
        time_of_day = self.get_time_of_day()
        
        # Add weather/time/season tags
        if weather['season'] not in tags:
            tags.append(weather['season'])
        if weather['condition'] not in tags:
            tags.append(weather['condition'])
        if time_of_day not in tags:
            tags.append(time_of_day)
        
        # Check for specific beverage queries
        if any(word in query.lower() for word in ['beverage', 'drink', 'drinks', 'lassi', 'chai', 'tea', 'juice', 'soda', 'beverages']):
            return """🍹 **Our Refreshing Beverages:**

**🥭 Mango Lassi** - $5.25
Creamy yogurt drink blended with sweet mango - our Instagram star! Perfect for cooling down after spicy dishes.

**🌸 Kashmiri Chai** - $4.20  
Pink tea from the Kashmir valley - delicate, aromatic, and Instagram-worthy. A traditional welcome drink.

**🥛 Sweet Lassi** - $4.20
Classic yogurt drink - natural spice neutralizer and digestive aid.

**☕ Masala Chai** - $3.15
Spiced Indian tea with warming ginger and cardamom.

**Perfect for:** Cooling down spicy dishes, refreshing on hot days, or as a traditional accompaniment to any meal!"""
        
        # Check for specific salad queries
        if any(word in query.lower() for word in ['salad', 'salads', 'fresh', 'greens', 'vegetables', 'healthy']):
            return """🥗 **Fresh & Healthy Options:**

**🥬 Palak Paneer** - $12.60
Fresh spinach curry with soft paneer cubes - nutrition meets indulgence! Rich in iron and plant-based protein.

**🥒 Fresh Cucumber Raita** - $3.15
Cooling yogurt with fresh cucumber - perfect side dish and spice neutralizer.

**🌿 Mint Chutney** - $2.10
Fresh mint and cilantro chutney - cooling AND flavorful, even kids love it as a dip!

**Perfect for:** Light meals, cooling down spicy dishes, or adding fresh elements to your meal!"""
        
        # Check for specific vegetarian queries
        if any(word in query.lower() for word in ['vegetarian', 'veg', 'vegan', 'plant-based', 'vegetarian menu', 'complete vegetarian']):
            return """🌱 **Our Vegetarian Favorites:**

**🥬 Palak Paneer** - $12.60
Fresh spinach curry with soft paneer cubes - nutrition meets indulgence! Rich in iron and plant-based protein.

**🫘 Lahori Channa** - $12.60
Chickpeas in robust tomato-onion gravy with warming Lahori spices. High fiber, plant protein, supports digestive health.

**🫘 Dal Makhni** - $12.60
Slow-simmered black lentils and kidney beans in rich, creamy tomato curry - a vegetarian masterpiece!

**🥭 Mango Lassi** - $5.25
Creamy yogurt drink blended with sweet mango - perfect vegetarian beverage!

**Perfect for:** Vegetarian diets, protein-rich plant meals, or anyone looking for delicious meat-free options!"""
        
        # Check for specific dessert queries
        if any(word in query.lower() for word in ['dessert', 'sweet', 'mithai', 'kheer', 'gulab', 'jalebi', 'halwa']):
            return """🍰 **Sweet Endings:**

**🥭 Mango Lassi** - $5.25
Creamy yogurt drink blended with sweet mango - our Instagram star! Perfect dessert beverage.

**🌸 Kashmiri Chai** - $4.20
Pink tea from the Kashmir valley - delicate, aromatic, and Instagram-worthy. Sweet and refreshing.

**🍯 Sweet Lassi** - $4.20
Classic sweetened yogurt drink - natural dessert and digestive aid.

**Perfect for:** Ending your meal on a sweet note, cooling down after spicy dishes, or as a refreshing dessert!"""
        
        # Check for specific bread/naan queries
        if any(word in query.lower() for word in ['bread', 'naan', 'roti', 'paratha', 'kulcha']):
            return """🍞 **Fresh Breads from Our Clay Oven:**

**🧄 Garlic Naan** - $3.15
Fresh garlic naan - essential for scooping up curries and creating the perfect bite.

**🧈 Butter Naan** - $3.15
Classic butter naan - soft, fluffy, and perfect for any curry.

**🌿 Plain Naan** - $2.10
Simple, fresh naan - your spice safety net and curry companion.

**🥬 Paratha** - $3.15
Layered flatbread - perfect for breakfast or as a hearty bread option.

**Perfect for:** Scooping up curries, creating the perfect bite, or as a side to any dish!"""
        
        # Default dietary matching (existing logic)
        matched_dishes = []
        for section in menu.values():
            for item in section.get('items', []):
                item_text = (item.get('name','') + ' ' + item.get('description','')).lower()
                item_tags = set()
                for tag, keywords in self.INTENT_KEYWORDS.items():
                    if any(kw in item_text for kw in keywords):
                        item_tags.add(tag)
                # If any user tag matches item tags, include
                if any(tag in item_tags for tag in tags):
                    matched_dishes.append(item)
        
        if matched_dishes:
            reply = f"🍽️ **Here are some dishes matching your preferences ({', '.join(tags)}):**\n\n"
            for dish in matched_dishes:
                reply += f"• **{dish['name']}**: {dish.get('description','')[:120]}\n"
            # Add weather/time/seasonal suggestion
            reply += f"\n{self.get_personalized_suggestion(tags, weather, time_of_day)}"
            return reply + "\nWould you like to refine your search (e.g., vegan, gluten-free, spicy, etc.)?"
        
        # If ambiguous, ask for clarification
        if not tags:
            return ("Could you clarify what you're looking for? For example: vegetarian, vegan, gluten-free, spicy, mild, healthy, BBQ, dessert, drink, etc. "
                    "We offer a wide range of options and I'd love to recommend the perfect dishes for you!")
        
        # Fallback
        return "I'm sorry, I couldn't find matching dishes. Could you specify your preference (e.g., vegan, spicy, gluten-free, etc.)?"

    def get_current_weather(self) -> dict:
        """Stub for weather awareness. Returns a simulated weather/season context for recommendations."""
        # In production, integrate with a weather API. Here, return a plausible default.
        now = datetime.datetime.now()
        month = now.month
        if month in [12, 1, 2]:
            season = 'winter'
            condition = 'cold'
        elif month in [6, 7, 8]:
            season = 'summer'
            condition = 'hot'
        else:
            season = 'spring' if month in [3, 4, 5] else 'fall'
            condition = 'mild'
        return {'season': season, 'condition': condition}

    def get_time_of_day(self) -> str:
        """Stub for time-of-day awareness. Returns breakfast, lunch, dinner, or late night."""
        now = datetime.datetime.now().hour
        if 5 <= now < 11:
            return 'breakfast'
        elif 11 <= now < 16:
            return 'lunch'
        elif 16 <= now < 22:
            return 'dinner'
        else:
            return 'late night'

    def get_personalized_suggestion(self, tags, weather, time_of_day):
        """Return a personalized suggestion string based on tags, weather, and time of day."""
        # Weather-based
        if weather['condition'] == 'cold':
            return "It's chilly outside—our hot Kashmiri Chai, creamy Dal Makhni, or sizzling BBQ platters are perfect for warming up!"
        elif weather['condition'] == 'hot':
            return "It's a warm day—try our refreshing Mango Lassi, cooling Raita, or light salads and grilled items."
        elif weather['season'] == 'summer':
            return "Summer calls for our chilled drinks, fresh salads, and lighter grilled dishes."
        elif weather['season'] == 'winter':
            return "Winter is perfect for hearty curries, hot naan, and warming chai."
        # Time of day
        if time_of_day == 'breakfast':
            return "Looking for breakfast? Our parathas, chai, and omelettes are a great start to your day."
        elif time_of_day == 'lunch':
            return "For lunch, our biryanis, BBQ platters, and fresh breads are very popular."
        elif time_of_day == 'dinner':
            return "Dinner at Zaika is best enjoyed with our signature curries, tandoori specials, and decadent desserts."
        elif time_of_day == 'late night':
            return "Late night cravings? Try our kabab rolls, pakoras, or a soothing cup of chai."
        # Festive/holiday
        if 'festive' in tags or 'holiday' in tags:
            return "Celebrating something special? Our chef's specials and festive platters are perfect for the occasion!"
        return "Let me know if you have a specific craving or occasion in mind!"

    def _handle_spice_inquiry(self, query: str) -> str:
        """Handle spice level concerns"""
        if any(word in query for word in ['mild', 'not spicy', 'kids', 'children', 'sensitive']):
            return """😊 **Perfect for Sensitive Palates** (We've got you covered!)

**🥛 Start here:** Sweet Lassi or Mango Lassi — natural spice neutralizers that also happen to be delicious!

**🍗 Safest bets:**
• **Chicken Malai Boti** - $15.75 (Cream-based, virtually no heat)
• **Dal Makhni** - $12.60 (Rich and comforting, gentle spices)  
• **Plain Rice** - $6.30 (Your spice safety net!)

**👨‍👩‍👧‍👦 Family dining wisdom:** Order one mild dish per spice-sensitive person, then add medium dishes for the adventurous ones. Everyone shares, everyone's happy!

**🔧 Customization magic:** Our chefs can make ANY curry mild — just mention it when ordering. We're talking "basically cream sauce with a whisper of authentic flavor."

**🍞 Emergency spice relief:** Naan bread, yogurt-based dishes, and our fresh cucumber raita work like culinary fire extinguishers.

**✨ Secret weapon:** Ask for our mint chutney on the side — cooling AND flavorful, even kids love it as a dip!

Would you like suggestions for a mixed spice-level meal where everyone at your table stays comfortable? 👨‍👩‍👧‍👦"""

        elif any(word in query for word in ['spicy', 'hot', 'fire', 'challenge']):
            return """🔥 **Spice Challenge Accepted!** (Bring the heat!)

**🌶️ Our spiciest regular items:**
• **Chicken Wings** - $9.45 (Our kitchen's spice showcase)
• **Karahi dishes** (when available) — traditional high-heat cooking
• **Extra spicy anything** — just ask! Our chefs love a challenge

**🔥 How to level up ANY dish:**
• Request "Pakistani spicy" — this signals authentic heat levels
• Ask for fresh green chilies on the side
• Order our house-made spicy chutneys

**💡 Spice veteran tips:**
• Start with medium, then add heat — easier than cooling down
• Order Lassi as backup (you might need it!)
• Our clay oven gives dishes a different kind of heat — smoky vs. just spicy

**🏆 The ultimate test:** Ask our chef to "make it as spicy as you would for your own family." That's when the real Pakistani heat comes out!

**🥵 Fair warning:** We take spice seriously here. Our "mild" might be other restaurants' "medium." Our "extra spicy" has made grown men cry happy tears.

How adventurous are you feeling? I can guide you to the perfect heat level! 🌶️🔥"""

        return """🌶️ **Spice Level Navigator** 

**Mild:** Creamy, aromatic, kid-friendly  
**Medium:** Traditional Pakistani spicing — flavorful with gentle warmth  
**Hot:** Authentic heat that Pakistani families enjoy  
**Extra Hot:** Challenge level — order with backup lassi! 

What's your usual spice comfort zone? I'll guide you perfectly! 😊"""

    def _handle_group_dining(self, query: str) -> str:
        """Handle party planning and group dining"""
        return """🎉 **Group Dining Made Effortless!** 

**🎯 Party Size Guidance:**

**4-6 People (Intimate Gathering):**
• Zaika's Mix Grill + Chicken Biryani + Vegetable option + Bread basket
• **Budget:** ~$75 | **Why:** Variety covers all tastes, built-in sharing

**8-12 People (Family Celebration):**  
• Family Platter + 2 Biryanis (different proteins) + Dal Makhni + Bread selection
• **Budget:** ~$150 | **Why:** Accommodates dietary preferences, generous portions

**15+ People (Major Event):**
• **Call us directly:** (732) 709-3700 — we create custom packages with 24-hour notice
• **Catering available:** We'll bring the clay oven magic to your location!

**🎈 Party Success Formula:**
✅ **Mix spice levels:** Mild + Medium + "Ask for extra spicy" options  
✅ **Protein variety:** Chicken + Vegetarian (covers 95% of preferences)  
✅ **Bread strategy:** Mix of plain, garlic, and specialty naans  
✅ **Cooling elements:** Multiple lassis — they're Instagram gold too!

**💡 Pro party tip:** Order 20% more than you think you need. Pakistani hospitality means generous portions, and happy guests with full plates create the best memories.

**🍰 Special occasions?** Let us know — we love making birthdays, anniversaries, and celebrations extra special!

What's the occasion and how many flavor adventurers are we feeding? 🎊"""

    def _handle_cultural_inquiry(self, query: str) -> str:
        """Handle questions about Pakistani culture and authenticity"""
        return """🇵🇰 **Authentic Pakistani Culinary Journey**

**🔥 The Clay Oven Difference:**
Our tandoor reaches 900°F — this isn't just cooking, it's culinary alchemy! That distinctive smoky char and tender-yet-crispy texture? Impossible to replicate at home.

**🌟 What Makes Us Authentically Pakistani:**
• **Family recipes** passed down three generations
• **Traditional techniques** — our dal simmers for hours, biryani is layered by hand
• **Cultural hospitality** — guests are family, dietary needs are honored
• **Halal commitment** — not just certified, but prepared with cultural understanding

**🎨 The Art of Pakistani Spicing:**
Each spice serves a purpose beyond flavor:
• **Turmeric:** Anti-inflammatory golden magic  
• **Cumin:** Digestive aid that's iron-rich  
• **Ginger & Garlic:** The foundation of Pakistani cooking  
• **Garam Masala:** Our signature blend (literally "warm spices")

**🍽️ Eating Pakistani Style:**
• **Sharing is caring** — dishes are meant for communal enjoyment
• **Bread as utensil** — naan isn't just a side, it's how you scoop and savor
• **Balance is key** — pair rich curries with cooling yogurt-based items

**💚 The Philosophy:**
Pakistani cuisine believes food should nourish both body and soul. Every meal should feel like a celebration, every guest should feel welcomed.

**✨ Want the full cultural experience?** Ask your server about the traditional way to eat each dish — there are stories behind every preparation!

What aspect of Pakistani culture through food interests you most? 🌶️✨"""

    def _handle_value_inquiry(self, query: str) -> str:
        """Handle budget-conscious inquiries"""
        return """💰 **Outstanding Value Without Compromise!**

**🏆 Maximum Impact, Minimum Spend:**

**🍛 The Biryani Strategy** (Feeds 2-3 people each):
• **Chicken Biryani** - $12.60 (Complete meal in one dish!)
• **Vegetable Biryani** - $10.50 (Surprisingly filling and flavorful)
• Add plain naan ($3.15) to stretch it even further

**🌱 Vegetarian Value Bombs:**
• **Dal Makhni** - $12.60 (Protein-packed, incredibly satisfying)
• **Lahori Channa** - $12.60 (Street food favorite, huge portions)
• **Perfect combo:** Dal + Rice + Naan = $21.90 for 2-3 people

**💡 Value Hacking Strategies:**
✅ **Share appetizers** — our pakoras are generous and meant for sharing
✅ **Biryanis are shareable** — seriously, they're huge!
✅ **Plain vs. specialty** naan saves $1-3 without sacrificing satisfaction
✅ **Lunch portions** — ask if available (smaller plates, smaller prices)

**🎯 Ultimate Budget Combo** (Feeds family of 4 for $45):
• Chicken Biryani + Vegetable Biryani + Dal Makhni + 4 Plain Naan
• Result: Everyone eats well + likely leftovers!

**💰 Money-saving secrets:**
• Our portions are American-generous with Pakistani soul
• Vegetarian dishes offer same quality spicing at lower cost  
• One biryani + one curry + bread = feast for 2-3 people

**📞 Budget tip:** Call ahead — we sometimes have daily specials not advertised online!

What's your target budget? I can create a feast plan that'll surprise you! 💚"""

    def _handle_quick_service(self, query: str) -> str:
        """Handle quick meal and takeout inquiries"""
        return """⚡ **Quick Service Without Sacrificing Soul!**

**🚀 Ready in 10-15 Minutes:**
• **Chicken Shami Kabab** - $7.35 (12 min — pre-made perfection)
• **Vegetable Pakora** - $7.35 (10 min — from fryer to your hands)
• **Any Naan** - $3.15-$6.30 (8 min clay oven magic)
• **Lassi** - $5.25 (2 min fresh blend)

**🍽️ Complete Quick Meals:**
• **Kabab Roll** - $5.25 (10 min wrapped convenience)
• **Dal + Rice** combo (12 min — we always have dal ready)
• **Pre-made Biryani** + Naan (15 min if available — ask!)

**⏰ Lunch Break Specials:**
• **Express Combo:** Kabab Roll + Masala Soda = $10.50 (8 minutes!)
• **Power Lunch:** Chicken Shami + Lassi = $12.60 (protein + probiotics!)
• **Veggie Quick:** Pakora + Naan + Tea = $13.50 (satisfying + warming)

**💡 Time-Saving Hacks:**
✅ **Call ahead:** (732) 709-3700 — we'll have it ready for pickup!
✅ **Ask about pre-made items** — biryani and dal are often ready to go
✅ **Appetizers as mains** — totally acceptable and filling!
✅ **Mobile payment** — speeds up the pickup process

**📱 Even faster:** Check if we have online ordering for pickup!

**⚡ Our promise:** Even our "fast" food maintains authentic flavors and quality. No shortcuts on taste, just efficiency in service!

How tight is your timeline? I can optimize your order for maximum speed! ⏰"""

    def _handle_menu_browsing(self, query: str) -> str:
        """Handle general menu exploration"""
        return """🍽️ **Welcome to Zaika's Culinary Universe!**

**🌟 First-time visitor? Start here:**

**🏆 Our Greatest Hits:**
• **Zaika's Chicken Mix Grill** - $19.95 (Six BBQ styles, one epic platter)
• **Chicken Biryani** - $12.60 (Comfort food perfection)  
• **Dal Makhni** - $12.60 (Vegetarian magic that converts meat-lovers)

**🔥 By Cooking Style:**
**Clay Oven BBQ** — Smoky, charred perfection at 900°F  
**Slow-Simmered Curries** — Rich, complex flavors developed over hours  
**Aromatic Rice** — Basmati perfection with traditional layering  
**Fresh Breads** — Hot from the tandoor, essential for the full experience

**💡 Choose Your Adventure:**
• **"Surprise me with your bestseller"** → Mix Grill experience
• **"I want comfort food"** → Biryani + Dal + Naan trinity
• **"Make it healthy"** → Grilled proteins + vegetable curries
• **"I'm spice-curious"** → Progressive heat journey from mild to bold
• **"Feed my family"** → Sharing platters with variety

**🎯 Tell me more specifically:**
• **Protein preference?** (Chicken, vegetarian, mixed)
• **Spice comfort zone?** (Mild, medium, bring-the-heat)  
• **Dining style?** (Quick bite, leisurely feast, family sharing)
• **Dietary needs?** (We accommodate everything!)

**🌶️ Cultural Note:** Pakistani cuisine is about balance — rich with cooling, spicy with mild, protein with vegetables. Every meal tells a story!

What type of culinary adventure calls to you today? I'm here to craft your perfect Zaika experience! ✨"""

    def get_directions_link(self, user_location: str) -> str:
        """Generate a Google Maps directions link from user_location to the restaurant."""
        base_url = "https://www.google.com/maps/dir/?api=1"
        destination = urllib.parse.quote_plus(self.location)
        origin = urllib.parse.quote_plus(user_location)
        return f"{base_url}&origin={origin}&destination={destination}"

    def _handle_general_inquiry(self, query: str) -> str:
        """Handle general questions and provide intelligent responses"""
        import re
        # Directions pattern: look for 'directions from', 'how do I get there from', 'route from', 'navigate from', or a zip code/address
        directions_patterns = [
            r"directions from (.+)",
            r"how do i get there from (.+)",
            r"route from (.+)",
            r"navigate from (.+)",
            r"from ([\w\s,\-]+\d{5})",  # e.g., from 08837 or from 123 Main St, Edison, NJ 08837
        ]
        for pat in directions_patterns:
            match = re.search(pat, query, re.IGNORECASE)
            if match:
                user_location = match.group(1).strip()
                link = self.get_directions_link(user_location)
                return f"Here are directions from '{user_location}' to Zaika BBQ & Grill:\n{link}\n\nSafe travels! 🚗"
        # If the query is just a zip code (5 digits) or looks like an address, treat as directions
        zip_code_match = re.fullmatch(r"\d{5}", query.strip())
        address_match = re.search(r"\d+\s+\w+.*(street|st\.|road|rd\.|avenue|ave\.|blvd|lane|ln\.|drive|dr\.|court|ct\.|circle|cir\.|plaza|plz\.|parkway|pkwy\.|way|terrace|ter\.|place|pl\.|trail|trl\.|highway|hwy\.|route|rt\.)", query.strip(), re.IGNORECASE)
        if zip_code_match or address_match:
            user_location = query.strip()
            link = self.get_directions_link(user_location)
            return f"Here are directions from '{user_location}' to Zaika BBQ & Grill:\n{link}\n\nSafe travels! 🚗"
        if any(word in query for word in ['about', 'who are you', 'your story', 'history']):
            return f"{self.about}\n\n📍 Address: {self.location}\n📞 Phone: {self.phone}\n✉️ Email: {self.email}\n🕒 Hours: {self.business_hours}\n🌐 Website: {self.website}"
        if any(word in query for word in ['hours', 'time', 'open', 'close']):
            return f"⏰ **Zaika BBQ Grill Hours & Contact**\n\n📍 **Location:** {self.location}\n📞 **Phone:** {self.phone}\n✉️ **Email:** {self.email}\n\n🕐 **Business Hours:**\n{self.business_hours}\n\n🚚 **Service Options:**\n✅ **Dine-in** — Full restaurant experience with clay oven aromas\n✅ **Pickup** — Ready in 15-20 minutes (call ahead!)  \n✅ **Delivery** — Available in Edison and surrounding areas\n✅ **Catering** — Custom packages with 24-hour notice\n\n💡 **Pro tip:** Call {self.phone} to confirm hours, place advance orders, or discuss dietary customizations!\n\nReady to experience authentic Pakistani flavors? What sounds delicious today? 😊"
        if any(word in query for word in ['location', 'address', 'directions']):
            return f"📍 **Find Us Easily!**\n\n🏢 **Address:** {self.location}\n📞 **Phone:** {self.phone}\n✉️ **Email:** {self.email}\n\n🚗 **Getting Here:**\n• **From Route 1:** Easy access via Amboy Avenue\n• **Parking:** On-site parking available\n• **Accessibility:** Wheelchair accessible entrance\n• **Public Transit:** Bus-friendly location\n\n🗺️ **Landmarks:** Near the heart of Edison's dining district\n\n💡 **First visit?** Call us at {self.phone} — we'll give you easy directions AND help you decide what to order!\n\n🎯 **Delivery Area:** We deliver throughout Edison and surrounding communities.\n\nReady to experience the flavors that have made us Edison's Pakistani cuisine destination? 🍽️✨"
        if any(word in query for word in ['pakistani', 'authentic', 'halal', 'culture']):
            return self._handle_cultural_inquiry(query)
        if any(word in query for word in ['google', 'maps', 'location on google', 'find you online']):
            return f"You can find us on Google Maps here: {self.google_maps}\n\nGoogle Profile:\n- Name: {self.GOOGLE_PROFILE['name']}\n- Category: {self.GOOGLE_PROFILE['category']}\n- Address: {self.GOOGLE_PROFILE['address']}\n- Phone: {self.GOOGLE_PROFILE['phone']}\n- Website: {self.GOOGLE_PROFILE['website']}\n- Hours: {self.GOOGLE_PROFILE['hours']}\n- Price Range: {self.price_range}\n- Rating: {self.rating} ⭐ ({self.review_count}+ reviews)\n- Social: Facebook: {self.social_media['facebook']}, Instagram: {self.social_media['instagram']}\n- Popular for: {', '.join(self.GOOGLE_PROFILE['popular_for'])}\n- Popular times: {self.popular_times}"
        if any(word in query for word in ['rating', 'review', 'reviews', 'google rating', 'stars']):
            return f"Our Google rating is {self.rating} stars based on {self.review_count}+ reviews.\n\nHere are some recent review highlights:\n- " + "\n- ".join(self.GOOGLE_PROFILE['review_snippets'])
        if any(word in query for word in ['price', 'cost', 'expensive', 'cheap', 'affordable']):
            return f"Our price range is {self.price_range} (moderate). We offer generous portions and great value for authentic Pakistani cuisine!"
        if any(word in query for word in ['social', 'facebook', 'instagram', 'media']):
            return f"Follow us on social media!\nFacebook: {self.social_media['facebook']}\nInstagram: {self.social_media['instagram']}"
        return f"🤔 **Great question!** Let me help you discover what makes Zaika special.\n\n**🍽️ What I can help you with:**\n• **Menu recommendations** — From bestsellers to hidden gems\n• **Dietary guidance** — Vegetarian, health-conscious, spice-level advice\n• **Cultural insights** — Stories behind our traditional dishes\n• **Party planning** — Group dining made effortless\n• **Quick service** — Fast options without sacrificing flavor\n\n**📞 For immediate assistance:** Call {self.phone} or email {self.email}\n\n**🌟 Popular conversation starters:**\n• \"What's your most Instagram-worthy dish?\"\n• \"I'm new to Pakistani food — where should I start?\"\n• \"What's good for someone who loves [spicy/mild/healthy] food?\"\n• \"Planning dinner for 6 people — help me choose!\"\n\nWhat aspect of the Zaika experience interests you most? I'm here to make your visit absolutely perfect! ✨"

    def chat_interface(self):
        """Interactive chat interface for testing"""
        welcome = f"{Fore.CYAN if COLORAMA_AVAILABLE else ''}🍢 ZAIKA BBQ GRILL - ELITE CULINARY CONCIERGE 🍢{Fore.RESET if COLORAMA_AVAILABLE else ''}"
        print(welcome)
        print(f"{Style.BRIGHT if COLORAMA_AVAILABLE else ''}✨ Your Personal Pakistani Cuisine Expert & Hospitality Professional ✨{Style.RESET_ALL if COLORAMA_AVAILABLE else ''}")
        print(f"📍 {self.location} | 📞 {self.phone}")
        print("\n💬 Ask me anything about our menu, culture, dietary needs, or dining experience!")
        print("Type 'quit' to exit\n")
        print("🌟 Try these sophisticated requests:")
        print("• 'What's trending on your Instagram this week?'")
        print("• 'I'm diabetic — what are my best options?'")
        print("• 'Surprise me with something authentically Pakistani'")
        print("• 'Planning a celebration for 8 people'")
        print("• 'I love spicy food — challenge me!'")
        print("• 'What makes Pakistani cuisine different from Indian?'")
        print("• 'Best value meal that still feels special?'\n")
        print("🚗 Type your address or zip code to get directions to Zaika BBQ & Grill!\n")
        if readline:
            readline.parse_and_bind('tab: complete')
        while True:
            try:
                user_query = input(f"{Fore.GREEN if COLORAMA_AVAILABLE else ''}Guest:{Fore.RESET if COLORAMA_AVAILABLE else ''} ")
                if user_query.lower() in ['quit', 'exit', 'bye']:
                    print(f"\n{Fore.CYAN if COLORAMA_AVAILABLE else ''}✨ Thank you for experiencing Zaika! We can't wait to serve you authentic Pakistani flavors soon! 🍽️{Fore.RESET if COLORAMA_AVAILABLE else ''}")
                    break
                response = self.generate_sophisticated_response(user_query)
                print(f"\n{Fore.YELLOW if COLORAMA_AVAILABLE else ''}Zaika Concierge: {response}{Fore.RESET if COLORAMA_AVAILABLE else ''}\n")
            except KeyboardInterrupt:
                print(f"\n\n{Fore.CYAN if COLORAMA_AVAILABLE else ''}✨ Thank you for visiting Zaika! We look forward to serving you authentic Pakistani cuisine soon! 🍽️{Fore.RESET if COLORAMA_AVAILABLE else ''}")
                break
            except Exception as e:
                logger.error(f"Technical difficulty: {e}")
                print(f"\nI apologize for the technical difficulty. Please call us directly at {self.phone} for immediate assistance, or try rephrasing your question.\n")

def main():
    """Initialize and run the Zaika AI Agent"""
    try:
        agent = ZaikaAIAgent()
        agent.chat_interface()
    except Exception as e:
        logger.error(f"Error initializing agent: {e}")
        print("Please ensure all dependencies are installed: pip install anthropic python-dotenv colorama")

if __name__ == "__main__":
    main()