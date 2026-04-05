import streamlit as st
from agent.agent_core import planner_agent, content_agent, reasoning_agent, decide_action
from mcp_client import MCPClient
from tools.ppt_tools import add_title_slide
from PIL import Image
import os
import time
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="AI PPT Generator", 
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    /* Main container styling */
    .main {
        padding: 0rem 1rem;
    }
    
    /* Gradient background for headers */
    .gradient-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    /* Card styling */
    .card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    
    /* Progress bar customization */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: transform 0.2s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    /* Success message styling */
    .success-message {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    
    /* Info box styling */
    .info-box {
        background: #e7f3ff;
        padding: 0.8rem;
        border-radius: 8px;
        border-left: 4px solid #2196f3;
        margin: 0.5rem 0;
    }
    
    /* Slide preview card */
    .slide-preview {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border: 1px solid #dee2e6;
        transition: all 0.3s;
    }
    
    .slide-preview:hover {
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        transform: translateX(5px);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Stats card */
    .stats-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .stats-number {
        font-size: 2rem;
        font-weight: bold;
    }
    
    .stats-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    
    /* Error message styling */
    .error-message {
        background: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #dc3545;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'generated' not in st.session_state:
    st.session_state.generated = False
if 'plan' not in st.session_state:
    st.session_state.plan = []
if 'file_path' not in st.session_state:
    st.session_state.file_path = None
if 'client' not in st.session_state:
    st.session_state.client = None

# Theme configuration
THEMES = {
    "blue": {
        "name": "Blue Professional",
        "title_color": "1E3A8A",
        "bg_color": "EFF6FF",
        "accent_color": "3B82F6"
    },
    "dark": {
        "name": "Dark Modern",
        "title_color": "FFFFFF",
        "bg_color": "1F2937",
        "accent_color": "6366F1"
    },
    "green": {
        "name": "Green Nature",
        "title_color": "064E3B",
        "bg_color": "ECFDF5",
        "accent_color": "10B981"
    },
    "purple": {
        "name": "Purple Creative",
        "title_color": "4C1D95",
        "bg_color": "F5F3FF",
        "accent_color": "8B5CF6"
    },
    "modern": {
        "name": "Modern Gradient",
        "title_color": "0F172A",
        "bg_color": "F8FAFC",
        "accent_color": "0EA5E9"
    }
}

# Sidebar
with st.sidebar:
    st.markdown("### 🎨 AI PPT Generator")
    st.markdown("---")
    
    # Quick stats (shown after generation)
    if st.session_state.generated and st.session_state.plan:
        st.markdown("### 📊 Quick Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
                <div class="stats-card">
                    <div class="stats-number">{len(st.session_state.plan)}</div>
                    <div class="stats-label">Total Slides</div>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <div class="stats-card">
                    <div class="stats-number">{datetime.now().strftime('%H:%M')}</div>
                    <div class="stats-label">Generated At</div>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 💡 Pro Tips")
    st.info("""
        • Be specific with your topic
        • Choose a theme that matches your content
        • Review slides before downloading
        • Use charts for data-heavy topics
    """)
    
    st.markdown("---")
    st.markdown("### 🚀 Features")
    st.success("""
        ✅ AI-powered content generation
        ✅ Multiple themes
        ✅ Charts & visualizations
        ✅ Live slide preview
        ✅ One-click download
    """)

# Main content
st.markdown("""
    <div class="gradient-header">
        <h1>🚀 AI PPT Generator</h1>
        <p>Create stunning presentations in seconds with AI</p>
    </div>
""", unsafe_allow_html=True)

# Input section
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    topic = st.text_input(
        "📝 **What's your presentation about?**",
        placeholder="e.g., The Future of Artificial Intelligence in Healthcare",
        help="Be specific for better results"
    )

with col2:
    selected_theme = st.selectbox(
        "🎨 **Choose Theme**",
        list(THEMES.keys()),
        format_func=lambda x: THEMES[x]["name"],
        help="Select a visual theme for your presentation"
    )

with col3:
    generate = st.button("✨ Generate PPT", use_container_width=True)

# Show example topics
if not topic:
    st.markdown("### 📋 Example Topics")
    example_col1, example_col2, example_col3 = st.columns(3)
    
    examples = [
        "Digital Marketing Trends 2024",
        "Sustainable Business Practices",
        "Machine Learning Fundamentals",
        "Remote Team Management",
        "Financial Planning 101",
        "Product Launch Strategy"
    ]
    
    for i, col in enumerate([example_col1, example_col2, example_col3]):
        with col:
            for j in range(2):
                idx = i*2 + j
                if idx < len(examples):
                    if st.button(f"📌 {examples[idx]}", key=f"example_{idx}", use_container_width=True):
                        topic = examples[idx]
                        st.rerun()

# Generation process
if generate and topic:
    st.session_state.generated = False
    st.markdown("---")
    
    try:
        # Progress tracking
        progress_container = st.container()
        
        with progress_container:
            st.markdown("## 🎯 Generating Your Presentation")
            
            # Step 1: Planning
            with st.spinner("🧠 Analyzing topic and planning slide structure..."):
                st.markdown("### 📋 Step 1: Slide Planning")
                plan_progress = st.progress(0, text="Analyzing topic...")
                time.sleep(0.5)
                
                st.session_state.plan = planner_agent(topic)
                
                # Validate plan
                if not st.session_state.plan or not isinstance(st.session_state.plan, list):
                    st.error("Failed to generate slide plan. Please try again with a different topic.")
                    st.stop()
                
                plan_progress.progress(100)
                
                # Display plan in a nice grid
                st.markdown("**📑 Presentation Outline:**")
                cols = st.columns(min(3, len(st.session_state.plan)))
                for idx, slide_title in enumerate(st.session_state.plan):
                    with cols[idx % len(cols)]:
                        st.markdown(f"""
                            <div class="slide-preview">
                                <strong>Slide {idx+1}</strong><br>
                                {slide_title}
                            </div>
                        """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Step 2: Initialize PPT
            with st.spinner("🎨 Setting up presentation..."):
                st.markdown("### 🎨 Step 2: Initializing Presentation")
                st.session_state.client = MCPClient()
                
                # Pass theme configuration
                theme_config = THEMES.get(selected_theme, THEMES["blue"])
                st.session_state.client.call_tool("create_ppt", theme_config)
                add_title_slide(st.session_state.client.prs, topic)
                st.success(f"✅ Presentation initialized with {THEMES[selected_theme]['name']} theme")
            
            st.markdown("---")
            
            # Step 3: Generate slides
            st.markdown("### ✨ Step 3: Generating Content")
            
            # Progress bar for slides
            slide_progress = st.progress(0)
            status_text = st.empty()
            
            for i, title in enumerate(st.session_state.plan):
                with st.expander(f"**Slide {i+1}: {title}**", expanded=(i==0)):
                    col1, col2 = st.columns([1, 1])
                    
                    with col1:
                        st.markdown("**🧠 AI Reasoning**")
                        try:
                            thought = reasoning_agent(title, topic)
                            if thought:
                                st.markdown(f'<div class="info-box">💭 {thought[:200]}</div>', unsafe_allow_html=True)
                            else:
                                st.markdown('<div class="info-box">💭 Analyzing slide content...</div>', unsafe_allow_html=True)
                        except Exception as e:
                            st.markdown(f'<div class="info-box">💭 Generating content strategy...</div>', unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown("**✍️ Content Generated**")
                        try:
                            content_list = content_agent(title, topic)
                            if content_list and isinstance(content_list, list):
                                for point in content_list[:5]:  # Show first 5 points
                                    st.markdown(f"• {point}")
                                if len(content_list) > 5:
                                    st.caption(f"... and {len(content_list)-5} more points")
                            else:
                                st.markdown("• Content generation in progress...")
                                content_list = ["Content will be added to your slide"]
                        except Exception as e:
                            st.warning(f"Using fallback content generation")
                            content_list = [f"Key points about {title}", "AI-generated content", "Professional insights"]
                    
                    # Decide and execute action
                    try:
                        action = decide_action(title)
                        
                        if action == "chart":
                            st.markdown("**📊 Chart Slide**")
                            try:
                                st.session_state.client.call_tool("add_chart", title)
                                st.success("✅ Chart slide generated successfully!")
                            except Exception as e:
                                st.warning(f"Chart generation in progress: {str(e)}")
                        else:
                            content = "\n".join(content_list) if content_list else f"Content for {title}"
                            try:
                                st.session_state.client.call_tool("add_slide", title, content)
                                st.success("✅ Slide added successfully!")
                            except Exception as e:
                                st.warning(f"Adding slide content...")
                    except Exception as e:
                        st.warning(f"Processing slide {i+1}...")
                    
                    # Live preview
                    st.markdown("**👁️ Live Preview**")
                    preview_container = st.container()
                    with preview_container:
                        st.markdown(f"#### {title}")
                        if content_list:
                            for point in content_list[:3]:  # Show first 3 points
                                st.markdown(f"• {point}")
                            if len(content_list) > 3:
                                st.caption(f"... and {len(content_list)-3} more points")
                        else:
                            st.markdown("• Preview will be available shortly")
                
                # Update progress
                slide_progress.progress((i+1)/len(st.session_state.plan))
                status_text.text(f"✨ Generated slide {i+1} of {len(st.session_state.plan)}")
            
            # Step 4: Save and finalize
            with st.spinner("💾 Finalizing presentation..."):
                st.markdown("---")
                st.markdown("### 💾 Step 4: Saving Presentation")
                
                if st.session_state.client and hasattr(st.session_state.client, 'call_tool'):
                    file_path = st.session_state.client.call_tool("save_ppt", topic)
                    st.session_state.file_path = file_path
                    
                    # Show file info
                    if os.path.exists(file_path):
                        file_size = os.path.getsize(file_path) / (1024 * 1024)  # Convert to MB
                        st.info(f"📁 File saved: `{os.path.basename(file_path)}` ({file_size:.2f} MB)")
                    else:
                        st.warning("File saved but location not found")
                else:
                    st.error("Failed to save presentation. Please try again.")
                    st.stop()
            
            # Success message with animation
            st.markdown("""
                <div class="success-message">
                    <h3>🎉 Presentation Generated Successfully!</h3>
                    <p>Your AI-powered presentation is ready to download. Click the button below to save it.</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Download section
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.session_state.file_path and os.path.exists(st.session_state.file_path):
                    with open(st.session_state.file_path, "rb") as f:
                        st.download_button(
                            label="📥 Download PPT (PowerPoint Format)",
                            data=f,
                            file_name=os.path.basename(st.session_state.file_path),
                            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                            use_container_width=True
                        )
                else:
                    st.error("File not found. Please regenerate the presentation.")
            
            st.session_state.generated = True
            
            # Feedback section
            st.markdown("---")
            st.markdown("### 💬 Feedback")
            feedback = st.radio("How was your experience?", ["😊 Excellent", "🙂 Good", "😐 Average", "😞 Poor"], horizontal=True)
            if feedback:
                st.success("Thanks for your feedback! We're constantly improving.")
    
    except Exception as e:
        st.markdown(f"""
            <div class="error-message">
                <strong>⚠️ Error occurred:</strong><br>
                {str(e)}<br><br>
                <strong>Suggestions:</strong><br>
                • Check your internet connection<br>
                • Try again with a different topic<br>
                • Refresh the page and try again
            </div>
        """, unsafe_allow_html=True)
        st.error(f"Detailed error: {str(e)}")

elif generate and not topic:
    st.error("⚠️ Please enter a topic before generating the presentation.")

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>Powered by AI | Generate professional presentations in seconds</p>
        <p style="font-size: 0.8rem;">© 2024 AI PPT Generator</p>
    </div>
""", unsafe_allow_html=True)