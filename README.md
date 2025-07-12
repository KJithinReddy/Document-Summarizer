# 📄 Document Summarizer

An AI-powered app that fetches any web document URL and generates concise summaries using LangChain, Groq LLaMA-3, and Streamlit.

------------------------------------------------------------

🧠 HOW IT WORKS

This app combines:
- LangChain: For document loading, text splitting, and prompt chaining  
- Groq LLaMA-3: As the backend language model for text generation  
- Streamlit: For user interface and interaction  
- Async processing: To efficiently generate map-reduce style summaries

------------------------------------------------------------

🍃 FEATURES

- Input any webpage URL  
- Automatically load and parse the webpage content  
- Split content into manageable chunks  
- Generate summary for each chunk asynchronously (map step)  
- Collapse partial summaries iteratively to create a final, concise summary (reduce step)  
- User-friendly Streamlit UI to enter URLs and display summaries

------------------------------------------------------------

🔧 INSTALLATION

1. Clone the repository:

   git clone https://github.com/KJithinReddy/Document-Summarizer.git
   
   cd document-summarizer

3. Create and activate a virtual environment:

   python -m venv venv  
   source venv/bin/activate     # On Windows: venv\Scripts\activate

4. Install dependencies:

   pip install -r requirements.txt

5. Set your environment variable in a `.env` file:

   GROQ_API_KEY=your_groq_api_key_here

------------------------------------------------------------

▶️ RUN THE APP

   streamlit run streamlit_app.py

Enter the URL of a document in the text box and click “Summarize” to get a concise summary.

------------------------------------------------------------

📂 FILE STRUCTURE

- `summarizermp.py` → Map-reduce summary logic, document loading, and chaining  
- `streamlit_app.py` → Streamlit frontend UI  
- `.env` → Environment variables (API keys)  
- `requirements.txt` → Python dependencies

------------------------------------------------------------

📦 requirements.txt

streamlit  
langchain  
langchain-groq  
langchain-core  
langchain-communities  
langchain-text-splitters  
python-dotenv  
asyncio

------------------------------------------------------------

💡 FUTURE IMPROVEMENTS

- Support PDFs and other document formats  
- Add caching for repeated URLs  
- Provide summary confidence scores  
- Enable multi-document summarization  
- Export summaries as text or PDF

------------------------------------------------------------

🧪 EXAMPLE USAGE

1. Enter a news article URL like: https://example.com/news/article123  
2. Click “Summarize”  
3. Receive a concise summary of the article’s main points

------------------------------------------------------------

Built using LangChain, Groq LLaMA, and Streamlit.
