# LLM-Powered Conversational Agent Using Prompt Engineering and API Integration

## Project Description
This project is a B.Tech AI/ML laboratory experiment demonstrating how to build a college admission chatbot. It highlights the use of an LLM (Large Language Model), Prompt Engineering, API Integration (OpenAI API), and maintaining a conversational context.

The chatbot answers queries about courses, eligibility, fees, admission procedures, and documents for a fictional "ABC Institute of Technology".

## Features
- **Modern Web Interface:** A clean, responsive UI built with HTML, CSS, and JS.
- **Conversational Context:** The backend passes recent conversation history to the LLM to understand contextual follow-ups.
- **Prompt Engineering:** The LLM is strictly guided via a system prompt to use a local JSON knowledge base and decline answering out-of-domain questions.
- **Graceful Error Handling:** Catches API key errors, network timeouts, and invalid inputs securely.

## Technologies Used
- Frontend: HTML5, CSS3, JavaScript (Fetch API)
- Backend: Python (Flask)
- LLM Provider: OpenAI API (via openai python package)

## How to Run

1. **Install Python**
   Ensure Python 3.8+ is installed on your system.

2. **Create a Virtual Environment (Optional but recommended)**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up the API Key**
   - Copy `.env.example` to a new file named `.env`
   - Add your OpenAI API key to the `.env` file:
     ```
     OPENAI_API_KEY=sk-your-actual-api-key-here
     ```

5. **Run the Flask Application**
   ```bash
   python app.py
   ```

6. **Access the Application**
   Open your browser and navigate to `http://localhost:5000`

## Expected Behavior
- The bot will respond politely using only the data found in `data/college_data.json`.
- If asked "Who is the Prime Minister?", it will refuse to answer.
- If asked "What is the fee for the second course?", it will understand "second course" based on previous context if you asked about courses earlier.

## Laboratory Report
The complete laboratory report for this experiment is located in the `College_Admission_LLM_Chatbot_Experiment.docx` document (generated separately).
