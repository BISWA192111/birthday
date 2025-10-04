import gradio as gr
import datetime
import time
import base64
import socket
from io import BytesIO
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import threading

def find_free_port(start_port=7861, max_attempts=10):
    """Find a free port starting from start_port"""
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('', port))
                return port
        except OSError:
            continue
    return start_port  # Fallback to original port

class BirthdayApp:
    def __init__(self):
        self.target_date = datetime.datetime(2025, 10, 10, 0, 0, 0)
        self.celebration_started = False
    
    def get_countdown(self):
        """Calculate time remaining until October 10th"""
        now = datetime.datetime.now()
        time_diff = self.target_date - now
        
        if time_diff.total_seconds() <= 0:
            self.celebration_started = True
            return "🎉 HAPPY BIRTHDAY! 🎉", True
        
        days = time_diff.days
        hours, remainder = divmod(time_diff.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        countdown_text = f"⏰ Time until birthday: {days} days, {hours} hours, {minutes} minutes, {seconds} seconds"
        return countdown_text, False
    
    def create_cake_image(self, cut_progress=0):
        """Create a cake image with cutting animation"""
        # Create image
        width, height = 400, 300
        img = Image.new('RGB', (width, height), color='lightblue')
        draw = ImageDraw.Draw(img)
        
        # Draw cake base
        cake_x = width // 2
        cake_y = height - 50
        cake_width = 200
        cake_height = 120
        
        # Cake layers
        layer_colors = ['#8B4513', '#D2691E', '#F4A460']  # Brown shades
        layer_height = cake_height // 3
        
        for i, color in enumerate(layer_colors):
            y_pos = cake_y - (i + 1) * layer_height
            draw.rectangle([
                cake_x - cake_width//2, y_pos,
                cake_x + cake_width//2, y_pos + layer_height
            ], fill=color, outline='black', width=2)
        
        # Draw candles
        candle_count = 5
        candle_spacing = cake_width // (candle_count + 1)
        for i in range(candle_count):
            candle_x = cake_x - cake_width//2 + (i + 1) * candle_spacing
            candle_y = cake_y - cake_height
            
            # Candle stick
            draw.rectangle([
                candle_x - 3, candle_y - 20,
                candle_x + 3, candle_y
            ], fill='yellow')
            
            # Flame
            if not self.celebration_started or cut_progress < 0.5:
                draw.ellipse([
                    candle_x - 5, candle_y - 30,
                    candle_x + 5, candle_y - 20
                ], fill='orange')
        
        # Add cake cutting effect
        if cut_progress > 0:
            # Draw knife
            knife_x = cake_x + cake_width//2 - int(cut_progress * cake_width)
            knife_y = cake_y - cake_height//2
            
            draw.line([
                knife_x, knife_y - 30,
                knife_x, knife_y + 30
            ], fill='silver', width=4)
            
            # Draw cut line
            if cut_progress > 0.3:
                cut_x = cake_x + cake_width//2 - int(cut_progress * cake_width * 0.7)
                draw.line([
                    cut_x, cake_y - cake_height,
                    cut_x, cake_y
                ], fill='white', width=2)
        
        # Add decorations
        if self.celebration_started:
            # Add confetti
            for _ in range(20):
                x = np.random.randint(0, width)
                y = np.random.randint(0, height//2)
                color = np.random.choice(['red', 'blue', 'green', 'yellow', 'purple'])
                draw.ellipse([x-3, y-3, x+3, y+3], fill=color)
        
        # Add birthday message
        if cut_progress > 0.8:
            try:
                font = ImageFont.truetype("arial.ttf", 24)
            except:
                font = ImageFont.load_default()
            
            text = "🎂 Happy Birthday! 🎂"
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_x = (width - text_width) // 2
            draw.text((text_x, 20), text, fill='red', font=font)
        
        return img
    
    def animate_cake_cutting(self):
        """Generate frames for cake cutting animation"""
        frames = []
        for i in range(21):  # 21 frames for smooth animation
            cut_progress = i / 20.0
            img = self.create_cake_image(cut_progress)
            frames.append(img)
        return frames
    
    def create_placeholder_image(self):
        """Create a placeholder image before the special day"""
        width, height = 400, 300
        img = Image.new('RGB', (width, height), color='#f0f8ff')
        draw = ImageDraw.Draw(img)
        
        # Draw a simple calendar icon
        cal_width, cal_height = 150, 120
        cal_x = width // 2
        cal_y = height // 2
        
        # Calendar base
        draw.rectangle([
            cal_x - cal_width//2, cal_y - cal_height//2,
            cal_x + cal_width//2, cal_y + cal_height//2
        ], fill='white', outline='#333333', width=3)
        
        # Calendar top
        draw.rectangle([
            cal_x - cal_width//2, cal_y - cal_height//2,
            cal_x + cal_width//2, cal_y - cal_height//2 + 20
        ], fill='#ff6b6b', outline='#333333', width=2)
        
        # Calendar rings
        for i in [-30, 0, 30]:
            draw.ellipse([
                cal_x + i - 5, cal_y - cal_height//2 - 10,
                cal_x + i + 5, cal_y - cal_height//2 + 10
            ], fill='#333333')
        
        # Date text
        try:
            font = ImageFont.truetype("arial.ttf", 36)
        except:
            font = ImageFont.load_default()
        
        text = "10"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_x = cal_x - text_width // 2
        draw.text((text_x, cal_y - 10), text, fill='#333333', font=font)
        
        # Month text
        try:
            small_font = ImageFont.truetype("arial.ttf", 16)
        except:
            small_font = ImageFont.load_default()
        
        month_text = "October"
        bbox = draw.textbbox((0, 0), month_text, font=small_font)
        text_width = bbox[2] - bbox[0]
        text_x = cal_x - text_width // 2
        draw.text((text_x, cal_y + 25), month_text, fill='#666666', font=small_font)
        
        return img
    
    def update_display(self):
        """Update the countdown and display"""
        countdown_text, is_birthday = self.get_countdown()
        
        if is_birthday and not hasattr(self, 'cake_frames'):
            # Generate cake cutting animation frames
            self.cake_frames = self.animate_cake_cutting()
            self.current_frame = 0
        
        if hasattr(self, 'cake_frames'):
            # Show animated cake cutting
            current_img = self.cake_frames[self.current_frame % len(self.cake_frames)]
            self.current_frame += 1
            return countdown_text, current_img
        else:
            # Show placeholder until the special day
            placeholder_img = self.create_placeholder_image()
            return countdown_text, placeholder_img

# Initialize the app
birthday_app = BirthdayApp()

def update_birthday_display():
    """Function to update the display for Gradio"""
    return birthday_app.update_display()

def create_initial_display():
    """Create initial display image"""
    return birthday_app.create_placeholder_image()

# Create Gradio interface
with gr.Blocks(
    title="⏰ Countdown Timer App",
    theme=gr.themes.Soft(),
    css="""
    .main-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    .countdown-text {
        font-size: 24px;
        font-weight: bold;
        text-align: center;
        color: #ffffff !important;
        padding: 20px;
        background: rgba(0, 0, 0, 0.7);
        border-radius: 15px;
        margin: 10px;
    }
    .cake-container {
        text-align: center;
        padding: 20px;
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        margin: 10px;
    }
    .gradio-container .prose h1,
    .gradio-container .prose h2,
    .gradio-container .prose h3,
    .gradio-container .prose p,
    .gradio-container .prose li {
        color: #ffffff !important;
    }
    """
) as demo:
    
    gr.Markdown(
        """
        # ⏰ Countdown Timer
        ## Important date approaching!
        
        Keep an eye on the countdown - something special happens on October 10th! 📅
        """,
        elem_classes=["countdown-text"]
    )
    
    with gr.Row():
        with gr.Column():
            countdown_display = gr.Textbox(
                label="⏰ Countdown Timer",
                value=birthday_app.get_countdown()[0],
                interactive=False,
                elem_classes=["countdown-text"]
            )
        
    with gr.Row():
        with gr.Column():
            cake_display = gr.Image(
                label="📅 Special Date",
                value=create_initial_display(),
                elem_classes=["cake-container"]
            )
    
    with gr.Row():
        with gr.Column():
            gr.Markdown(
                """
                ### 📅 Event Features:
                - **Real-time countdown** to October 10th
                - **Special display** when the date arrives
                - **Interactive interface** with live updates
                - **Mysterious content** revealed at the right time
                
                *Something amazing will happen when the countdown reaches zero!* ✨
                """
            )
    
    # Auto-refresh using a button that triggers automatically
    with gr.Row():
        refresh_btn = gr.Button("🔄 Refresh", elem_id="refresh-btn", visible=True, size="sm")
    
    # Set up refresh functionality
    refresh_btn.click(
        fn=update_birthday_display,
        outputs=[countdown_display, cake_display]
    )
    
    # Initial load
    demo.load(
        fn=update_birthday_display,
        outputs=[countdown_display, cake_display]
    )
    
    # Add JavaScript for auto-refresh
    gr.HTML("""
    <script>
    let refreshInterval;
    function startAutoRefresh() {
        if (refreshInterval) clearInterval(refreshInterval);
        refreshInterval = setInterval(function() {
            const refreshBtn = document.querySelector('#refresh-btn button');
            if (refreshBtn) {
                refreshBtn.click();
            }
        }, 2000); // Refresh every 2 seconds instead of 1
    }
    // Start refresh after page loads
    setTimeout(startAutoRefresh, 2000);
    </script>
    """)

if __name__ == "__main__":
    # Find an available port
    original_port = 7861
    available_port = find_free_port(original_port)
    
    if available_port != original_port:
        print(f"⚠️  Port {original_port} is busy, using port {available_port} instead")
    
    print("⏰ Starting Countdown App...")
    print(f"📅 Target date: October 10th, 2025")
    print(f"🌟 Access the app at: http://localhost:{available_port}")
    
    # Detect if running on Hugging Face Spaces
    import os
    is_huggingface = os.getenv("SPACE_ID") is not None
    
    demo.launch(
        server_name="0.0.0.0",
        server_port=available_port,
        share=False if is_huggingface else True,  # Disable share on HF Spaces
        show_error=True
    )
