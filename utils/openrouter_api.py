
import os
import json
import logging
import requests
import urllib.parse
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

# Get API key from environment variables with fallback
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "mistralai/mistral-7b-instruct:free"  # Darmowy model Mistral

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "HTTP-Referer": "https://cv-optimizer-pro.repl.co/"  # Replace with your actual domain
}

def send_api_request(prompt, max_tokens=2000):
    """
    Send a request to the OpenRouter API
    """
    if not OPENROUTER_API_KEY:
        logger.error("OpenRouter API key not found")
        raise ValueError("OpenRouter API key not set in environment variables")
    
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are an expert resume editor and career advisor. Always respond in the same language as the CV or job description provided by the user."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens
    }
    
    try:
        logger.debug(f"Sending request to OpenRouter API")
        response = requests.post(OPENROUTER_BASE_URL, headers=headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        logger.debug(f"Received response from OpenRouter API")
        
        if 'choices' in result and len(result['choices']) > 0:
            return result['choices'][0]['message']['content']
        else:
            raise ValueError("Unexpected API response format")
    
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {str(e)}")
        raise Exception(f"Failed to communicate with OpenRouter API: {str(e)}")
    
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        logger.error(f"Error parsing API response: {str(e)}")
        raise Exception(f"Failed to parse OpenRouter API response: {str(e)}")

def optimize_cv(cv_text, job_description):
    """
    Create an optimized version of CV using advanced AI processing
    """
    prompt = f"""
    TASK: Stwórz całkowicie nową, spersonalizowaną wersję CV precyzyjnie dopasowaną do wymagań stanowiska.
    
    Kluczowe wytyczne optymalizacji:
    1. Głęboka analiza i transformacja doświadczenia:
       - Przeprowadź szczegółową analizę każdego stanowiska pod kątem wymagań nowej roli
       - Zidentyfikuj i wyeksponuj transferowalne umiejętności
       - Dodaj wymierzalne rezultaty i osiągnięcia (%, liczby, skala projektów)
       - Użyj profesjonalnego, branżowego słownictwa charakterystycznego dla danego sektora
       - Stwórz nowe opisy stanowisk wykorzystując słowa kluczowe z ogłoszenia
    
    2. Zaawansowana personalizacja:
       - Dopasuj tone of voice do kultury firmy i branży
       - Uwzględnij specyficzne technologie i metodologie wymienione w ogłoszeniu
       - Dodaj sekcję highlight'ów dopasowaną do priorytetowych wymagań
       - Stwórz spersonalizowane podsumowanie zawodowe podkreślające najważniejsze atuty
    
    3. Optymalizacja umiejętności i kompetencji:
       - Podziel umiejętności na kategorie: techniczne, miękkie, branżowe
       - Określ poziom zaawansowania w skali 1-5 dla kluczowych kompetencji
       - Dodaj konkretne przykłady zastosowania każdej kluczowej umiejętności
       - Uwzględnij certyfikaty i szkolenia istotne dla stanowiska
    
    4. Dostosowanie struktury i formatowania:
       - Zastosuj przejrzystą, profesjonalną hierarchię informacji
       - Użyj bullet pointów dla lepszej czytelności
       - Zachowaj spójny format dat i opisów
       - Zoptymalizuj pod kątem ATS używając standardowych nagłówków
    
    5. Elementy dodatkowe:
       - Dodaj sekcję projektów specjalnych jeśli są istotne
       - Uwzględnij osiągnięcia i wyróżnienia branżowe
       - Dodaj linki do portfolio/projektów jeśli są dostępne
       - Uwzględnij wolontariat lub działalność dodatkową wspierającą profil zawodowy
    
    WAŻNE ZASADY:
    - Zachowaj pełną spójność z prawdą zawartą w oryginalnym CV
    - Każda sekcja musi być napisana od nowa z fokusem na nowe stanowisko
    - Używaj aktywnych czasowników i konkretnych przykładów
    - Odpowiedz w tym samym języku co oryginalne CV
    
    DANE:
    
    Opis stanowiska:
    {job_description}
    
    Oryginalne CV:
    {cv_text}
    
    Zwróć tylko zoptymalizowane CV w formacie tekstowym, bez dodatkowych komentarzy.
    """
    
    return send_api_request(prompt, max_tokens=2500)

def generate_recruiter_feedback(cv_text, job_description=""):
    """
    Generate feedback on a CV as if from an AI recruiter
    """
    context = ""
    if job_description:
        context = f"Job description for context:\n{job_description}"
        
    prompt = f"""
    TASK: You are an experienced professional recruiter. Review this CV and provide detailed, actionable feedback.
    
    Include:
    1. Overall impression
    2. Strengths and weaknesses
    3. Formatting and structure assessment
    4. Content quality evaluation
    5. ATS compatibility
    6. Specific improvement suggestions
    7. Rating out of 10
    
    IMPORTANT: Respond in the same language as the CV. If the CV is in Polish, respond in Polish. If the CV is in English, respond in English.
    
    {context}
    
    CV:
    {cv_text}
    
    Provide detailed recruiter feedback. Be honest but constructive.
    """
    
    return send_api_request(prompt, max_tokens=2000)

def generate_cover_letter(cv_text, job_description):
    """
    Generate a cover letter based on a CV and job description
    """
    prompt = f"""
    TASK: Create a personalized cover letter based on this CV and job description.
    
    The cover letter should:
    - Be professionally formatted
    - Highlight relevant skills and experiences from the CV
    - Connect the candidate's background to the job requirements
    - Include a compelling introduction and conclusion
    - Be approximately 300-400 words
    
    IMPORTANT: Respond in the same language as the CV. If the CV is in Polish, respond in Polish. If the CV is in English, respond in English.
    
    Job description:
    {job_description}
    
    CV:
    {cv_text}
    
    Return only the cover letter in plain text format.
    """
    
    return send_api_request(prompt, max_tokens=2000)

def translate_to_english(cv_text):
    """
    Translate a CV to English while preserving professional terminology
    """
    prompt = f"""
    TASK: Translate this CV to professional English.
    
    Important:
    - Maintain all professional terminology
    - Preserve the original structure and formatting
    - Ensure proper translation of industry-specific terms
    - Keep names of companies and products unchanged
    - Make sure the translation sounds natural and professional in English
    
    Original CV:
    {cv_text}
    
    Return only the translated CV in plain text format.
    """
    
    return send_api_request(prompt, max_tokens=2500)

def suggest_alternative_careers(cv_text):
    """
    Suggest alternative career paths based on the skills in a CV
    """
    prompt = f"""
    TASK: Analyze this CV and suggest alternative career paths based on the skills and experience.
    
    For each suggested career path include:
    1. Job title/role
    2. Why it's a good fit based on existing skills
    3. What additional skills might be needed
    4. Potential industries or companies to target
    5. Estimated effort to transition (low/medium/high)
    
    IMPORTANT: Respond in the same language as the CV. If the CV is in Polish, respond in Polish. If the CV is in English, respond in English.
    
    CV:
    {cv_text}
    
    Provide a detailed analysis with specific, actionable recommendations.
    """
    
    return send_api_request(prompt, max_tokens=2000)

def generate_multi_versions(cv_text, roles):
    """
    Generate multiple versions of a CV tailored to different roles
    """
    roles_text = "\n".join([f"- {role}" for role in roles])
    
    prompt = f"""
    TASK: Create tailored versions of this CV for different roles.
    
    Roles to create CV versions for:
    {roles_text}
    
    For each role:
    1. Highlight relevant skills and experiences
    2. Customize the professional summary
    3. Adjust the emphasis of achievements
    4. Remove or downplay irrelevant information
    
    IMPORTANT: Respond in the same language as the CV. If the CV is in Polish, respond in Polish. If the CV is in English, respond in English.
    
    Original CV:
    {cv_text}
    
    Return each version clearly separated with a heading indicating the role.
    """
    
    return send_api_request(prompt, max_tokens=3000)

def analyze_job_url(url):
    """
    Extract job description from a URL with improved handling for popular job sites
    """
    try:
        logger.debug(f"Analyzing job URL: {url}")
        
        # Validate URL
        parsed_url = urllib.parse.urlparse(url)
        if not parsed_url.scheme or not parsed_url.netloc:
            raise ValueError("Invalid URL format")
        
        # Fetch the page
        response = requests.get(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        })
        response.raise_for_status()
        
        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Try to find the job description
        job_text = ""
        domain = parsed_url.netloc.lower()
        
        # Enhanced site-specific extraction for popular job boards
        if 'linkedin.com' in domain:
            containers = soup.select('.description__text, .show-more-less-html, .jobs-description__content')
            if containers:
                job_text = containers[0].get_text(separator='\n', strip=True)
                
        elif 'indeed.com' in domain:
            container = soup.select_one('#jobDescriptionText')
            if container:
                job_text = container.get_text(separator='\n', strip=True)
                
        elif 'pracuj.pl' in domain:
            containers = soup.select('[data-test="section-benefit-expectations-text"], [data-test="section-description-text"]')
            if containers:
                job_text = '\n'.join([c.get_text(separator='\n', strip=True) for c in containers])
                
        elif 'olx.pl' in domain or 'praca.pl' in domain:
            containers = soup.select('.offer-description, .offer-content, .description')
            if containers:
                job_text = containers[0].get_text(separator='\n', strip=True)
        
        # If no specific site pattern matched, use generic approach
        if not job_text:
            # Look for common containers for job descriptions
            potential_containers = soup.select('.job-description, .description, .details, article, .job-content, [class*=job], [class*=description], [class*=offer]')
            if potential_containers:
                # Get the longest container text as it's likely the main description
                for container in potential_containers:
                    container_text = container.get_text(separator='\n', strip=True)
                    if len(container_text) > len(job_text):
                        job_text = container_text
            
            # If still no container found, get the body text
            if not job_text and soup.body:
                # Remove navigation, header, footer and scripts
                for tag in soup.select('nav, header, footer, script, style, iframe'):
                    tag.decompose()
                
                job_text = soup.body.get_text(separator='\n', strip=True)
                
                # If body text is very long, try to extract the most relevant part
                if len(job_text) > 10000:
                    paragraphs = job_text.split('\n')
                    # Look for paragraphs with keywords likely to be in job descriptions
                    keywords = ['requirements', 'responsibilities', 'qualifications', 'skills', 'experience', 'about the job', 
                                'wymagania', 'obowiązki', 'kwalifikacje', 'umiejętności', 'doświadczenie', 'o pracy']
                    
                    relevant_paragraphs = []
                    found_relevant = False
                    
                    for paragraph in paragraphs:
                        if any(keyword.lower() in paragraph.lower() for keyword in keywords):
                            found_relevant = True
                        if found_relevant and len(paragraph.strip()) > 50:  # Only include substantive paragraphs
                            relevant_paragraphs.append(paragraph)
                    
                    if relevant_paragraphs:
                        job_text = '\n'.join(relevant_paragraphs)
        
        # Clean up the text - remove excessive whitespace but preserve paragraph breaks
        job_text = '\n'.join([' '.join(line.split()) for line in job_text.split('\n') if line.strip()])
        
        if not job_text:
            raise ValueError("Could not extract job description from the URL")
        
        logger.debug(f"Successfully extracted job description from URL")
        
        # If the text is too long, summarize it using the AI
        if len(job_text) > 4000:
            logger.debug(f"Job description is long ({len(job_text)} chars), summarizing with AI")
            job_text = summarize_job_description(job_text)
        
        return job_text
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching job URL: {str(e)}")
        raise Exception(f"Failed to fetch job posting from URL: {str(e)}")
    
    except Exception as e:
        logger.error(f"Error analyzing job URL: {str(e)}")
        raise Exception(f"Failed to analyze job posting: {str(e)}")

def summarize_job_description(job_text):
    """
    Summarize a long job description using the AI
    """
    prompt = f"""
    TASK: Extract and summarize the key information from this job posting.
    
    Include:
    1. Job title and company (if mentioned)
    2. Required skills and qualifications
    3. Responsibilities and duties
    4. Preferred experience
    5. Any other important details (benefits, location, etc.)
    6. TOP 5 keywords that are critically important for this position
    
    IMPORTANT: Detect the language of the job posting and respond in that same language.
    If the job posting is in Polish, respond in Polish.
    If the job posting is in English, respond in English.
    
    Job posting text:
    {job_text[:4000]}...
    
    Provide a concise but comprehensive summary of this job posting, focusing on information relevant for CV optimization.
    Format the TOP 5 keywords as a separate section at the end labeled "KLUCZOWE SŁOWA:" (in Polish) or "KEY KEYWORDS:" (in English).
    """
    
    return send_api_request(prompt, max_tokens=1500)

def analyze_market_trends(job_title, industry=""):
    """
    Analyze market trends and suggest popular skills/keywords for a specific job or industry
    """
    prompt = f"""
    TASK: Przeprowadź analizę trendów rynkowych dla pozycji: {job_title} w branży: {industry if industry else "wszystkich branżach"}.
    
    Przygotuj następujące informacje:
    1. TOP 10 najbardziej poszukiwanych umiejętności technicznych dla tej pozycji w 2025 roku
    2. TOP 5 umiejętności miękkich cenionych przez pracodawców
    3. Technologie/narzędzia wschodząće, które warto wymienić w CV
    4. 3 najważniejsze certyfikaty lub szkolenia zwiększające wartość kandydata
    5. Trendy płacowe - przedziały wynagrodzeń 
    
    Format odpowiedzi powinien być zwięzły, przejrzysty i łatwy do odczytania przez osobę szukającą pracy.
    Jeśli nazwa stanowiska jest w języku angielskim, odpowiedz po angielsku. Jeśli w języku polskim - odpowiedz po polsku.
    """
    
    return send_api_request(prompt, max_tokens=1500)

def ats_optimization_check(cv_text, job_description=""):
    """
    Check CV against ATS (Applicant Tracking System) and provide suggestions for improvement
    """
    context = ""
    if job_description:
        context = f"Ogłoszenie o pracę dla odniesienia:\n{job_description[:2000]}"
        
    prompt = f"""
    TASK: Sprawdź to CV pod kątem kompatybilności z systemami ATS (Applicant Tracking System) i oceń jego skuteczność.
    
    Przeprowadź następujące analizy:
    1. Wykryj potencjalne problemy z formatowaniem, które mogą utrudnić odczyt przez systemy ATS
    2. Sprawdź gęstość słów kluczowych i trafność ich wykorzystania
    3. Oceń strukturę CV i zaproponuj ulepszenia dla lepszej czytelności maszynowej
    4. Zidentyfikuj brakujące sekcje lub informacje, które są często wymagane przez ATS
    5. Oceń ogólną skuteczność CV w systemach ATS w skali 1-10
    
    {context}
    
    CV do analizy:
    {cv_text}
    
    Odpowiedz w tym samym języku co CV. Jeśli CV jest po polsku, odpowiedz po polsku.
    Format odpowiedzi powinien być przejrzysty, z wyraźnie oznaczonymi sekcjami i konkretnymi sugestiami usprawnień.
    """
    
    return send_api_request(prompt, max_tokens=1800)

def generate_interview_questions(cv_text, job_description=""):
    """
    Generate likely interview questions based on CV and job description
    """
    context = ""
    if job_description:
        context = f"Uwzględnij poniższe ogłoszenie o pracę przy tworzeniu pytań:\n{job_description[:2000]}"
        
    prompt = f"""
    TASK: Wygeneruj zestaw potencjalnych pytań rekrutacyjnych, które kandydat może otrzymać podczas rozmowy kwalifikacyjnej.
    
    Pytania powinny być:
    1. Specyficzne dla doświadczenia i umiejętności kandydata wymienionych w CV
    2. Dopasowane do stanowiska (jeśli podano opis stanowiska)
    3. Zróżnicowane - połączenie pytań technicznych, behawioralnych i sytuacyjnych
    4. Realistyczne i często zadawane przez rekruterów
    
    Uwzględnij po co najmniej 3 pytania z każdej kategorii:
    - Pytania o doświadczenie zawodowe
    - Pytania techniczne/o umiejętności
    - Pytania behawioralne
    - Pytania sytuacyjne
    - Pytania o motywację i dopasowanie do firmy/stanowiska
    
    {context}
    
    CV:
    {cv_text}
    
    Odpowiedz w tym samym języku co CV. Jeśli CV jest po polsku, odpowiedz po polsku.
    Dodatkowo, do każdego pytania dodaj krótką wskazówkę, jak można by na nie odpowiedzieć w oparciu o informacje z CV.
    """
    
    return send_api_request(prompt, max_tokens=2000)
