from google import genai
import gradio as gr
import os 


# ==========================================
# 1. GEMINI API KEY
# ==========================================



api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


# ==========================================
# 2. CHATBOT FUNCTION
# ==========================================

def chatbot(message, history):

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=message
    )

    answer = response.text

    history = history or []

    history.append({
        "role": "user",
        "content": message
    })

    history.append({
        "role": "assistant",
        "content": answer
    })

    return history


# ==========================================
# 3. CUSTOM UI DESIGN
# ==========================================

custom_css = """

.gradio-container {

    background:
        radial-gradient(
            circle at top right,
            rgba(14, 116, 144, 0.25),
            transparent 35%
        ),

        radial-gradient(
            circle at bottom left,
            rgba(30, 64, 175, 0.25),
            transparent 35%
        ),

        linear-gradient(
            135deg,
            #020617,
            #0f172a,
            #172554
        ) !important;

    min-height: 100vh !important;
}


#main-card {

    max-width: 900px;
    margin: auto;
    padding: 18px;
}


#header {

    text-align: center;

    padding: 12px 20px;

    border-radius: 16px;

    background:
        linear-gradient(
            135deg,
            #0f766e,
            #0369a1
        );

    box-shadow:
        0 8px 25px rgba(0,0,0,0.30);

    margin-bottom: 14px;
}


#chatbot {

    border-radius: 18px !important;

    background:
        rgba(15,23,42,0.90) !important;

    border:
        1px solid rgba(148,163,184,0.15) !important;

    box-shadow:
        0 10px 30px rgba(0,0,0,0.30);

    overflow: hidden;
}


#textbox textarea {

    border-radius: 14px !important;

    background:
        #1e293b !important;

    color: white !important;

    border:
        1px solid #334155 !important;

    font-size: 15px !important;
}


#send-btn {

    background:
        linear-gradient(
            135deg,
            #0891b2,
            #2563eb
        ) !important;

    color: white !important;

    border: none !important;

    border-radius: 12px !important;

    font-weight: 600 !important;

    box-shadow:
        0 6px 18px rgba(37,99,235,0.30);
}


#clear-btn {

    background:
        #334155 !important;

    color: white !important;

    border:
        1px solid #475569 !important;

    border-radius: 12px !important;

    font-weight: 600 !important;
}


footer {
    display: none !important;
}

"""


# ==========================================
# 4. CREATE INTERFACE
# ==========================================

with gr.Blocks() as demo:

    with gr.Column(elem_id="main-card"):

        gr.HTML(
            """
            <div id="header">

                <div style="
                    font-size:30px;
                    margin-bottom:2px;
                ">
                    🤖
                </div>

                <h2 style="
                    color:white;
                    margin:2px 0;
                    font-size:23px;
                ">
                    Gemini AI Assistant
                </h2>

                <p style="
                    color:#dbeafe;
                    margin:2px 0;
                    font-size:13px;
                ">
                    Ask questions and get intelligent answers
                </p>

            </div>
            """
        )


        chat = gr.Chatbot(
            label="💬 Conversation",
            height=460,
            elem_id="chatbot"
        )


        message = gr.Textbox(
            placeholder="💬 Type your question here...",
            label="Your Message",
            lines=2,
            elem_id="textbox"
        )


        with gr.Row():

            send = gr.Button(
                "🚀 Send",
                elem_id="send-btn"
            )

            clear = gr.Button(
                "🧹 Clear Chat",
                elem_id="clear-btn"
            )


    # ======================================
    # SEND BUTTON
    # ======================================

    send.click(
        fn=chatbot,
        inputs=[message, chat],
        outputs=[chat]
    )


    # ======================================
    # ENTER KEY
    # ======================================

    message.submit(
        fn=chatbot,
        inputs=[message, chat],
        outputs=[chat]
    )


    # ======================================
    # CLEAR CHAT
    # ======================================

    clear.click(
        fn=lambda: [],
        inputs=None,
        outputs=[chat]
    )


# ==========================================
# 5. LAUNCH
# ==========================================

demo.launch(
    css=custom_css,
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", 7860))
)