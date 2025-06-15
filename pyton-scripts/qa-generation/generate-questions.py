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
        
        qa_pairs.append({"question": f"Ce îmi poți spune despre {name}?", "answer": obj["description"]})
        qa_pairs.append({"question": f"Unde se află {name}?", "answer": f"{name} se află în {city}, județul {county}."})
        qa_pairs.append({"question": f"În ce localitate se află {name}?", "answer": f"{name} este situat în {city}."})
        qa_pairs.append({"question": f"Ce categorie de obiectiv turistic este {name}?", "answer": f"{name} este un obiectiv turistic de tip {category}."})
        qa_pairs.append({"question": f"Ce pot vizita în {city}?", "answer": f"În {city}, poți vizita obiective precum {', '.join(set(obj['name'] for obj in data['turistic_objects'] if obj['location']['city'] == city))}."})
        qa_pairs.append({"question": f"Care sunt atracțiile principale din {city}?", "answer": f"Atractiile principale din {city} includ {', '.join(set(obj['name'] for obj in data['turistic_objects'] if obj['location']['city'] == city))}."})

        for activity in activities:
            qa_pairs.append({"question": f"Pot să fac {activity} la {name}?", "answer": f"Da, {name} este potrivit pentru {activity}."})
            qa_pairs.append({"question": f"Este {name} potrivit pentru {activity}?", "answer": f"Da, {name} oferă oportunități pentru {activity}."})
            qa_pairs.append({"question": f"Ce locuri din {city} sunt bune pentru {activity}?", "answer": f"{name} este un loc recomandat pentru {activity} în {city}."})
            qa_pairs.append({"question": f"Unde pot merge în {county} pentru {activity}?", "answer": f"În județul {county}, poți încerca {name} pentru {activity}."})
            qa_pairs.append({"question": f"Vreau să fac {activity} în {city}.", "answer": f"Dacă vrei să faci {activity} în {city}, poți vizita {name}."})
            qa_pairs.append({"question": f"Vreau să fac {activity} în {county}.", "answer": f"În județul {county}, {name} este un loc bun pentru {activity}."})

        for rel in relevant_for:
            qa_pairs.append({"question": f"Este {name} recomandat pentru {rel}?", "answer": f"Da, {name} este recomandat pentru {rel}."})
            qa_pairs.append({"question": f"Ce locuri din {county} sunt bune pentru {rel}?", "answer": f"{name} este un loc excelent pentru {rel} în județul {county}."})

        for accom in accommodation:
            qa_pairs.append({"question": f"Unde mă pot caza dacă vizitez {name}?", "answer": f"Poți să te cazezi la {accom}, aproape de {name}."})
            qa_pairs.append({"question": f"Este {accom} aproape de {name}?", "answer": f"Da, {accom} este situat în apropierea {name}."})
            qa_pairs.append({"question": f"Ce opțiuni de cazare sunt disponibile lângă {name}?", "answer": f"Opțiunile de cazare lângă {name} includ {', '.join(accommodation)}."})
            qa_pairs.append({"question": f"Unde mă pot caza în {city}?", "answer": f"În {city}, poți găsi cazare la {', '.join(set(accommodation))}."})

        for attraction in nearby_attractions:
            qa_pairs.append({"question": f"Ce alte obiective turistice sunt aproape de {name}?", "answer": f"Obiectivele turistice din apropierea {name} includ {', '.join(nearby_attractions)}."})
            qa_pairs.append({"question": f"Merită să vizitez {attraction} dacă sunt la {name}?", "answer": f"Da, {attraction} este o atracție recomandată în apropierea {name}."})

    for activity in set(itertools.chain.from_iterable([obj.get("activities", []) + obj.get("relevant_for", []) for obj in data["turistic_objects"]])):
        qa_pairs.append({"question": f"Ce pot vizita în {county} dacă mă interesează {activity}?", "answer": f"În județul {county}, poți vizita {', '.join([obj['name'] for obj in data['turistic_objects'] if activity in obj.get('activities', [])])} pentru {activity}."})
    
    return qa_pairs

def main():
    script_dir = Path(__file__).parent
    file_path = script_dir / "obiective-turistice-alba.json"
    data = load_json(file_path)
    qa_pairs = generate_questions_and_answers(data)
    
    output_file = script_dir / "generated_qa.json"
    with output_file.open("w", encoding="utf-8") as out_file:
        json.dump(qa_pairs, out_file, indent=4, ensure_ascii=False)
    
    print(f"Generat {len(qa_pairs)} perechi de întrebări și răspunsuri pentru antrenament în JSON.")

if __name__ == "__main__":
    main()
