from flask import Flask, render_template, request
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
client = Anthropic()


@app.route("/", methods=["GET", "POST"])
def index():
    summary = None
    error = None
    original_text = ""

    length = "short"

    if request.method == "POST":
        original_text = request.form.get("text", "").strip()
        length = request.form.get("length", "short")
        if not original_text:
            error = "Please paste some text to summarize."
        else:
            if length == "very_short":
                prompt = f"Summarize the following text in 3 sentences or fewer:\n\n{original_text}"
            else:
                prompt = f"Summarize the following text concisely:\n\n{original_text}"
            try:
                message = client.messages.create(
                    model="claude-sonnet-4-6",
                    max_tokens=1024,
                    messages=[{"role": "user", "content": prompt}],
                )
                summary = message.content[0].text
            except Exception as e:
                error = f"API error: {e}"

    return render_template(
        "index.html",
        summary=summary,
        error=error,
        original_text=original_text,
        length=length,
    )


if __name__ == "__main__":
    app.run(debug=True)
