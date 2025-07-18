import json
import random
from typing import List, Dict

def create_question_variations(original_question: str) -> List[str]:
    """Membuat berbagai variasi pertanyaan dengan teknik parafrase yang beragam"""
    variations = []
    
    # Variasi 1: Menggunakan kata tanya yang berbeda
    question_starters = [
        "Apa", "Bagaimana", "Jelaskan", "Tolong jelaskan", "Bisakah dijelaskan",
        "Mohon penjelasan", "Uraikan", "Ceritakan", "Paparkan", "Deskripsikan",
        "Sebutkan", "Terangkan", "Gambarkan", "Berikan penjelasan", "Sampaikan"
    ]
    
    # Variasi 2: Sinonim kata kunci
    synonyms = {
        "UNNES": ["UNNES", "Universitas Negeri Semarang", "Unnes", "kampus UNNES"],
        "universitas": ["universitas", "perguruan tinggi", "institusi pendidikan", "lembaga pendidikan", "kampus", "almamater"],
        "lokasi": ["lokasi", "tempat", "posisi", "letak", "area", "wilayah"],
        "sejarah": ["sejarah", "riwayat", "kisah", "asal-usul", "latar belakang"],
        "fakultas": ["fakultas", "bagian akademik", "unit akademik", "divisi akademik"]
    }
    
    # Variasi 3: Struktur kalimat yang berbeda
    sentence_patterns = [
        "{starter} {content}?",
        "{starter} mengenai {content}?",
        "{starter} tentang {content}?",
        "Mohon {starter_lower} {content}?",
        "Tolong {starter_lower} {content}?",
        "Bisakah {starter_lower} {content}?",
        "Dapatkah {starter_lower} {content}?"
    ]
    
    # Generate variasi berdasarkan pola yang ada
    base_content = original_question.lower()
    
    for i in range(10):  # Membuat 10 variasi per pertanyaan
        # Pilih starter acak
        starter = random.choice(question_starters)
        
        # Modifikasi konten dengan sinonim
        modified_content = original_question
        for key, synonym_list in synonyms.items():
            if key.lower() in modified_content.lower():
                modified_content = modified_content.replace(key, random.choice(synonym_list))
        
        # Hapus kata tanya dari awal jika ada
        content_words = modified_content.split()[1:] if modified_content.split() else []
        content = " ".join(content_words)
        
        # Pilih pola kalimat acak
        pattern = random.choice(sentence_patterns)
        
        if "{starter_lower}" in pattern:
            variation = pattern.format(starter_lower=starter.lower(), content=content)
        else:
            variation = pattern.format(starter=starter, content=content)
        
        # Bersihkan dan tambahkan ke variasi
        variation = variation.strip().replace("  ", " ")
        if variation not in variations and variation != original_question:
            variations.append(variation)
    
    return variations[:8]  # Ambil maksimal 8 variasi

def create_answer_variations(original_answer: str) -> List[str]:
    """Membuat berbagai variasi jawaban dengan teknik parafrase yang beragam"""
    variations = []
    
    # Sinonim untuk kata-kata umum dalam jawaban
    answer_synonyms = {
        "UNNES": ["UNNES", "Universitas Negeri Semarang", "Unnes"],
        "universitas": ["universitas", "perguruan tinggi", "institusi pendidikan", "lembaga pendidikan"],
        "terletak": ["terletak", "berada", "berlokasi", "berposisi"],
        "dipimpin": ["dipimpin", "dikepalai", "dibawahi", "dikomandoi"],
        "merupakan": ["merupakan", "adalah", "ialah", "yakni", "yaitu"],
        "dimulai": ["dimulai", "berawal", "bermula", "diawali"],
        "berdasarkan": ["berdasarkan", "sesuai", "mengacu pada", "berpedoman pada"]
    }
    
    # Variasi awalan kalimat
    sentence_starters = [
        "",  # Tanpa awalan
        "Berdasarkan informasi, ",
        "Dapat dijelaskan bahwa ",
        "Perlu diketahui bahwa ",
        "Faktanya, "
    ]
    
    for i in range(8):  # Membuat 8 variasi per jawaban
        modified_answer = original_answer
        
        # Ganti kata dengan sinonim secara acak
        for word, synonym_list in answer_synonyms.items():
            if word in modified_answer:
                modified_answer = modified_answer.replace(word, random.choice(synonym_list))
        
        # Tambah awalan kalimat secara acak
        starter = random.choice(sentence_starters)
        if starter:
            modified_answer = starter + modified_answer.lower()
            # Kapitalisasi huruf pertama setelah awalan
            modified_answer = modified_answer[0].upper() + modified_answer[1:]
        
        # Variasi struktur kalimat sederhana
        if i % 3 == 0 and "yang" in modified_answer:
            modified_answer = modified_answer.replace(" yang ", " yang mana ")
        elif i % 3 == 1 and "dan" in modified_answer:
            modified_answer = modified_answer.replace(" dan ", " serta ")
        
        if modified_answer not in variations and modified_answer != original_answer:
            variations.append(modified_answer)
    
    return variations

def mega_paraphrase_dataset(input_file: str, output_file: str):
    """Membuat dataset dengan parafrase yang sangat banyak"""
    
    # Baca dataset asli
    with open(input_file, 'r', encoding='utf-8') as f:
        original_data = [json.loads(line) for line in f]
    
    mega_dataset = []
    
    print(f"Memproses {len(original_data)} entri asli...")
    
    for idx, entry in enumerate(original_data):
        original_question = entry['messages'][0]['content']
        original_answer = entry['messages'][1]['content']
        
        # Tambahkan data asli
        mega_dataset.append(entry)
        
        # Buat variasi pertanyaan
        question_variations = create_question_variations(original_question)
        
        # Buat variasi jawaban
        answer_variations = create_answer_variations(original_answer)
        
        # Kombinasi variasi pertanyaan dengan jawaban asli
        for q_var in question_variations:
            new_entry = {
                "messages": [
                    {"role": "user", "content": q_var},
                    {"role": "assistant", "content": original_answer}
                ]
            }
            mega_dataset.append(new_entry)
        
        # Kombinasi pertanyaan asli dengan variasi jawaban
        for a_var in answer_variations:
            new_entry = {
                "messages": [
                    {"role": "user", "content": original_question},
                    {"role": "assistant", "content": a_var}
                ]
            }
            mega_dataset.append(new_entry)
        
        # Kombinasi variasi pertanyaan dengan variasi jawaban (sampel)
        for i in range(min(5, len(question_variations), len(answer_variations))):
            if i < len(question_variations) and i < len(answer_variations):
                new_entry = {
                    "messages": [
                        {"role": "user", "content": question_variations[i]},
                        {"role": "assistant", "content": answer_variations[i]}
                    ]
                }
                mega_dataset.append(new_entry)
        
        if (idx + 1) % 10 == 0:
            print(f"Diproses: {idx + 1}/{len(original_data)} entri")
    
    # Hapus duplikasi
    unique_dataset = []
    seen_combinations = set()
    
    for entry in mega_dataset:
        combination = (entry['messages'][0]['content'], entry['messages'][1]['content'])
        if combination not in seen_combinations:
            unique_dataset.append(entry)
            seen_combinations.add(combination)
    
    # Simpan ke file JSONL
    with open(output_file, 'w', encoding='utf-8') as f:
        for entry in unique_dataset:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    
    # Simpan juga ke file JSON untuk referensi
    json_output_file = output_file.replace('.jsonl', '.json')
    with open(json_output_file, 'w', encoding='utf-8') as f:
        json.dump(unique_dataset, f, ensure_ascii=False, indent=2)
    
    print(f"\n=== HASIL MEGA PARAFRASE ===")
    print(f"Dataset asli: {len(original_data)} entri")
    print(f"Dataset setelah mega parafrase: {len(unique_dataset)} entri")
    print(f"Peningkatan: {len(unique_dataset) - len(original_data)} entri baru")
    print(f"Rasio peningkatan: {len(unique_dataset) / len(original_data):.1f}x")
    print(f"\nFile output:")
    print(f"- JSONL: {output_file}")
    print(f"- JSON: {json_output_file}")
    
    # Tampilkan contoh hasil
    print(f"\n=== CONTOH HASIL MEGA PARAFRASE ===")
    if len(unique_dataset) > 0:
        sample = unique_dataset[0]
        print(f"Pertanyaan: {sample['messages'][0]['content']}")
        print(f"Jawaban: {sample['messages'][1]['content'][:100]}...")
    
    return len(unique_dataset)

if __name__ == "__main__":
    input_file = "training_data_unnes_mistral_format.jsonl"
    output_file = "training_data_unnes_mega_paraphrased.jsonl"
    
    total_entries = mega_paraphrase_dataset(input_file, output_file)
    print(f"\nMega parafrase selesai! Total entri: {total_entries}")