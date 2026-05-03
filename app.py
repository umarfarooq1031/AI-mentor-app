import os
import gradio as gr
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)

MODEL = "llama-3.3-70b-versatile"

# -------------------------------
# AI CALL FUNCTION
# -------------------------------
def ask_groq(prompt):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt}
            ],
            model=MODEL,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"


# -------------------------------
# FEATURE 1: AI MENTOR
# -------------------------------
def mentor_response(question):
    prompt = f"""
You are a friendly AI mentor for undergraduate students.
Explain the concept in a simple, clear way.

Include:
- Easy explanation
- Example
- Key points

Question: {question}
"""
    return ask_groq(prompt)


# -------------------------------
# FEATURE 2: UML + ERD GENERATOR
# -------------------------------
def generate_design(requirement):
    prompt = f"""
Generate system design for the following project:

{requirement}

Include:
1. UML (Use Case Diagram in text form)
2. Class Diagram (text)
3. ERD (Entities + Relationships)

Format clearly with headings.
"""
    return ask_groq(prompt)


# -------------------------------
# FEATURE 3: CODE GENERATOR
# -------------------------------
def generate_code(requirement):
    prompt = f"""
Generate a Python project skeleton for:

{requirement}

Include:
- Folder structure
- Main files
- Basic classes
- Starter functions

Keep it simple and beginner-friendly.
"""
    return ask_groq(prompt)


# -------------------------------
# GRADIO UI
# -------------------------------
with gr.Blocks(theme=gr.themes.Soft()) as app:

    gr.Markdown("""
# 🚀 AI Mentor for Learning
### Your Smart Study Buddy 😎
""")

    with gr.Tabs():

        # TAB 1
        with gr.Tab("📚 Ask Mentor"):
            question = gr.Textbox(label="Ask anything...")
            answer = gr.Textbox(label="Answer", lines=10)
            btn1 = gr.Button("Get Answer 💡")
            btn1.click(fn=mentor_response, inputs=question, outputs=answer)

        # TAB 2
        with gr.Tab("🧩 Generate Design"):
            req1 = gr.Textbox(label="Project idea")
            design_output = gr.Textbox(label="UML + ERD", lines=15)
            btn2 = gr.Button("Generate Design 🛠️")
            btn2.click(fn=generate_design, inputs=req1, outputs=design_output)

        # TAB 3
        with gr.Tab("💻 Generate Code"):
            req2 = gr.Textbox(label="Project requirement")
            code_output = gr.Textbox(label="Code Skeleton", lines=15)
            btn3 = gr.Button("Generate Code ⚡")
            btn3.click(fn=generate_code, inputs=req2, outputs=code_output)

    gr.Markdown("✨ Built for Students")

# Run app
app.launch()
