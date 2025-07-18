import json
import os

def convert_to_mistral_format(input_file, output_file):
    """
    Mengkonversi format dataset dari instruction-input-output ke format Mistral 7B
    
    Args:
        input_file (str): Path ke file JSONL input
        output_file (str): Path ke file JSONL output
    """
    converted_data = []
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                    
                try:
                    # Parse JSON dari setiap baris
                    data = json.loads(line)
                    
                    # Ekstrak instruction dan output
                    instruction = data.get('instruction', '')
                    output = data.get('output', '')
                    
                    # Skip jika instruction atau output kosong
                    if not instruction or not output:
                        print(f"Warning: Baris {line_num} memiliki instruction atau output kosong, dilewati.")
                        continue
                    
                    # Konversi ke format Mistral
                    mistral_format = {
                        "messages": [
                            {
                                "role": "user",
                                "content": instruction
                            },
                            {
                                "role": "assistant", 
                                "content": output
                            }
                        ]
                    }
                    
                    converted_data.append(mistral_format)
                    
                except json.JSONDecodeError as e:
                    print(f"Error parsing JSON pada baris {line_num}: {e}")
                    continue
        
        # Tulis hasil konversi ke file output
        with open(output_file, 'w', encoding='utf-8') as f:
            for item in converted_data:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')
        
        print(f"Konversi berhasil!")
        print(f"File input: {input_file}")
        print(f"File output: {output_file}")
        print(f"Total data yang dikonversi: {len(converted_data)} entri")
        
        # Tampilkan contoh hasil konversi
        if converted_data:
            print("\nContoh hasil konversi:")
            print(json.dumps(converted_data[0], indent=2, ensure_ascii=False))
            
    except FileNotFoundError:
        print(f"Error: File {input_file} tidak ditemukan.")
    except Exception as e:
        print(f"Error: {e}")

def main():
    # Path file input dan output
    input_file = "training_data_unnes.jsonl"
    output_file = "training_data_unnes_mistral_format.jsonl"
    
    # Pastikan file input ada
    if not os.path.exists(input_file):
        print(f"File {input_file} tidak ditemukan di direktori saat ini.")
        return
    
    # Jalankan konversi
    convert_to_mistral_format(input_file, output_file)
    
    # Buat juga versi JSON (bukan JSONL) jika diperlukan
    json_output_file = "training_data_unnes_mistral_format.json"
    
    try:
        # Baca file JSONL yang baru dibuat
        with open(output_file, 'r', encoding='utf-8') as f:
            all_data = []
            for line in f:
                if line.strip():
                    all_data.append(json.loads(line))
        
        # Tulis sebagai array JSON
        with open(json_output_file, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, indent=2, ensure_ascii=False)
        
        print(f"\nFile JSON array juga dibuat: {json_output_file}")
        
    except Exception as e:
        print(f"Error membuat file JSON: {e}")

if __name__ == "__main__":
    main()