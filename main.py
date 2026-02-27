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

    if request.method == "POST":
        original_text = request.form.get("text", "").strip()
        if not original_text:
            error = "Please paste some text to summarize."
        else:
            try:
                message = client.messages.create(
                    model="claude-sonnet-4-6",
                    max_tokens=1024,
                    messages=[
                        {
                            "role": "user",
                            "content": f"Summarize the following text concisely:\n\n{original_text}",
                        }
                    ],
                )
                summary = message.content[0].text
            except Exception as e:
                error = f"API error: {e}"

    return render_template(
        "index.html",
        summary=summary,
        error=error,
        original_text=original_text,
    )


if __name__ == "__main__":
    app.run(debug=True)
