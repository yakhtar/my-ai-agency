# Zaika BBQ Grill AI Assistant
import anthropic

# Initialize Claude with your API key
client = anthropic.Anthropic(api_key="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")

def answer_restaurant_question(question):
    """
    This function answers restaurant questions using Claude AI
    """
    
    restaurant_info = """
    You are a helpful assistant for Zaika BBQ Grill, a family-owned Pakistani restaurant in Edison, New Jersey.
    
    HOURS: Daily 11:00 AM - 10:00 PM
    PHONE: (732) 709-3700
    ADDRESS: 1199 Amboy Ave, Edison, NJ 08837
    
    SPECIALTIES:
    - BBQ Mix Grill (most popular dish!)
    - Goat Paya (traditional Pakistani specialty)
    - Beef Seekh Kabab
    - Daal Makhni (lentil curry)
    - Chicken Biryani
    - Brain Masala (authentic specialty)
    - All meat is halal
    
    SERVICES:
    - Dine-in, takeout, delivery available
    - Reservations accepted for large groups
    - Wheelchair accessible
    - Vegetarian and vegan options
    - Prayer space available
    - Family-owned with authentic Pakistani hospitality
    """
    
    prompt = f"""
    {restaurant_info}
    
    Customer Question: {question}
    
    Answer as a friendly restaurant staff member. Keep it helpful and concise.
    """
    
    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=150,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    except Exception as e:
        return f"Sorry, I'm having trouble right now. Please call us at (732) 709-3700!"

# Test the bot
if __name__ == "__main__":
    print("🍢 Zaika BBQ Grill - AI Assistant")
    print("Ask me anything about our authentic Pakistani cuisine!")
    print("Type 'quit' to exit\n")
    
    while True:
        question = input("Customer: ")
        if question.lower() == 'quit':
            break
        
        answer = answer_restaurant_question(question)
        print(f"Zaika Assistant: {answer}\n")