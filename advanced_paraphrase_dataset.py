import json
import random
import itertools

def get_question_variations():
    """Mendapatkan berbagai variasi untuk pertanyaan"""
    return {
        # Kata tanya utama
        "Apa": ["Apakah", "Bagaimana", "Jelaskan", "Tolong jelaskan", "Bisakah dijelaskan", "Mohon penjelasan tentang"],
        "apa": ["apakah", "bagaimana", "jelaskan", "tolong jelaskan", "bisakah dijelaskan", "mohon penjelasan tentang"],
        "Sebutkan": ["Tuliskan", "Jelaskan", "Uraikan", "Sampaikan", "Paparkan", "Rincikan", "Daftarkan", "Cantumkan"],
        "sebutkan": ["tuliskan", "jelaskan", "uraikan", "sampaikan", "paparkan", "rincikan", "daftarkan", "cantumkan"],
        "Bagaimana": ["Seperti apa", "Gimana", "Apa saja", "Tolong jelaskan", "Mohon dijelaskan", "Bisakah diuraikan"],
        "bagaimana": ["seperti apa", "gimana", "apa saja", "tolong jelaskan", "mohon dijelaskan", "bisakah diuraikan"],
        "Dimana": ["Di mana", "Lokasi", "Tempat", "Posisi", "Letak", "Alamat"],
        "dimana": ["di mana", "lokasi", "tempat", "posisi", "letak", "alamat"],
        "Kapan": ["Pada saat", "Waktu", "Tanggal", "Periode", "Masa", "Saat"],
        "kapan": ["pada saat", "waktu", "tanggal", "periode", "masa", "saat"],
        "Siapa": ["Nama", "Sosok", "Figur", "Tokoh", "Orang", "Individu"],
        "siapa": ["nama", "sosok", "figur", "tokoh", "orang", "individu"],
        "Berapa": ["Jumlah", "Total", "Hitungan", "Banyaknya", "Kuantitas"],
        "berapa": ["jumlah", "total", "hitungan", "banyaknya", "kuantitas"],
        
        # Kata kunci UNNES
        "UNNES": ["Universitas Negeri Semarang", "UNNES", "Unnes", "kampus UNNES"],
        "Universitas Negeri Semarang": ["UNNES", "Unnes", "kampus UNNES", "Universitas Negeri Semarang"],
        "universitas": ["perguruan tinggi", "kampus", "institusi pendidikan", "lembaga pendidikan", "almamater"],
        "fakultas": ["fakultas", "jurusan", "bagian akademik", "unit akademik", "divisi akademik"],
        "program studi": ["jurusan", "prodi", "bidang studi", "program", "studi"],
        "mahasiswa": ["siswa", "peserta didik", "mahasiswa", "pelajar", "anak didik"],
        "dosen": ["pengajar", "tenaga pendidik", "akademisi", "pendidik", "guru besar"],
        "kampus": ["universitas", "area kampus", "lingkungan akademik", "kompleks pendidikan"]
    }

def get_answer_variations():
    """Mendapatkan berbagai variasi untuk jawaban"""
    return {
        # Kata hubung dan penjelasan
        "merupakan": ["adalah", "ialah", "yakni", "yaitu", "berupa", "termasuk"],
        "adalah": ["merupakan", "ialah", "yakni", "yaitu", "berupa", "termasuk"],
        "ialah": ["adalah", "merupakan", "yakni", "yaitu", "berupa"],
        "yakni": ["yaitu", "adalah", "ialah", "merupakan"],
        "yaitu": ["yakni", "adalah", "ialah", "merupakan"],
        
        # Kata kerja
        "bertugas": ["berfungsi", "berperan", "memiliki tugas", "bertanggung jawab", "mengemban tugas", "menjalankan fungsi"],
        "berfungsi": ["bertugas", "berperan", "memiliki fungsi", "menjalankan peran"],
        "berperan": ["berfungsi", "bertugas", "memiliki peran", "menjalankan peran"],
        "meliputi": ["terdiri dari", "mencakup", "termasuk", "antara lain", "berisi", "memuat"],
        "terdiri dari": ["meliputi", "mencakup", "berisi", "terbagi menjadi", "memuat"],
        "mencakup": ["meliputi", "terdiri dari", "termasuk", "berisi", "memuat"],
        "menyelenggarakan": ["melaksanakan", "mengadakan", "menjalankan", "menggelar", "menyelenggarakan"],
        "melaksanakan": ["menyelenggarakan", "mengadakan", "menjalankan", "menggelar", "melakukan"],
        "memberikan": ["menyediakan", "menawarkan", "menghadirkan", "menyajikan", "mengadakan"],
        "menyediakan": ["memberikan", "menawarkan", "menyajikan", "menghadirkan"],
        
        # Kata benda institusi
        "UNNES": ["Universitas Negeri Semarang", "UNNES", "Unnes"],
        "Universitas Negeri Semarang": ["UNNES", "Unnes"],
        "universitas": ["perguruan tinggi", "institusi pendidikan tinggi", "lembaga pendidikan tinggi"],
        "perguruan tinggi": ["universitas", "institusi pendidikan tinggi", "lembaga pendidikan"],
        "fakultas": ["fakultas", "unit akademik", "bagian akademik"],
        "program studi": ["jurusan", "prodi", "bidang studi", "program"],
        "mahasiswa": ["peserta didik", "siswa", "mahasiswa", "pelajar"],
        "pendidikan": ["edukasi", "pembelajaran", "pengajaran", "pendidikan"]
    }

def get_question_patterns():
    """Mendapatkan pola-pola pertanyaan yang berbeda"""
    return {
        "Apa itu": [
            "Jelaskan tentang", "Bagaimana definisi", "Apa yang dimaksud dengan", 
            "Tolong uraikan mengenai", "Bisakah dijelaskan tentang", "Mohon penjelasan mengenai",
            "Apa pengertian dari", "Bagaimana penjelasan", "Tolong jelaskan apa itu"
        ],
        "Apa saja": [
            "Sebutkan", "Tuliskan", "Jelaskan", "Uraikan", "Paparkan", 
            "Rincikan", "Daftarkan", "Cantumkan", "Sampaikan"
        ],
        "Dimana lokasi": [
            "Di mana letak", "Lokasi", "Tempat", "Posisi", "Alamat", 
            "Di mana posisi", "Letak", "Dimana tempat"
        ],
        "Bagaimana sejarah": [
            "Seperti apa riwayat", "Ceritakan sejarah", "Jelaskan latar belakang",
            "Uraikan sejarah", "Paparkan riwayat", "Sampaikan sejarah"
        ],
        "Siapa saja": [
            "Sebutkan nama-nama", "Tuliskan daftar", "Uraikan siapa", 
            "Daftarkan nama", "Cantumkan siapa"
        ],
        "Berapa jumlah": [
            "Seberapa banyak", "Jumlah total", "Hitungan", "Total", "Banyaknya"
        ]
    }

def get_sentence_starters():
    """Mendapatkan variasi awalan kalimat untuk jawaban"""
    return {
        "Universitas Negeri Semarang (UNNES)": [
            "UNNES atau Universitas Negeri Semarang",
            "Universitas Negeri Semarang yang dikenal sebagai UNNES",
            "UNNES (Universitas Negeri Semarang)",
            "Universitas Negeri Semarang atau UNNES",
            "UNNES, singkatan dari Universitas Negeri Semarang,"
        ],
        "UNNES": [
            "Universitas Negeri Semarang (UNNES)",
            "UNNES atau Universitas Negeri Semarang",
            "Universitas Negeri Semarang yang disingkat UNNES"
        ]
    }

def advanced_paraphrase_question(question, variation_count=1):
    """Membuat beberapa variasi parafrase untuk satu pertanyaan"""
    variations = []
    question_vars = get_question_variations()
    patterns = get_question_patterns()
    
    for i in range(variation_count):
        paraphrased = question
        
        # Ganti pola kalimat terlebih dahulu
        for pattern, alternatives in patterns.items():
            if pattern in paraphrased:
                paraphrased = paraphrased.replace(pattern, random.choice(alternatives))
        
        # Ganti kata-kata dengan sinonim
        words = paraphrased.split()
        for j, word in enumerate(words):
            clean_word = word.rstrip('?!.,;:')
            if clean_word in question_vars and random.random() > 0.3:  # 70% chance to replace
                punctuation = word[len(clean_word):]
                words[j] = random.choice(question_vars[clean_word]) + punctuation
        
        variations.append(' '.join(words))
    
    return variations

def advanced_paraphrase_answer(answer, variation_count=1):
    """Membuat beberapa variasi parafrase untuk satu jawaban"""
    variations = []
    answer_vars = get_answer_variations()
    starters = get_sentence_starters()
    
    for i in range(variation_count):
        paraphrased = answer
        
        # Ganti awalan kalimat
        for starter, alternatives in starters.items():
            if paraphrased.startswith(starter):
                paraphrased = paraphrased.replace(starter, random.choice(alternatives), 1)
        
        # Ganti kata-kata dengan sinonim
        words = paraphrased.split()
        for j, word in enumerate(words):
            clean_word = word.rstrip('.,;:!?')
            if clean_word in answer_vars and random.random() > 0.4:  # 60% chance to replace
                punctuation = word[len(clean_word):]
                words[j] = random.choice(answer_vars[clean_word]) + punctuation
        
        variations.append(' '.join(words))
    
    return variations

def create_advanced_paraphrased_dataset(variations_per_entry=5):
    """Membuat dataset dengan banyak variasi parafrase"""
    
    # Baca dataset asli
    with open('training_data_unnes_mistral_format.jsonl', 'r', encoding='utf-8') as f:
        original_data = [json.loads(line) for line in f]
    
    expanded_data = []
    
    # Proses setiap entri
    for entry in original_data:
        # Tambahkan data asli
        expanded_data.append(entry)
        
        original_question = entry['messages'][0]['content']
        original_answer = entry['messages'][1]['content']
        
        # Buat beberapa variasi parafrase
        question_variations = advanced_paraphrase_question(original_question, variations_per_entry)
        answer_variations = advanced_paraphrase_answer(original_answer, variations_per_entry)
        
        # Kombinasikan variasi pertanyaan dan jawaban
        for q_var, a_var in zip(question_variations, answer_variations):
            if q_var != original_question or a_var != original_answer:  # Hindari duplikasi
                paraphrased_entry = {
                    "messages": [
                        {
                            "role": "user",
                            "content": q_var
                        },
                        {
                            "role": "assistant",
                            "content": a_var
                        }
                    ]
                }
                expanded_data.append(paraphrased_entry)
    
    # Simpan dataset yang sudah diperbanyak
    with open('training_data_unnes_advanced_paraphrased.jsonl', 'w', encoding='utf-8') as f:
        for entry in expanded_data:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    
    # Simpan juga dalam format JSON array
    with open('training_data_unnes_advanced_paraphrased.json', 'w', encoding='utf-8') as f:
        json.dump(expanded_data, f, ensure_ascii=False, indent=2)
    
    print(f"Dataset berhasil diperbanyak dengan metode advanced!")
    print(f"Jumlah entri asli: {len(original_data)}")
    print(f"Jumlah entri setelah parafrase advanced: {len(expanded_data)}")
    print(f"Variasi per entri: {variations_per_entry}")
    print(f"Peningkatan: {((len(expanded_data) - len(original_data)) / len(original_data) * 100):.1f}%")
    print(f"File disimpan sebagai:")
    print(f"- training_data_unnes_advanced_paraphrased.jsonl")
    print(f"- training_data_unnes_advanced_paraphrased.json")
    
    # Tampilkan contoh variasi
    print("\n=== CONTOH VARIASI PARAFRASE ===")
    print("\nPertanyaan Asli:")
    print(f'"{original_data[0]["messages"][0]["content"]}"')
    
    # Tampilkan beberapa variasi pertanyaan
    sample_questions = advanced_paraphrase_question(original_data[0]["messages"][0]["content"], 3)
    for i, q in enumerate(sample_questions, 1):
        print(f"\nVariasi Pertanyaan {i}:")
        print(f'"{q}"')
    
    print("\nJawaban Asli:")
    print(f'"{original_data[0]["messages"][1]["content"][:100]}..."')
    
    # Tampilkan beberapa variasi jawaban
    sample_answers = advanced_paraphrase_answer(original_data[0]["messages"][1]["content"], 3)
    for i, a in enumerate(sample_answers, 1):
        print(f"\nVariasi Jawaban {i}:")
        print(f'"{a[:100]}..."')

if __name__ == "__main__":
    # Buat dataset dengan 5 variasi per entri (total ~570 entri)
    create_advanced_paraphrased_dataset(variations_per_entry=5)