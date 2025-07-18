import json
import random

def paraphrase_question(question):
    """Parafrase pertanyaan dengan variasi kata dan struktur kalimat"""
    
    # Dictionary untuk sinonim dan variasi kata
    synonyms = {
        "Apa": ["Apakah", "Bagaimana", "Jelaskan"],
        "apa": ["apakah", "bagaimana", "jelaskan"],
        "Sebutkan": ["Tuliskan", "Jelaskan", "Uraikan", "Sampaikan"],
        "sebutkan": ["tuliskan", "jelaskan", "uraikan", "sampaikan"],
        "Bagaimana": ["Seperti apa", "Gimana", "Apa saja"],
        "bagaimana": ["seperti apa", "gimana", "apa saja"],
        "Dimana": ["Di mana", "Lokasi", "Tempat"],
        "dimana": ["di mana", "lokasi", "tempat"],
        "Kapan": ["Pada saat", "Waktu", "Tanggal"],
        "kapan": ["pada saat", "waktu", "tanggal"],
        "Siapa": ["Nama", "Sosok", "Figur"],
        "siapa": ["nama", "sosok", "figur"],
        "UNNES": ["Universitas Negeri Semarang", "UNNES"],
        "universitas": ["perguruan tinggi", "kampus", "institusi pendidikan"],
        "fakultas": ["fakultas", "jurusan", "bagian akademik"],
        "program studi": ["jurusan", "prodi", "bidang studi"],
        "mahasiswa": ["siswa", "peserta didik", "mahasiswa"],
        "dosen": ["pengajar", "tenaga pendidik", "akademisi"],
        "kampus": ["universitas", "area kampus", "lingkungan akademik"]
    }
    
    # Variasi struktur kalimat
    question_patterns = {
        "Apa itu": ["Jelaskan tentang", "Bagaimana definisi", "Apa yang dimaksud dengan", "Tolong uraikan mengenai"],
        "Apa saja": ["Sebutkan", "Tuliskan", "Jelaskan", "Uraikan"],
        "Dimana lokasi": ["Di mana letak", "Lokasi", "Tempat", "Posisi"],
        "Bagaimana sejarah": ["Seperti apa riwayat", "Ceritakan sejarah", "Jelaskan latar belakang"],
        "Siapa saja": ["Sebutkan nama-nama", "Tuliskan daftar", "Uraikan siapa"],
        "Berapa jumlah": ["Seberapa banyak", "Jumlah total", "Hitungan"]
    }
    
    paraphrased = question
    
    # Ganti pola kalimat terlebih dahulu
    for pattern, alternatives in question_patterns.items():
        if pattern in paraphrased:
            paraphrased = paraphrased.replace(pattern, random.choice(alternatives))
    
    # Ganti kata-kata dengan sinonim
    words = paraphrased.split()
    for i, word in enumerate(words):
        # Hapus tanda baca untuk pencocokan
        clean_word = word.rstrip('?!.,;:')
        if clean_word in synonyms:
            # Pertahankan tanda baca asli
            punctuation = word[len(clean_word):]
            words[i] = random.choice(synonyms[clean_word]) + punctuation
    
    return ' '.join(words)

def paraphrase_answer(answer):
    """Parafrase jawaban dengan variasi kata dan struktur"""
    
    # Dictionary untuk sinonim dalam jawaban
    answer_synonyms = {
        "merupakan": ["adalah", "ialah", "yakni", "yaitu"],
        "adalah": ["merupakan", "ialah", "yakni", "yaitu"],
        "bertugas": ["berfungsi", "berperan", "memiliki tugas", "bertanggung jawab"],
        "meliputi": ["terdiri dari", "mencakup", "termasuk", "antara lain"],
        "terdiri dari": ["meliputi", "mencakup", "berisi", "terbagi menjadi"],
        "bertanggung jawab": ["bertugas", "berperan", "memiliki kewajiban"],
        "menyelenggarakan": ["melaksanakan", "mengadakan", "menjalankan"],
        "melaksanakan": ["menyelenggarakan", "mengadakan", "menjalankan"],
        "memberikan": ["menyediakan", "menawarkan", "menghadirkan"],
        "menyediakan": ["memberikan", "menawarkan", "menyajikan"],
        "UNNES": ["Universitas Negeri Semarang", "UNNES"],
        "universitas": ["perguruan tinggi", "institusi pendidikan tinggi"],
        "fakultas": ["fakultas", "unit akademik"],
        "program studi": ["jurusan", "prodi", "bidang studi"],
        "mahasiswa": ["peserta didik", "siswa", "mahasiswa"],
        "pendidikan": ["edukasi", "pembelajaran", "pengajaran"]
    }
    
    # Variasi awalan kalimat
    sentence_starters = {
        "Universitas Negeri Semarang (UNNES)": [
            "UNNES atau Universitas Negeri Semarang",
            "Universitas Negeri Semarang yang dikenal sebagai UNNES",
            "UNNES (Universitas Negeri Semarang)"
        ]
    }
    
    paraphrased = answer
    
    # Ganti awalan kalimat
    for starter, alternatives in sentence_starters.items():
        if paraphrased.startswith(starter):
            paraphrased = paraphrased.replace(starter, random.choice(alternatives), 1)
    
    # Ganti kata-kata dengan sinonim
    words = paraphrased.split()
    for i, word in enumerate(words):
        # Hapus tanda baca untuk pencocokan
        clean_word = word.rstrip('.,;:!?')
        if clean_word in answer_synonyms:
            # Pertahankan tanda baca asli
            punctuation = word[len(clean_word):]
            words[i] = random.choice(answer_synonyms[clean_word]) + punctuation
    
    return ' '.join(words)

def create_paraphrased_dataset():
    """Membuat dataset yang sudah diparafrase"""
    
    # Baca dataset asli
    with open('training_data_unnes_mistral_format.jsonl', 'r', encoding='utf-8') as f:
        original_data = [json.loads(line) for line in f]
    
    paraphrased_data = []
    
    # Proses setiap entri
    for entry in original_data:
        # Tambahkan data asli
        paraphrased_data.append(entry)
        
        # Buat versi parafrase
        original_question = entry['messages'][0]['content']
        original_answer = entry['messages'][1]['content']
        
        paraphrased_question = paraphrase_question(original_question)
        paraphrased_answer = paraphrase_answer(original_answer)
        
        # Buat entri baru dengan parafrase
        paraphrased_entry = {
            "messages": [
                {
                    "role": "user",
                    "content": paraphrased_question
                },
                {
                    "role": "assistant",
                    "content": paraphrased_answer
                }
            ]
        }
        
        paraphrased_data.append(paraphrased_entry)
    
    # Simpan dataset yang sudah diperbanyak
    with open('training_data_unnes_paraphrased.jsonl', 'w', encoding='utf-8') as f:
        for entry in paraphrased_data:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    
    # Simpan juga dalam format JSON array
    with open('training_data_unnes_paraphrased.json', 'w', encoding='utf-8') as f:
        json.dump(paraphrased_data, f, ensure_ascii=False, indent=2)
    
    print(f"Dataset berhasil diperbanyak!")
    print(f"Jumlah entri asli: {len(original_data)}")
    print(f"Jumlah entri setelah parafrase: {len(paraphrased_data)}")
    print(f"File disimpan sebagai:")
    print(f"- training_data_unnes_paraphrased.jsonl")
    print(f"- training_data_unnes_paraphrased.json")
    
    # Tampilkan contoh parafrase
    print("\n=== CONTOH PARAFRASE ===")
    print("\nPertanyaan Asli:")
    print(f'"{original_data[0]["messages"][0]["content"]}"')
    print("\nPertanyaan Parafrase:")
    print(f'"{paraphrased_data[1]["messages"][0]["content"]}"')
    print("\nJawaban Asli:")
    print(f'"{original_data[0]["messages"][1]["content"][:100]}..."')
    print("\nJawaban Parafrase:")
    print(f'"{paraphrased_data[1]["messages"][1]["content"][:100]}..."')

if __name__ == "__main__":
    create_paraphrased_dataset()