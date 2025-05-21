import os
import logging
from openai import OpenAI

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize OpenAI client
OPENAI_API_KEY = os.environ.get("OPENROUTER_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def generate_cv_content(name, email, phone, education, experience, skills):
    """
    Generate CV content based on user input with emphasis on factual information.
    
    Args:
        name (str): User's name
        email (str): User's email
        phone (str): User's phone number
        education (str): User's educational background
        experience (str): User's work experience
        skills (str): User's skills
        
    Returns:
        dict: Formatted CV sections
    """
    try:
        # Prepare user input data
        user_data = {
            "name": name,
            "email": email,
            "phone": phone,
            "education": education,
            "experience": experience,
            "skills": skills
        }
        
        # Create a prompt that emphasizes factual information only with even stricter guidelines
        prompt = f"""
        You are a professional CV creator that follows extremely strict ethical guidelines against fabrication.

        CRITICAL RULES - FOLLOW THESE EXACTLY:
        1. NEVER invent or fabricate ANY information not provided by the user
        2. If information is incomplete, keep that section short and basic - DO NOT add details
        3. DO NOT embellish qualifications, skills, or experiences
        4. DO NOT generate fictional employment details, dates, or achievements
        5. ONLY organize the provided text - never add content
        6. ONLY use the exact information provided by the user, even if it seems too brief
        7. DO NOT add skills that weren't mentioned
        8. DO NOT create a narrative about career progression unless explicitly stated
        9. DO NOT infer job titles, responsibilities, or achievements
        10. If sections are vague, keep them vague rather than making specific claims

        User provided the following information to include in their CV:
        
        Name: {user_data['name']}
        Email: {user_data['email']}
        Phone: {user_data['phone']}
        Education: {user_data['education']}
        Experience: {user_data['experience']}
        Skills: {user_data['skills']}

        Format this information into professional CV sections, strictly using ONLY the exact text provided above.
        
        Return your response as a JSON object with the following structure:
        {{
            "profile_summary": "A very brief professional summary using ONLY actual information provided, without ANY assumptions or fabrications",
            "education": "Formatted education section using ONLY the exact education text provided",
            "experience": "Formatted work experience section using ONLY the exact experience text provided",
            "skills": "Formatted skills section using ONLY the exact skills text provided",
            "contact": "Formatted contact information"
        }}
        """
        
        # Call OpenAI API with enhanced instructions against fabrication
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a professional CV creator with ZERO TOLERANCE for fabrication. You MUST NEVER add information that wasn't explicitly provided by the user, even if the CV seems incomplete. Your role is to format ONLY the exact information given."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.1  # Even lower temperature to further reduce any creativity/fabrication
        )
        
        # Extract and return generated content
        cv_content = response.choices[0].message.content
        logger.debug(f"Generated CV content: {cv_content}")
        
        # Parse JSON response
        import json
        cv_json = json.loads(cv_content)
        
        return cv_json
        
    except Exception as e:
        logger.error(f"Error in CV generation: {str(e)}")
        # Return a simple error structure
        return {
            "profile_summary": "Error generating profile.",
            "education": "Error processing education information.",
            "experience": "Error processing experience information.",
            "skills": "Error processing skills information.",
            "contact": f"Name: {name}, Email: {email}, Phone: {phone}"
        }
