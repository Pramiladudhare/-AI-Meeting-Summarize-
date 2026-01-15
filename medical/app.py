from typing import List, Tuple

import streamlit as st

from llm import summarize_transcript
from utils import build_markdown, build_pdf, chunk_text


st.set_page_config(
    page_title="AI Meeting Notes Summarizer", 
    page_icon="📝", 
    layout="wide",
    initial_sidebar_state="expanded"
)


def get_transcript_text() -> str:
	# Create tabs for better UX
	tab1, tab2 = st.tabs(["📁 Upload File", "✏️ Paste Text"])
	
	text_from_upload = ""
	with tab1:
		st.markdown("### Upload Your Meeting Transcript")
		uploaded = st.file_uploader(
			"Choose a .txt file", 
			type=["txt"], 
			accept_multiple_files=False,
			help="Upload a text file containing your meeting transcript"
		)
		if uploaded is not None:
			try:
				text_from_upload = uploaded.read().decode("utf-8", errors="ignore")
				st.success(f"✅ File uploaded successfully! ({len(text_from_upload)} characters)")
			except Exception:
				st.error("❌ Could not read file. Please ensure it's a plain .txt file.")
	
	with tab2:
		st.markdown("### Paste Your Meeting Transcript")
		pasted = st.text_area(
			"Paste your meeting transcript here", 
			height=300, 
			placeholder="Example:\nAlice: Thanks for joining. Goal is to decide the landing page hero.\nBob: Current bounce rate is 62%. We need a clearer value prop.\nCarol: I propose 'Track expenses effortlessly. See savings in real time.'",
			help="Copy and paste your meeting transcript directly into this text area"
		)
	
	return pasted.strip() if pasted and len(pasted.strip()) > 0 else text_from_upload.strip()


def sidebar_controls() -> Tuple[int, str]:
	st.sidebar.markdown("## ⚙️ Customization Options")
	
	st.sidebar.markdown("### 📊 Summary Settings")
	length = st.sidebar.slider(
		"Summary length (bullets)", 
		min_value=5, 
		max_value=20, 
		value=10,
		help="Number of bullet points in the summary"
	)
	
	tone = st.sidebar.selectbox(
		"Tone", 
		["neutral", "executive", "friendly", "detailed"], 
		index=0,
		help="Choose the tone for your summary"
	)
	
	st.sidebar.markdown("---")
	st.sidebar.markdown("### 💡 Tips")
	st.sidebar.info("""
	- **Executive**: Professional, concise
	- **Friendly**: Casual, team-focused  
	- **Detailed**: Comprehensive, thorough
	- **Neutral**: Balanced, objective
	""")
	
	return length, tone


def main() -> None:
	# Header with better styling
	st.markdown("""
	<div style="text-align: center; padding: 2rem 0; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); border-radius: 10px; margin-bottom: 2rem;">
		<h1 style="color: white; margin: 0; font-size: 2.5rem;">📝 AI Meeting Notes Summarizer</h1>
		<p style="color: #f0f0f0; margin: 0.5rem 0 0 0; font-size: 1.2rem;">Transform your meeting transcripts into actionable insights</p>
	</div>
	""", unsafe_allow_html=True)

	# Feature highlights
	col1, col2, col3, col4 = st.columns(4)
	with col1:
		st.markdown("""
		<div style="text-align: center; padding: 1rem; background: #f8f9fa; border-radius: 8px; border-left: 4px solid #28a745;">
			<h4 style="margin: 0; color: #28a745;">⚡ Fast Processing</h4>
			<p style="margin: 0.5rem 0 0 0; color: #666;">Quick summarization</p>
		</div>
		""", unsafe_allow_html=True)
	
	with col2:
		st.markdown("""
		<div style="text-align: center; padding: 1rem; background: #f8f9fa; border-radius: 8px; border-left: 4px solid #007bff;">
			<h4 style="margin: 0; color: #007bff;">🔒 Privacy First</h4>
			<p style="margin: 0.5rem 0 0 0; color: #666;">No data sent to external APIs</p>
		</div>
		""", unsafe_allow_html=True)
	
	with col3:
		st.markdown("""
		<div style="text-align: center; padding: 1rem; background: #f8f9fa; border-radius: 8px; border-left: 4px solid #ffc107;">
			<h4 style="margin: 0; color: #ffc107;">📊 Smart Analysis</h4>
			<p style="margin: 0.5rem 0 0 0; color: #666;">Extracts key points & actions</p>
		</div>
		""", unsafe_allow_html=True)
	
	with col4:
		st.markdown("""
		<div style="text-align: center; padding: 1rem; background: #f8f9fa; border-radius: 8px; border-left: 4px solid #dc3545;">
			<h4 style="margin: 0; color: #dc3545;">📥 Easy Export</h4>
			<p style="margin: 0.5rem 0 0 0; color: #666;">Download as Markdown</p>
		</div>
		""", unsafe_allow_html=True)

	st.markdown("---")

	length, tone = sidebar_controls()

	# Main content area
	st.markdown("## 📋 Input Your Meeting Transcript")
	
	# Handle sample loading
	if 'sample_loaded' in st.session_state:
		st.info("📋 Sample transcript loaded! Switch to the 'Paste Text' tab to see it.")
	
	transcript = get_transcript_text()
	
	# If sample was loaded, use it
	if 'sample_loaded' in st.session_state and not transcript:
		transcript = st.session_state['sample_loaded']

	# Action buttons with better styling
	st.markdown("---")
	col1, col2, col3 = st.columns([1, 1, 1])
	
	with col1:
		if st.button("🚀 Generate Summary", key="summarize_button", use_container_width=True, type="primary"):
			if not transcript:
				st.error("⚠️ Please upload a file or paste transcript text first.")
			else:
				with st.spinner("🔄 Analyzing transcript and generating summary..."):
					chunks = chunk_text(transcript)
					summary_bullets: List[str] = []
					action_items: List[str] = []
					
					# Progress bar
					progress_bar = st.progress(0)
					total_chunks = len(chunks)
					
					for idx, ch in enumerate(chunks):
						partial_summary, partial_actions = summarize_transcript(ch, length=length, tone=tone)
						summary_bullets.extend(partial_summary)
						action_items.extend(partial_actions)
						progress_bar.progress((idx + 1) / total_chunks)

					# De-duplicate and trim
					summary_bullets = list(dict.fromkeys([s.strip(" -\n") for s in summary_bullets if s.strip()]))
					action_items = list(dict.fromkeys([a.strip(" -\n") for a in action_items if a.strip()]))

					md = build_markdown(summary_bullets, action_items)
					
					# Store in session state
					st.session_state['summary_md'] = md
					st.session_state['summary_bullets'] = summary_bullets
					st.session_state['action_items'] = action_items
					
					st.success("✅ Summary generated successfully!")
	
	with col2:
		if st.button("🗑️ Clear All", key="clear_button", use_container_width=True):
			st.rerun()
	
	with col3:
		if st.button("📋 Load Sample", key="sample_button", use_container_width=True):
			sample_text = """Alice: Thanks for joining. Goal is to decide the landing page hero.
Bob: Current bounce rate is 62%. We need a clearer value prop.
Carol: I propose "Track expenses effortlessly. See savings in real time."
Bob: A/B test that vs "Control your money with smart insights."
Alice: OK. Bob owns the A/B test. Deadline Friday.
Carol: I'll deliver two hero images by Wednesday."""
			st.session_state['sample_loaded'] = sample_text
			st.rerun()

	# Display results
	if 'summary_md' in st.session_state:
		st.markdown("---")
		st.markdown("## 📊 Generated Summary")
		
		# Summary stats
		col1, col2, col3 = st.columns(3)
		with col1:
			st.metric("Key Points", len(st.session_state['summary_bullets']))
		with col2:
			st.metric("Action Items", len(st.session_state['action_items']))
		with col3:
			st.metric("Total Characters", len(st.session_state['summary_md']))
		
		# Display summary
		st.markdown(st.session_state['summary_md'])
		
		# Download buttons
		col_md, col_pdf = st.columns(2)
		with col_md:
			st.download_button(
				label="📥 Download as Markdown",
				data=st.session_state['summary_md'],
				file_name=f"meeting_summary_{tone}_{length}bullets.md",
				mime="text/markdown",
				use_container_width=True
			)
		with col_pdf:
			pdf_bytes = build_pdf(
				st.session_state['summary_bullets'],
				st.session_state['action_items']
			)
			st.download_button(
				label="📄 Download as PDF",
				data=pdf_bytes,
				file_name=f"meeting_summary_{tone}_{length}bullets.pdf",
				mime="application/pdf",
				use_container_width=True
			)


if __name__ == "__main__":
	main()


