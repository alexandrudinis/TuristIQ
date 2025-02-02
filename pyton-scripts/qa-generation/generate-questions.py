import json
import itertools
from pathlib import Path

def load_json(file_path):
    with file_path.open("r", encoding="utf-8") as file:
        return json.load(file)

def generate_questions_and_answers(data):
    qa_pairs = []
    county = data["judet"]
    
    for obj in data.get("turistic_objects", []):
        name = obj["name"]
        city = obj["location"]["city"]
        category = obj["category"]
        activities = obj.get("activities", [])
        relevant_for = obj.get("relevant_for", [])
        accommodation = obj.get("accommodation", [])
        nearby_attractions = obj.get("nearby_attractions", [])
        
        # Întrebări generale despre obiectiv
        qa_pairs.append((f"Ce îmi poți spune despre {name}?", obj["description"]))
        qa_pairs.append((f"Unde se află {name}?", f"{name} se află în {city}, județul {county}."))
        qa_pairs.append((f"În ce localitate se află {name}?", f"{name} este situat în {city}."))
        qa_pairs.append((f"Ce categorie de obiectiv turistic este {name}?", f"{name} este un obiectiv turistic de tip {category}."))
        qa_pairs.append((f"Ce pot vizita în {city}?", f"În {city}, poți vizita obiective precum {', '.join(set(obj['name'] for obj in data['turistic_objects'] if obj['location']['city'] == city))}."))
        qa_pairs.append((f"Care sunt atracțiile principale din {city}?", f"Atractiile principale din {city} includ {', '.join(set(obj['name'] for obj in data['turistic_objects'] if obj['location']['city'] == city))}."))

        # Întrebări despre activități
        for activity in activities:
            qa_pairs.append((f"Pot să fac {activity} la {name}?", f"Da, {name} este potrivit pentru {activity}."))
            qa_pairs.append((f"Este {name} potrivit pentru {activity}?", f"Da, {name} oferă oportunități pentru {activity}."))
            qa_pairs.append((f"Ce locuri din {city} sunt bune pentru {activity}?", f"{name} este un loc recomandat pentru {activity} în {city}."))
            qa_pairs.append((f"Unde pot merge în {county} pentru {activity}?", f"În județul {county}, poți încerca {name} pentru {activity}."))
            qa_pairs.append((f"Vreau să fac {activity} în {city}.", f"Dacă vrei să faci {activity} în {city}, poți vizita {name}."))
            qa_pairs.append((f"Vreau să fac {activity} în {county}.", f"În județul {county}, {name} este un loc bun pentru {activity}."))

        # Întrebări despre relevanță
        for rel in relevant_for:
            qa_pairs.append((f"Este {name} recomandat pentru {rel}?", f"Da, {name} este recomandat pentru {rel}."))
            qa_pairs.append((f"Ce locuri din {county} sunt bune pentru {rel}?", f"{name} este un loc excelent pentru {rel} în județul {county}."))

        # Întrebări despre cazare
        for accom in accommodation:
            qa_pairs.append((f"Unde mă pot caza dacă vizitez {name}?", f"Poți să te cazezi la {accom}, aproape de {name}."))
            qa_pairs.append((f"Este {accom} aproape de {name}?", f"Da, {accom} este situat în apropierea {name}."))
            qa_pairs.append((f"Ce opțiuni de cazare sunt disponibile lângă {name}?", f"Opțiunile de cazare lângă {name} includ {', '.join(accommodation)}."))
            qa_pairs.append((f"Unde mă pot caza în {city}?", f"În {city}, poți găsi cazare la {', '.join(set(accommodation))}."))

        # Întrebări despre atracții din apropiere
        for attraction in nearby_attractions:
            qa_pairs.append((f"Ce alte obiective turistice sunt aproape de {name}?", f"Obiectivele turistice din apropierea {name} includ {', '.join(nearby_attractions)}."))
            qa_pairs.append((f"Merită să vizitez {attraction} dacă sunt la {name}?", f"Da, {attraction} este o atracție recomandată în apropierea {name}."))

    # Întrebări generale despre județ și activități
    for activity in set(itertools.chain.from_iterable([obj.get("activities", []) + obj.get("relevant_for", []) for obj in data["turistic_objects"]])):
        qa_pairs.append((f"Ce pot vizita în {county} dacă mă interesează {activity}?", f"În județul {county}, poți vizita {', '.join([obj['name'] for obj in data['turistic_objects'] if activity in obj.get('activities', [])])} pentru {activity}."))

    return qa_pairs

def main():
    script_dir = Path(__file__).parent  # Obține directorul scriptului
    file_path = script_dir / "obiective-turistice-alba.json"  # Construiește calea absolută
    data = load_json(file_path)
    qa_pairs = generate_questions_and_answers(data)
    
    output_file = script_dir / "generated_qa.txt"  # Fișierul de output
    with output_file.open("w", encoding="utf-8") as out_file:
        for question, answer in qa_pairs:
            out_file.write(f"Q: {question}\nA: {answer}\n\n")
    
    print(f"Generat {len(qa_pairs)} perechi de întrebări și răspunsuri pentru antrenament.")

if __name__ == "__main__":
    main()
