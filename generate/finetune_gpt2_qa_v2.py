
from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments, TextDataset, DataCollatorForLanguageModeling
import os

# Calea către dataset și modelul de bază
dataset_path = "qa_finetune_dataset_extended.txt"
model_name = "distilgpt2"
output_dir = "./distilgpt2-finetuned2"

# Încarcă tokenizer și modelul de bază
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

# Creează dataset
def load_dataset(file_path, tokenizer, block_size=128):
    return TextDataset(
        tokenizer=tokenizer,
        file_path=file_path,
        block_size=block_size
    )

train_dataset = load_dataset(dataset_path, tokenizer)

# Pregătește datele (cu mascarea limbajului)
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer, mlm=False,
)

# Setări de antrenare
training_args = TrainingArguments(
    output_dir=output_dir,
    overwrite_output_dir=True,
    num_train_epochs=4,
    per_device_train_batch_size=2,
    save_steps=500,
    save_total_limit=1,
    logging_steps=50,
    prediction_loss_only=True
)

# Trainer și pornirea antrenamentului
trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=train_dataset
)

trainer.train()
trainer.save_model(output_dir)
tokenizer.save_pretrained(output_dir)
