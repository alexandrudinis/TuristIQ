
from transformers import GPT2LMHeadModel, GPT2Tokenizer, Trainer, TrainingArguments
from datasets import load_dataset
import torch

# Verifică dacă avem un GPU disponibil
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# Încarcă tokenizerul și modelul
model_name = "distilgpt2"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token
model = GPT2LMHeadModel.from_pretrained(model_name)
model.to(device)

# Încarcă datasetul
data_path = "qa_finetune_dataset.txt"  # asigură-te că e în același folder cu scriptul
dataset = load_dataset("text", data_files={"train": data_path})

# Tokenizare cu labels = input_ids
def tokenize_function(example):
    tokens = tokenizer(example["text"], truncation=True, padding="max_length", max_length=256)
    tokens["labels"] = tokens["input_ids"].copy()
    return tokens

tokenized_datasets = dataset.map(tokenize_function, batched=True)

# Setări de antrenare
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="no",
    per_device_train_batch_size=2,
    num_train_epochs=3,
    save_total_limit=1,
    logging_dir="./logs",
    logging_steps=50,
    save_steps=500,
    push_to_hub=False,
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
)

# Antrenare
trainer.train()

# Salvare model și tokenizer
trainer.save_model("./distilgpt2-finetuned")
tokenizer.save_pretrained("./distilgpt2-finetuned")

print("Modelul antrenat a fost salvat în folderul ./distilgpt2-finetuned")
