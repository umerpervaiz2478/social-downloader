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
