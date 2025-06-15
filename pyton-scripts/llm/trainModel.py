import json
from pathlib import Path
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments, DataCollatorForLanguageModeling
from datasets import Dataset

# Încarcă datele din JSON
def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

# Pregătește dataset-ul pentru antrenare
def prepare_dataset(data, tokenizer):
    questions = [item["question"] for item in data]
    answers = [item["answer"] for item in data]
    texts = [q + " " + a for q, a in zip(questions, answers)]
    encodings = tokenizer(texts, truncation=True, padding="max_length", max_length=512)
    return Dataset.from_dict(encodings)

# Setează calea către fișierul JSON
json_path = Path("generated_qa.json")  # Modifică dacă fișierul e în altă locație
data = load_json(json_path)

# Încarcă modelul și tokenizer-ul
model_name = "distilgpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Setează un token de padding
tokenizer.pad_token = tokenizer.eos_token
model.resize_token_embeddings(len(tokenizer))

# Pregătește dataset-ul
train_dataset = prepare_dataset(data, tokenizer)

# Configurare Trainer
training_args = TrainingArguments(
    output_dir="./trained_model",
    evaluation_strategy="no",  # Elimină evaluarea
    save_strategy="epoch",
    per_device_train_batch_size=4,
    num_train_epochs=3,
    weight_decay=0.01,
    logging_dir="./logs",
    logging_steps=10,
    save_total_limit=2,
)

# Folosește un data collator pentru modelul de limbaj
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False  # Modelul GPT-2 nu folosește Masked Language Modeling
)

# Inițializează Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    data_collator=data_collator,
)

# Antrenează modelul
trainer.train()

# Salvează modelul și tokenizer-ul
model.save_pretrained("./trained_model")
tokenizer.save_pretrained("./trained_model")

print("Antrenare completă! Modelul a fost salvat în 'trained_model'.")

