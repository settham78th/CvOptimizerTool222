import os
import logging
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from cv_generator import generate_cv_content

# Set up logging for easier debugging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev_secret_key")

# Routes
@app.route('/', methods=['GET'])
def index():
    """Render the main CV generation form."""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    """Generate CV content based on form input."""
    try:
        # Get form data
        name = request.form.get('name', '')
        email = request.form.get('email', '')
        phone = request.form.get('phone', '')
        education = request.form.get('education', '')
        experience = request.form.get('experience', '')
        skills = request.form.get('skills', '')
        
        # Generate CV content with fact-checking prompts
        cv_content = generate_cv_content(
            name=name,
            email=email,
            phone=phone,
            education=education,
            experience=experience,
            skills=skills
        )
        
        # Store in session for rendering
        session['cv_content'] = cv_content
        
        return redirect(url_for('view_cv'))
    except Exception as e:
        logging.error(f"Error generating CV: {str(e)}")
        flash("An error occurred while generating your CV. Please try again.")
        return redirect(url_for('index'))

@app.route('/view_cv', methods=['GET'])
def view_cv():
    """View the generated CV."""
    cv_content = session.get('cv_content', None)
    if not cv_content:
        flash("No CV has been generated yet.")
        return redirect(url_for('index'))
    
    return render_template('cv.html', cv_content=cv_content)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
