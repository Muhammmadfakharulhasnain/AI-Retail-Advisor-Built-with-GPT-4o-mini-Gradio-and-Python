import os
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr

# === Load Environment Variables ===
load_dotenv(override=True)
openai_api_key = os.getenv('OPENAI_API_KEY')

if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set")

# === Initialize OpenAI Client ===
openai = OpenAI(api_key=openai_api_key)
MODEL = 'gpt-4o-mini'

# === Base System Message ===
system_message = (
    "You are a helpful assistant in a clothes store. You should try to gently encourage "
    "the customer to try items that are on sale. Hats are 60% off, and most other items are 50% off. "
    "For example, if the customer says 'I'm looking to buy a hat', you could reply something like, "
    "'Wonderful - we have lots of hats - including several that are part of our sales event.' "
    "Encourage the customer to buy hats if they are unsure what to get."
)

system_message += (
    "\nIf the customer asks for shoes, you should respond that shoes are not on sale today, "
    "but remind the customer to look at hats!"
)

# === Chat Function ===
def chat(message, history):
    relevant_system_message = system_message

    if 'belt' in message.lower():
        relevant_system_message += " The store does not sell belts; if you are asked for belts, be sure to point out other items on sale."

    messages = [{"role": "system", "content": relevant_system_message}] + history + [{"role": "user", "content": message}]
    stream = openai.chat.completions.create(model=MODEL, messages=messages)

    response = ""
    for chunk in stream:
        response += chunk.choices[0].delta.content or ''
        yield response

# === Use Built-in Dark Theme ===
dark_theme = gr.themes.Monochrome()

# === Launch Chat Interface ===
gr.ChatInterface(
    fn=chat,
    title="🛍️ AI Retail Advisor – Built with GPT-4o-mini, Gradio, and Python",
    description="Welcome! I'm your shopping assistant. Ask me about clothes, hats (60% off!), and other sale items.",
    theme=dark_theme,
    type="messages"
).launch()
