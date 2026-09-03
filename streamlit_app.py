import streamlit as st
import os
import glob
import time

# Import existing Python downloaders
from TikTokDownloader import download_and_move_vid
from RedditDownloader import download_and_move
from Instagram import download_instagram_post
from YouTubeDownloader import download_youtube_video

# ─── Page Configuration ────────────────────────────────────────────────────
st.set_page_config(
    page_title="Titanium Downloader — TikTok, Instagram & More",
    page_icon="⬇️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─── Folders ───────────────────────────────────────────────────────────────
TIKTOK_FOLDER = 'tiktok_videos'
INSTAGRAM_FOLDER = 'instagram_files'
REDDIT_FOLDER = 'reddit_videos'
YOUTUBE_FOLDER = 'youtube_files'

for f in [TIKTOK_FOLDER, INSTAGRAM_FOLDER, REDDIT_FOLDER, YOUTUBE_FOLDER]:
    os.makedirs(f, exist_ok=True)

# ─── Custom Dark Glassmorphic CSS ──────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .stApp {
        background-color: #0a0b10;
        color: #f8fafc;
    }
    
    /* Header Bar */
    .custom-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 1rem 0 2rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 2rem;
    }
    
    .brand-title {
        font-size: 1.4rem;
        font-weight: 800;
        color: #ffffff;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .brand-accent {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .creator-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.45rem;
        padding: 0.4rem 0.95rem;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 600;
        color: #94a3b8;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-decoration: none;
        transition: all 0.2s ease;
    }
    
    .creator-pill:hover {
        background: rgba(238, 42, 123, 0.15);
        border-color: rgba(238, 42, 123, 0.4);
        color: #ffffff;
        text-decoration: none;
    }
    
    /* Input Styling */
    .stTextInput input {
        background-color: rgba(18, 20, 29, 0.8) !important;
        border: 1.5px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        font-size: 1rem !important;
        padding: 0.75rem 1rem !important;
    }
    
    .stTextInput input:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2) !important;
    }
    
    /* Button */
    .stButton button {
        width: 100%;
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        transition: transform 0.15s ease !important;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        filter: brightness(1.1);
    }
    
    /* Download Success Box */
    .download-card {
        background: rgba(18, 20, 29, 0.8);
        border: 1px solid rgba(34, 197, 94, 0.3);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        margin-top: 1.5rem;
    }
</style>

<div class="custom-header">
    <div class="brand-title">
        <span>⬇️ Titanium<span class="brand-accent"> DL</span></span>
    </div>
    <a href="https://www.instagram.com/titanium_web27/" target="_blank" rel="noopener noreferrer" class="creator-pill">
        <span>Made by <strong>Umer</strong></span>
        <span>📸</span>
    </a>
</div>
""", unsafe_allow_html=True)

# ─── Hero ──────────────────────────────────────────────────────────────────
st.markdown("<h2 style='text-align: center; font-weight: 800; margin-bottom: 0.2rem;'>Social Media Video Downloader</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 0.95rem; margin-bottom: 2rem;'>Download TikTok, Instagram, Reddit, and YouTube videos directly with Python.</p>", unsafe_allow_html=True)

# ─── URL Input ─────────────────────────────────────────────────────────────
url = st.text_input(
    label="Video URL",
    placeholder="Paste TikTok, Instagram, Reddit, or YouTube link here...",
    label_visibility="collapsed"
)

# ─── Download Action ───────────────────────────────────────────────────────
if st.button("Download Video ⬇️", use_container_width=True):
    if not url or not url.strip():
        st.warning("⚠️ Please enter a video link first.")
    else:
        url = url.strip()
        target_path = None
        platform = None

        with st.spinner("Processing video... This may take a few seconds"):
            try:
                if 'tiktok.com' in url:
                    platform = "TikTok"
                    target_path = download_and_move_vid(url, TIKTOK_FOLDER)
                elif 'instagram.com' in url:
                    platform = "Instagram"
                    target_path = download_instagram_post(url, INSTAGRAM_FOLDER)
                elif 'reddit.com' in url or 'redd.it' in url:
                    platform = "Reddit"
                    target_path = download_and_move(url, REDDIT_FOLDER)
                elif 'youtube.com' in url or 'youtu.be' in url:
                    platform = "YouTube"
                    target_path = download_youtube_video(url, YOUTUBE_FOLDER)
                else:
                    st.error("❌ Unsupported URL. Please provide a valid TikTok, Instagram, Reddit, or YouTube link.")

            except Exception as e:
                st.error(f"Failed to process video: {str(e)}")

        if target_path and os.path.exists(target_path):
            st.success(f"✅ {platform} Video ready!")
            
            # Preview video
            st.video(target_path)
            
            # Direct Download button
            with open(target_path, "rb") as file:
                file_name = os.path.basename(target_path)
                st.download_button(
                    label=f"💾 Save {file_name} to Device",
                    data=file,
                    file_name=file_name,
                    mime="video/mp4",
                    use_container_width=True
                )
        elif target_path:
            st.warning("⚠️ Processing completed, but could not locate the output video.")

# ─── Footer ────────────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align: center; margin-top: 4rem; padding-top: 1.5rem; border-top: 1px solid rgba(255,255,255,0.08); color: #64748b; font-size: 0.8rem;'>
    Personal use only. Respect creators' rights. &copy; 2026 Titanium Downloader.
</div>
""", unsafe_allow_html=True)
