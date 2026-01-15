 #  AI Meeting Notes Summarizer (Streamlit)

Quick app to upload or paste a meeting transcript and generate:
- Concise bullet-point summary
- Action items with owners and due dates (when present)
- Download as Markdown

 #  Tech stack
- Streamlit
- OpenAI API (GPT-4o mini or GPT-4o)

 # Setup
1) Install Python 3.10+
2) Create a virtual environment (optional but recommended)
3) Install dependencies:
```
pip install -r requirements.txt
```
4) Set your OpenAI API key (PowerShell example):
```
$env:OPENAI_API_KEY = "sk-..."
```
5) Run the app:
```
streamlit run app.py
```

Usage tips
- You can upload a .txt file or paste raw text.
- Use the sliders to select summary length and tone.
- Click "Summarize"; then download the Markdown file.

Notes
- This starter uses OpenAI Models API; you can switch to other providers by editing `llm.py`.
- For longer transcripts, chunking is applied automatically.

