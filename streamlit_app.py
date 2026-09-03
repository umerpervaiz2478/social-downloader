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
    page_title="Titanium DL — Social Video Downloader",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─── Storage Folders ───────────────────────────────────────────────────────
TIKTOK_FOLDER = 'tiktok_videos'
INSTAGRAM_FOLDER = 'instagram_files'
REDDIT_FOLDER = 'reddit_videos'
YOUTUBE_FOLDER = 'youtube_files'

for f in [TIKTOK_FOLDER, INSTAGRAM_FOLDER, REDDIT_FOLDER, YOUTUBE_FOLDER]:
    os.makedirs(f, exist_ok=True)

# ─── Custom Dark Glassmorphic & Elegant CSS ────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');
    
    /* Base Reset & Typography */
    html, body, [class*="css"], .stMarkdown, .stText {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    
    /* Clean Chrome */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header[data-testid="stHeader"] {
        background: transparent !important;
    }
    
    /* Atmospheric Dark Mesh Gradient */
    .stApp {
        background: #090b14;
        background-image: 
            radial-gradient(at 5% 10%, rgba(99, 102, 241, 0.18) 0px, transparent 45%),
            radial-gradient(at 95% 15%, rgba(236, 72, 153, 0.15) 0px, transparent 45%),
            radial-gradient(at 50% 50%, rgba(139, 92, 246, 0.08) 0px, transparent 60%),
            radial-gradient(at 85% 90%, rgba(6, 182, 212, 0.14) 0px, transparent 50%),
            radial-gradient(at 15% 85%, rgba(16, 185, 129, 0.10) 0px, transparent 50%);
        background-attachment: fixed;
        color: #f8fafc;
    }
    
    /* Layout Container */
    .block-container {
        max-width: 760px !important;
        padding-top: 1.25rem !important;
        padding-bottom: 3.5rem !important;
    }

    /* ─── Top Navbar ────────────────────────────────────────────── */
    .custom-navbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.85rem 1.4rem;
        background: rgba(18, 22, 38, 0.65);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
        margin-bottom: 2rem;
    }
    
    .brand-group {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .brand-icon {
        width: 40px;
        height: 40px;
        border-radius: 12px;
        background: linear-gradient(135deg, #6366f1, #d946ef);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.25rem;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.45);
    }
    
    .brand-name {
        font-size: 1.25rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        color: #ffffff;
    }
    
    .brand-tag {
        font-size: 0.65rem;
        font-weight: 700;
        padding: 0.2rem 0.55rem;
        border-radius: 999px;
        background: rgba(99, 102, 241, 0.2);
        border: 1px solid rgba(99, 102, 241, 0.4);
        color: #a5b4fc;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        margin-left: 0.4rem;
    }
    
    .creator-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.45rem 1rem;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 600;
        color: #cbd5e1;
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-decoration: none !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .creator-badge:hover {
        background: linear-gradient(135deg, rgba(238, 42, 123, 0.2), rgba(129, 52, 175, 0.2));
        border-color: rgba(238, 42, 123, 0.5);
        color: #ffffff;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px -4px rgba(238, 42, 123, 0.4);
    }

    /* ─── Hero Section ───────────────────────────────────────────── */
    .hero-container {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .hero-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.45rem;
        padding: 0.35rem 0.95rem;
        border-radius: 999px;
        background: rgba(99, 102, 241, 0.12);
        border: 1px solid rgba(99, 102, 241, 0.32);
        color: #c7d2fe;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        margin-bottom: 1.1rem;
        box-shadow: 0 2px 12px rgba(99, 102, 241, 0.2);
    }
    
    .hero-title {
        font-size: 2.35rem;
        font-weight: 800;
        line-height: 1.22;
        letter-spacing: -0.03em;
        margin-bottom: 0.85rem;
        color: #ffffff;
    }
    
    .hero-gradient-text {
        background: linear-gradient(135deg, #818cf8 0%, #c084fc 45%, #f472b6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .hero-subtitle {
        color: #94a3b8;
        font-size: 1rem;
        font-weight: 400;
        max-width: 550px;
        margin: 0 auto 1.6rem;
        line-height: 1.6;
    }

    /* ─── Platform Showcase Chips ───────────────────────────────── */
    .platform-bar {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 0.65rem;
        margin-bottom: 2rem;
    }
    
    .platform-chip {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.4rem 0.95rem;
        border-radius: 12px;
        background: rgba(18, 22, 38, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        font-size: 0.82rem;
        font-weight: 600;
        color: #cbd5e1;
        transition: all 0.25s ease;
    }
    
    .platform-chip:hover {
        border-color: rgba(255, 255, 255, 0.25);
        background: rgba(255, 255, 255, 0.06);
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.35);
    }
    
    .dot-online {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background-color: #10b981;
        box-shadow: 0 0 8px #10b981;
    }

    /* ─── Glass Action Card ─────────────────────────────────────── */
    .glass-card {
        background: rgba(18, 22, 38, 0.72);
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 24px;
        padding: 1.8rem;
        box-shadow: 0 20px 45px -15px rgba(0, 0, 0, 0.65), inset 0 1px 0 rgba(255, 255, 255, 0.12);
        margin-bottom: 2rem;
    }

    /* ─── Input Field Styling ────────────────────────────────────── */
    .stTextInput > div > div > input {
        background: rgba(11, 14, 25, 0.85) !important;
        border: 1.5px solid rgba(255, 255, 255, 0.14) !important;
        border-radius: 14px !important;
        color: #ffffff !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        padding: 0.95rem 1.2rem !important;
        box-shadow: inset 0 2px 6px rgba(0, 0, 0, 0.45) !important;
        transition: all 0.25s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #818cf8 !important;
        box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.25), 0 0 20px rgba(99, 102, 241, 0.2), inset 0 2px 4px rgba(0, 0, 0, 0.3) !important;
        background: rgba(15, 18, 32, 0.95) !important;
    }

    .stTextInput > div > div > input::placeholder {
        color: #64748b !important;
        font-size: 0.92rem !important;
    }

    /* ─── Primary Action Button (st.button) ──────────────────────── */
    div[data-testid="stButton"] > button {
        width: 100% !important;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 45%, #d946ef 100%) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.22) !important;
        border-radius: 14px !important;
        padding: 0.85rem 1.6rem !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        letter-spacing: 0.02em !important;
        box-shadow: 0 6px 20px -2px rgba(124, 58, 237, 0.48), inset 0 1px 0 rgba(255, 255, 255, 0.35) !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        cursor: pointer !important;
        position: relative !important;
        overflow: hidden !important;
    }

    div[data-testid="stButton"] > button:hover {
        transform: translateY(-2.5px) !important;
        box-shadow: 0 12px 28px -4px rgba(124, 58, 237, 0.7), 0 0 25px rgba(217, 70, 239, 0.35), inset 0 1px 0 rgba(255, 255, 255, 0.5) !important;
        filter: brightness(1.1) !important;
        border-color: rgba(255, 255, 255, 0.4) !important;
    }

    div[data-testid="stButton"] > button:active {
        transform: translateY(1px) scale(0.985) !important;
        box-shadow: 0 3px 10px rgba(124, 58, 237, 0.4) !important;
        filter: brightness(0.95) !important;
    }

    /* ─── Download Button (st.download_button) ───────────────────── */
    div[data-testid="stDownloadButton"] > button {
        width: 100% !important;
        background: linear-gradient(135deg, #059669 0%, #10b981 50%, #06b6d4 100%) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.25) !important;
        border-radius: 14px !important;
        padding: 0.9rem 1.6rem !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        letter-spacing: 0.02em !important;
        box-shadow: 0 6px 22px -2px rgba(16, 185, 129, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.35) !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        cursor: pointer !important;
        margin-top: 0.5rem !important;
    }

    div[data-testid="stDownloadButton"] > button:hover {
        transform: translateY(-2.5px) !important;
        box-shadow: 0 12px 30px -4px rgba(16, 185, 129, 0.7), 0 0 25px rgba(6, 182, 212, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.5) !important;
        filter: brightness(1.1) !important;
        border-color: rgba(255, 255, 255, 0.45) !important;
    }

    div[data-testid="stDownloadButton"] > button:active {
        transform: translateY(1px) scale(0.985) !important;
        box-shadow: 0 3px 10px rgba(16, 185, 129, 0.4) !important;
    }

    /* ─── Detected Platform Dynamic Pill ────────────────────────── */
    .detected-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.42rem 0.95rem;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 700;
        margin-bottom: 0.95rem;
        border: 1px solid rgba(255, 255, 255, 0.15);
        animation: fadeIn 0.3s ease-in-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-4px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .detected-tiktok {
        background: rgba(0, 242, 234, 0.12);
        color: #00f2ea;
        border-color: rgba(0, 242, 234, 0.4);
        box-shadow: 0 0 15px rgba(0, 242, 234, 0.2);
    }

    .detected-instagram {
        background: rgba(225, 48, 108, 0.15);
        color: #ff5b99;
        border-color: rgba(225, 48, 108, 0.4);
        box-shadow: 0 0 15px rgba(225, 48, 108, 0.2);
    }

    .detected-reddit {
        background: rgba(255, 69, 0, 0.15);
        color: #ff6535;
        border-color: rgba(255, 69, 0, 0.4);
        box-shadow: 0 0 15px rgba(255, 69, 0, 0.2);
    }

    .detected-youtube {
        background: rgba(255, 0, 0, 0.14);
        color: #ff4d4d;
        border-color: rgba(255, 0, 0, 0.4);
        box-shadow: 0 0 15px rgba(255, 0, 0, 0.2);
    }

    /* ─── Video Result Card ─────────────────────────────────────── */
    .result-card {
        background: rgba(18, 22, 38, 0.75);
        border: 1px solid rgba(16, 185, 129, 0.35);
        border-radius: 20px;
        padding: 1.4rem 1.6rem;
        backdrop-filter: blur(20px);
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 16px 36px -10px rgba(16, 185, 129, 0.18);
        animation: fadeIn 0.35s ease;
    }

    .result-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .result-tag {
        font-size: 0.95rem;
        font-weight: 700;
        color: #34d399;
        display: flex;
        align-items: center;
        gap: 0.45rem;
    }

    .result-size {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.82rem;
        color: #cbd5e1;
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 0.3rem 0.7rem;
        border-radius: 8px;
    }

    /* ─── Video Player Frame ────────────────────────────────────── */
    div[data-testid="stVideo"] {
        border-radius: 18px !important;
        overflow: hidden !important;
        border: 1px solid rgba(255, 255, 255, 0.14) !important;
        box-shadow: 0 14px 35px rgba(0, 0, 0, 0.5) !important;
        margin-bottom: 1.25rem !important;
    }

    /* ─── Status Alerts Polish ──────────────────────────────────── */
    div[data-testid="stAlert"] {
        background: rgba(18, 22, 38, 0.85) !important;
        backdrop-filter: blur(16px) !important;
        border-radius: 16px !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        color: #f1f5f9 !important;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3) !important;
    }

    /* ─── Feature Highlights Strip ──────────────────────────────── */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
        gap: 0.85rem;
        margin-top: 2rem;
        margin-bottom: 2rem;
    }

    .feature-box {
        background: rgba(255, 255, 255, 0.028);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 16px;
        padding: 1rem 0.85rem;
        text-align: center;
        transition: all 0.25s ease;
    }

    .feature-box:hover {
        background: rgba(255, 255, 255, 0.055);
        border-color: rgba(99, 102, 241, 0.35);
        transform: translateY(-2px);
    }

    .feature-icon {
        font-size: 1.35rem;
        margin-bottom: 0.35rem;
    }

    .feature-label {
        font-size: 0.82rem;
        font-weight: 700;
        color: #e2e8f0;
    }

    .feature-sub {
        font-size: 0.72rem;
        color: #94a3b8;
        margin-top: 0.15rem;
    }

    /* ─── Footer ────────────────────────────────────────────────── */
    .custom-footer {
        text-align: center;
        margin-top: 3.5rem;
        padding-top: 1.5rem;
        border-top: 1px solid rgba(255, 255, 255, 0.07);
        color: #64748b;
        font-size: 0.82rem;
        line-height: 1.6;
    }
</style>

<!-- Top Navigation Bar -->
<div class="custom-navbar">
    <div class="brand-group">
        <div class="brand-icon">⚡</div>
        <div>
            <span class="brand-name">Titanium</span>
            <span class="brand-tag">PRO</span>
        </div>
    </div>
    <a href="https://www.instagram.com/titanium_web27/" target="_blank" rel="noopener noreferrer" class="creator-badge">
        <span>Curated by <strong>Umer</strong></span>
        <span>📸</span>
    </a>
</div>

<!-- Hero Area -->
<div class="hero-container">
    <div class="hero-pill">
        <span>✨ Next-Gen Media Extractor</span>
    </div>
    <h1 class="hero-title">
        Download Videos from <br/><span class="hero-gradient-text">Any Platform Instantly</span>
    </h1>
    <p class="hero-subtitle">
        High-performance downloader for TikTok, Instagram, Reddit, and YouTube. Clean, fast, and watermark-free video downloads right to your device.
    </p>
</div>

<!-- Supported Platforms Row -->
<div class="platform-bar">
    <div class="platform-chip">
        <span class="dot-online"></span>
        <span>🎵 TikTok</span>
    </div>
    <div class="platform-chip">
        <span class="dot-online"></span>
        <span>📸 Instagram Reels & Posts</span>
    </div>
    <div class="platform-chip">
        <span class="dot-online"></span>
        <span>🤖 Reddit Clips</span>
    </div>
    <div class="platform-chip">
        <span class="dot-online"></span>
        <span>🎬 YouTube Shorts & Videos</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── URL Detection Helper ───────────────────────────────────────────────────
def detect_platform(raw_url: str):
    if not raw_url:
        return None
    url_l = raw_url.lower().strip()
    if 'tiktok.com' in url_l:
        return ("TikTok", "detected-tiktok", "🎵 TikTok Video")
    elif 'instagram.com' in url_l:
        return ("Instagram", "detected-instagram", "📸 Instagram Reel / Post")
    elif 'reddit.com' in url_l or 'redd.it' in url_l:
        return ("Reddit", "detected-reddit", "🤖 Reddit Video Post")
    elif 'youtube.com' in url_l or 'youtu.be' in url_l:
        return ("YouTube", "detected-youtube", "🎬 YouTube Video / Short")
    return None

# ─── Glass Card & Input Form ────────────────────────────────────────────────
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

url_input = st.text_input(
    label="Video URL",
    placeholder="Paste link here (e.g., https://www.instagram.com/reel/... or https://vt.tiktok.com/...)",
    label_visibility="collapsed"
)

# Live platform detection feedback
detected = detect_platform(url_input)
if detected:
    st.markdown(f"""
        <div class="detected-badge {detected[1]}">
            <span>✨ {detected[2]} detected</span>
        </div>
    """, unsafe_allow_html=True)

# Primary Interactive Action Button
download_pressed = st.button("🚀 Fetch & Process Video", use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

# ─── Download Logic & Execution ─────────────────────────────────────────────
if download_pressed:
    if not url_input or not url_input.strip():
        st.warning("⚠️ Please paste a valid video URL first to begin download.")
    else:
        url = url_input.strip()
        target_path = None
        platform = None

        with st.spinner("⚡ Fetching and preparing high-definition media... Please wait"):
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
                    st.error("❌ Unsupported link format. Please provide a valid TikTok, Instagram, Reddit, or YouTube URL.")

            except Exception as e:
                st.error(f"❌ Failed to process video: {str(e)}")

        # ─── Video Display & Download Action ─────────────────────────────────
        if target_path and os.path.exists(target_path):
            file_name = os.path.basename(target_path)
            file_size_mb = os.path.getsize(target_path) / (1024 * 1024)

            st.markdown(f"""
            <div class="result-card">
                <div class="result-header">
                    <span class="result-tag">✅ {platform} Video Ready</span>
                    <span class="result-size">{file_size_mb:.2f} MB</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Embedded Preview
            st.video(target_path)

            # Glowing Download Button
            with open(target_path, "rb") as file_handle:
                st.download_button(
                    label=f"💾 Save {file_name} to Device",
                    data=file_handle,
                    file_name=file_name,
                    mime="video/mp4",
                    use_container_width=True
                )
        elif target_path:
            st.warning("⚠️ Processing completed, but the output file could not be located on disk.")

# ─── Value Props / Features Grid ───────────────────────────────────────────
st.markdown("""
<div class="feature-grid">
    <div class="feature-box">
        <div class="feature-icon">⚡</div>
        <div class="feature-label">Blazing Fast</div>
        <div class="feature-sub">Direct stream extraction</div>
    </div>
    <div class="feature-box">
        <div class="feature-icon">💎</div>
        <div class="feature-label">Original HD</div>
        <div class="feature-sub">Max available resolution</div>
    </div>
    <div class="feature-box">
        <div class="feature-icon">🚫</div>
        <div class="feature-label">No Watermarks</div>
        <div class="feature-sub">Clean export where possible</div>
    </div>
    <div class="feature-box">
        <div class="feature-icon">🔒</div>
        <div class="feature-label">100% Free</div>
        <div class="feature-sub">No signup or limits</div>
    </div>
</div>

<div class="custom-footer">
    <div>Crafted for personal and creative use &bull; Respect creator intellectual property rights</div>
    <div style="margin-top: 0.35rem; color: #475569;">&copy; 2026 Titanium DL &bull; Powered by Streamlit & Python</div>
</div>
""", unsafe_allow_html=True)
