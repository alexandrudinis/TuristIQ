
from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForCausalLM
from flask_cors import CORS
import torch

# Încarcă modelul și tokenizerul din directorul distilgpt2-finetuned2
model_path = "./distilgpt2-finetuned2"
model = AutoModelForCausalLM.from_pretrained(model_path, torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32)
tokenizer = AutoTokenizer.from_pretrained(model_path)
model.to("cuda" if torch.cuda.is_available() else "cpu")

# Creează aplicația Flask
app = Flask(__name__)
CORS(app)

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        message = data.get("question", "")

        # Tokenizare cu attention_mask
        inputs = tokenizer(message, return_tensors="pt", padding=True, truncation=True).to(model.device)
        outputs = model.generate(
            **inputs,
            max_new_tokens=100,
            do_sample=True,
            temperature=0.7,
            top_p=0.95
        )

        response_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

        return jsonify({"answer": response_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
