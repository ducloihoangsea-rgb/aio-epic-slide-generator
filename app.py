"""
AIO Epic Slide Generator
A user-friendly, bilingual Streamlit application that generates highly styled
PowerPoint presentations from structured JSON data and background images.

Supports: English & Vietnamese (Tiếng Anh & Tiếng Việt)
"""

import json
from io import BytesIO
from PIL import Image as PILImage

import streamlit as st
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor


# =============================================================================
# INTERNATIONALIZATION (I18N) — Bilingual Support
# =============================================================================

I18N = {
    "en": {
        "page_title": "AIO Epic Slide Generator",
        "header_title": "AIO Epic Slide Generator",
        "header_subtitle": "Create cinematic, professional presentations in seconds. Upload your data and images — we'll handle the design.",
        "lang_label": "🌐 Language / Ngôn ngữ",
        "step1_title": "📁 Step 1: Upload Your Data",
        "json_label": "Upload JSON Data File (.json)",
        "json_help": "Upload a structured JSON file containing your slide content.",
        "image_label": "Upload Background Images (.png, .jpg, .jpeg)",
        "image_help": "Upload one or more background images. File names must match the 'image_filename' values in your JSON.",
        "step2_title": "🔍 Step 2: Preview Your Slides",
        "no_json": "⬅️ Please upload a JSON file to preview your slides.",
        "preview_slide": "Slide",
        "preview_title": "Title",
        "preview_bullets": "Bullet Points",
        "preview_image": "Background Image",
        "preview_image_missing": "⚠️ Image not uploaded yet",
        "step3_title": "🚀 Step 3: Generate Presentation",
        "generate_btn": "✨ Generate Epic Presentation",
        "generate_disabled": "Please upload both a JSON file and at least one background image to enable generation.",
        "generating": "Designing your epic presentation... Please wait.",
        "success_msg": "🎉 Your presentation is ready! Download it below.",
        "download_btn": "📥 Download Epic Presentation (.pptx)",
        "error_json_decode": "JSON Parsing Error: {}. Please check your file format.",
        "error_invalid_json": "Invalid JSON structure. The 'slides' key was not found.",
        "error_generic": "An unexpected error occurred: {}",
        "sidebar_guide_title": "📖 Quick Guide",
        "sidebar_guide_text": """
**1. Prepare JSON:** Create a file with your slide text.  
**2. Prepare Images:** Collect background images. Names must match JSON.  
**3. Upload:** Use the panel on the left.  
**4. Generate:** Click the big button below.  
**5. Download:** Get your `.pptx` file instantly.
""",
        "example_json_title": "📋 JSON Example Structure",
        "footer": "Made with ❤️ by AIO | Streamlit Cloud Ready",
        "slide_count": "slides detected",
        "image_count": "images uploaded",
        "status_ready": "Ready to generate",
        "status_waiting": "Waiting for uploads...",
    },
    "vi": {
        "page_title": "AIO Epic Slide Generator",
        "header_title": "AIO Epic Slide Generator",
        "header_subtitle": "Tạo bài thuyết trình điện ảnh, chuyên nghiệp chỉ trong vài giây. Tải lên dữ liệu và hình ảnh — phần còn lại để chúng tôi lo.",
        "lang_label": "🌐 Ngôn ngữ / Language",
        "step1_title": "📁 Bước 1: Tải lên dữ liệu",
        "json_label": "Tải lên file JSON (.json)",
        "json_help": "Tải lên file JSON có cấu trúc chứa nội dung các slide.",
        "image_label": "Tải lên ảnh nền (.png, .jpg, .jpeg)",
        "image_help": "Tải lên một hoặc nhiều ảnh nền. Tên file phải khớp với giá trị 'image_filename' trong JSON.",
        "step2_title": "🔍 Bước 2: Xem trước nội dung",
        "no_json": "⬅️ Vui lòng tải lên file JSON để xem trước các slide.",
        "preview_slide": "Slide",
        "preview_title": "Tiêu đề",
        "preview_bullets": "Nội dung chính",
        "preview_image": "Ảnh nền",
        "preview_image_missing": "⚠️ Chưa tải lên ảnh này",
        "step3_title": "🚀 Bước 3: Tạo bài thuyết trình",
        "generate_btn": "✨ Tạo bài thuyết trình",
        "generate_disabled": "Vui lòng tải lên cả file JSON và ít nhất một ảnh nền để bắt đầu.",
        "generating": "Đang thiết kế bài thuyết trình của bạn... Vui lòng đợi.",
        "success_msg": "🎉 Bài thuyết trình đã sẵn sàng! Tải xuống bên dưới.",
        "download_btn": "📥 Tải xuống Epic Presentation (.pptx)",
        "error_json_decode": "Lỗi phân tích JSON: {}. Vui lòng kiểm tra định dạng file.",
        "error_invalid_json": "Cấu trúc JSON không hợp lệ. Không tìm thấy khóa 'slides'.",
        "error_generic": "Đã xảy ra lỗi không mong muốn: {}",
        "sidebar_guide_title": "📖 Hướng dẫn nhanh",
        "sidebar_guide_text": """
**1. Chuẩn bị JSON:** Tạo file chứa nội dung slide.  
**2. Chuẩn bị ảnh:** Thu thập ảnh nền. Tên phải khớp với JSON.  
**3. Tải lên:** Dùng bảng bên trái.  
**4. Tạo:** Nhấn nút lớn bên dưới.  
**5. Tải xuống:** Nhận file `.pptx` ngay lập tức.
""",
        "example_json_title": "📋 Cấu trúc JSON mẫu",
        "footer": "Được tạo bởi AIO ❤️ | Tương thích Streamlit Cloud",
        "slide_count": "slide được tìm thấy",
        "image_count": "ảnh đã tải lên",
        "status_ready": "Sẵn sàng tạo",
        "status_waiting": "Đang chờ tải lên...",
    }
}


def get_text(key: str, lang: str = "en") -> str:
    """
    Retrieve a translated string by key for the selected language.
    """
    return I18N.get(lang, I18N["en"]).get(key, key)


# =============================================================================
# CONSTANTS
# =============================================================================

SLIDE_WIDTH = Inches(16)
SLIDE_HEIGHT = Inches(9)

# Overlay dimensions (left half of the slide)
OVERLAY_LEFT = Inches(0)
OVERLAY_TOP = Inches(0)
OVERLAY_WIDTH = Inches(8)
OVERLAY_HEIGHT = Inches(9)

# Typography settings
TITLE_FONT_NAME = "Arial"
TITLE_FONT_SIZE = Pt(48)
TITLE_COLOR = RGBColor(255, 215, 0)  # Gold

BULLET_FONT_NAME = "Arial"
BULLET_FONT_SIZE = Pt(24)
BULLET_COLOR = RGBColor(255, 255, 255)  # White

# Layout positioning
TITLE_LEFT = Inches(0.75)
TITLE_TOP = Inches(1.5)
TITLE_WIDTH = Inches(6.5)
TITLE_HEIGHT = Inches(2.0)

BULLETS_LEFT = Inches(0.75)
BULLETS_TOP = Inches(4.0)
BULLETS_WIDTH = Inches(6.5)
BULLETS_HEIGHT = Inches(4.0)

# Overlay opacity (0-255)
OVERLAY_OPACITY = int(255 * 0.60)

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def create_overlay_image() -> BytesIO:
    """
    Generate a black PNG image with 60% opacity using Pillow.
    Returns an in-memory BytesIO buffer.
    """
    dpi = 96
    width_px = int(8 * dpi)
    height_px = int(9 * dpi)

    overlay_rgba = PILImage.new(
        "RGBA", (width_px, height_px), (0, 0, 0, OVERLAY_OPACITY)
    )

    img_buffer = BytesIO()
    overlay_rgba.save(img_buffer, format="PNG")
    img_buffer.seek(0)
    return img_buffer


def add_background_image(slide, image_bytes: BytesIO) -> None:
    """Add a full-bleed background image to a slide."""
    slide.shapes.add_picture(
        image_bytes,
        Inches(0),
        Inches(0),
        width=SLIDE_WIDTH,
        height=SLIDE_HEIGHT
    )


def add_dark_overlay(slide) -> None:
    """Add a semi-transparent dark overlay to the left half of the slide."""
    overlay_buffer = create_overlay_image()
    slide.shapes.add_picture(
        overlay_buffer,
        OVERLAY_LEFT,
        OVERLAY_TOP,
        width=OVERLAY_WIDTH,
        height=OVERLAY_HEIGHT
    )


def add_title_textbox(slide, title_text: str) -> None:
    """Add a styled title textbox to the slide."""
    textbox = slide.shapes.add_textbox(
        TITLE_LEFT,
        TITLE_TOP,
        TITLE_WIDTH,
        TITLE_HEIGHT
    )
    text_frame = textbox.text_frame
    text_frame.word_wrap = True

    paragraph = text_frame.paragraphs[0]
    paragraph.alignment = PP_ALIGN.LEFT

    run = paragraph.add_run()
    run.text = title_text.upper()
    run.font.name = TITLE_FONT_NAME
    run.font.size = TITLE_FONT_SIZE
    run.font.bold = True
    run.font.color.rgb = TITLE_COLOR


def add_bullet_textbox(slide, bullets: list) -> None:
    """Add styled bullet points to the slide."""
    textbox = slide.shapes.add_textbox(
        BULLETS_LEFT,
        BULLETS_TOP,
        BULLETS_WIDTH,
        BULLETS_HEIGHT
    )
    text_frame = textbox.text_frame
    text_frame.word_wrap = True

    for idx, bullet_text in enumerate(bullets):
        if idx == 0:
            paragraph = text_frame.paragraphs[0]
        else:
            paragraph = text_frame.add_paragraph()

        paragraph.alignment = PP_ALIGN.LEFT
        paragraph.level = 0

        run = paragraph.add_run()
        run.text = str(bullet_text)
        run.font.name = BULLET_FONT_NAME
        run.font.size = BULLET_FONT_SIZE
        run.font.color.rgb = BULLET_COLOR


def build_slide(slide, slide_data: dict, image_map: dict) -> None:
    """
    Build a single slide with background, overlay, and typography.
    """
    image_filename = slide_data.get("image_filename")
    if image_filename and image_filename in image_map:
        add_background_image(slide, image_map[image_filename])

    add_dark_overlay(slide)

    title = slide_data.get("title", "")
    if title:
        add_title_textbox(slide, title)

    bullets = slide_data.get("bullets", [])
    if bullets:
        add_bullet_textbox(slide, bullets)


def generate_presentation(json_data: dict, image_map: dict) -> BytesIO:
    """
    Generate the complete PowerPoint presentation in memory.
    """
    prs = Presentation()
    prs.slide_width = SLIDE_WIDTH
    prs.slide_height = SLIDE_HEIGHT

    blank_layout = prs.slide_layouts[6]

    slides = json_data.get("slides", [])
    for slide_data in slides:
        slide = prs.slides.add_slide(blank_layout)
        build_slide(slide, slide_data, image_map)

    pptx_buffer = BytesIO()
    prs.save(pptx_buffer)
    pptx_buffer.seek(0)
    return pptx_buffer


# =============================================================================
# UI COMPONENTS
# =============================================================================

def render_sidebar(lang: str) -> tuple:
    """
    Render the sidebar with uploaders and quick guide.
    Returns (json_file, image_files, image_map).
    """
    st.sidebar.markdown(f"## {get_text('sidebar_guide_title', lang)}")
    st.sidebar.info(get_text("sidebar_guide_text", lang))

    st.sidebar.markdown("---")
    st.sidebar.markdown(f"### {get_text('step1_title', lang)}")

    json_file = st.sidebar.file_uploader(
        label=get_text("json_label", lang),
        type=["json"],
        accept_multiple_files=False,
        help=get_text("json_help", lang)
    )

    image_files = st.sidebar.file_uploader(
        label=get_text("image_label", lang),
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=True,
        help=get_text("image_help", lang)
    )

    image_map = {}
    if image_files:
        for img in image_files:
            image_map[img.name] = BytesIO(img.read())

    return json_file, image_files, image_map


def render_preview(json_data: dict, image_map: dict, lang: str) -> None:
    """
    Render a user-friendly preview of slides before generation.
    """
    st.markdown(f"## {get_text('step2_title', lang)}")

    if not json_data or "slides" not in json_data:
        st.info(get_text("no_json", lang))
        return

    slides = json_data.get("slides", [])

    for idx, slide in enumerate(slides):
        with st.expander(
            f"🎬 {get_text('preview_slide', lang)} {slide.get('slide_number', idx + 1)}: "
            f"{slide.get('title', 'Untitled')}",
            expanded=(idx == 0)
        ):
            col1, col2 = st.columns([2, 1])

            with col1:
                st.markdown(f"**{get_text('preview_title', lang)}:**")
                st.write(f"_{slide.get('title', '')}_")

                st.markdown(f"**{get_text('preview_bullets', lang)}:**")
                for bullet in slide.get("bullets", []):
                    st.write(f"• {bullet}")

            with col2:
                img_name = slide.get("image_filename", "")
                st.markdown(f"**{get_text('preview_image', lang)}:**")
                st.code(img_name, language="text")
                if img_name in image_map:
                    st.success("✅ OK")
                else:
                    st.warning(get_text("preview_image_missing", lang))


def render_json_example(lang: str) -> None:
    """Render a collapsible JSON example."""
    with st.expander(get_text("example_json_title", lang), expanded=False):
        example = """{
  "slides": [
    {
      "slide_number": 1,
      "title": "CÚ SỐC CHUỖI CUNG ỨNG",
      "bullets": [
        "Container rơi xuống biển.",
        "Hậu quả tài chính nặng nề."
      ],
      "image_filename": "epic_bg_1.jpg"
    },
    {
      "slide_number": 2,
      "title": "GIẢI PHÁP CÔNG NGHỆ",
      "bullets": [
        "AI dự đoán rủi ro.",
        "Tự động hóa quy trình."
      ],
      "image_filename": "epic_bg_2.jpg"
    }
  ]
}"""
        st.code(example, language="json")


# =============================================================================
# MAIN APPLICATION
# =============================================================================

def main() -> None:
    """Main entry point for the Streamlit application."""
    st.set_page_config(
        page_title="AIO Epic Slide Generator",
        page_icon="🎬",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Custom CSS for better visuals
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.8rem;
        font-weight: 800;
        color: #FF4B4B;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #6c757d;
        text-align: center;
        margin-bottom: 2rem;
    }
    .status-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8f9fa;
        border-left: 4px solid #FF4B4B;
    }
    .footer {
        text-align: center;
        color: #6c757d;
        margin-top: 3rem;
        font-size: 0.85rem;
    }
    div[data-testid="stDownloadButton"] button {
        background-color: #28a745;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
    }
    div[data-testid="stDownloadButton"] button:hover {
        background-color: #218838;
    }
    </style>
    """, unsafe_allow_html=True)

    # Language selector at the very top (even above sidebar)
    lang = st.radio(
        label="🌐 Language / Ngôn ngữ",
        options=["en", "vi"],
        format_func=lambda x: "🇺🇸 English" if x == "en" else "🇻🇳 Tiếng Việt",
        horizontal=True,
        label_visibility="collapsed"
    )

    # Header
    st.markdown(f'<div class="main-header">{get_text("header_title", lang)}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sub-header">{get_text("header_subtitle", lang)}</div>', unsafe_allow_html=True)

    # Sidebar uploads
    json_file, image_files, image_map = render_sidebar(lang)

    # Main layout
    col_left, col_right = st.columns([2, 1])

    with col_left:
        # JSON Example
        render_json_example(lang)

        # Status indicator
        st.markdown("---")
        status_col1, status_col2, status_col3 = st.columns(3)

        slide_count = 0
        if json_file:
            try:
                json_file.seek(0)
                preview_data = json.load(json_file)
                slide_count = len(preview_data.get("slides", []))
            except:
                slide_count = 0

        with status_col1:
            st.metric(
                label=get_text("slide_count", lang).title(),
                value=slide_count
            )
        with status_col2:
            st.metric(
                label=get_text("image_count", lang).title(),
                value=len(image_files)
            )
        with status_col3:
            if json_file and len(image_files) > 0 and slide_count > 0:
                st.metric(
                    label="Status",
                    value=get_text("status_ready", lang)
                )
            else:
                st.metric(
                    label="Status",
                    value=get_text("status_waiting", lang)
                )

    with col_right:
        # Quick tip card
        st.info("""
        💡 **Pro Tip:**
        Tên file ảnh trong JSON phải khớp **chính xác** với tên file bạn tải lên.
        Ví dụ: `"epic_bg_1.jpg"` ↔️ `epic_bg_1.jpg`
        """)

    # Divider
    st.markdown("---")

    # Preview section
    preview_data = None
    if json_file:
        try:
            json_file.seek(0)
            preview_data = json.load(json_file)
        except:
            preview_data = None

    render_preview(preview_data, image_map, lang)

    # Divider
    st.markdown("---")

    # Generation section
    st.markdown(f"## {get_text('step3_title', lang)}")

    can_generate = (
        json_file is not None
        and len(image_files) > 0
        and preview_data is not None
        and "slides" in preview_data
    )

    if not can_generate:
        st.info(get_text("generate_disabled", lang))

    if st.button(
        label=get_text("generate_btn", lang),
        disabled=not can_generate,
        type="primary",
        use_container_width=True
    ):
        try:
            with st.spinner(get_text("generating", lang)):
                json_file.seek(0)
                json_data = json.load(json_file)

                if "slides" not in json_data:
                    st.error(get_text("error_invalid_json", lang))
                    st.stop()

                pptx_buffer = generate_presentation(json_data, image_map)

            st.success(get_text("success_msg", lang))
            st.balloons()

            st.download_button(
                label=get_text("download_btn", lang),
                data=pptx_buffer,
                file_name="Epic_Presentation.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                type="primary",
                use_container_width=True
            )

        except json.JSONDecodeError as e:
            st.error(get_text("error_json_decode", lang).format(e))
        except Exception as e:
            st.error(get_text("error_generic", lang).format(e))

    # Footer
    st.markdown(f'<div class="footer">{get_text("footer", lang)}</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
