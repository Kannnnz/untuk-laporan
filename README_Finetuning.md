# Fine-tuning Mistral-7B untuk Dataset UNNES

Repository ini berisi kode untuk melakukan fine-tuning model Mistral-7B-Instruct-v0.2 menggunakan dataset UNNES dengan library Unsloth, yang dioptimalkan untuk Google Colab T4 GPU.

## 📁 File yang Disediakan

- `Tes_Finetuning_Mistral_Unnes_1.ipynb` - Notebook Jupyter untuk fine-tuning
- `Modelfile` - Konfigurasi untuk Ollama
- `training_data_unnes.jsonl` - Dataset training dalam format JSONL
- `training_data_unnes.json` - Dataset training dalam format JSON

## 🚀 Cara Menggunakan

### 1. Persiapan Google Colab

1. Buka Google Colab (https://colab.research.google.com/)
2. Upload notebook `Tes_Finetuning_Mistral_Unnes_1.ipynb`
3. Upload file dataset `training_data_unnes.jsonl` ke Colab
4. Pastikan menggunakan GPU T4:
   - Runtime → Change runtime type → Hardware accelerator: GPU → GPU type: T4

### 2. Menjalankan Fine-tuning

1. Jalankan semua cell secara berurutan
2. Proses akan memakan waktu sekitar 30-60 menit tergantung ukuran dataset
3. Model akan disimpan dalam format GGUF yang kompatibel dengan Ollama

### 3. Menggunakan Model dengan Ollama

Setelah fine-tuning selesai:

1. **Download file model:**
   ```bash
   # Download file mistral-unnes-Q4_K_M.gguf dari Colab
   ```

2. **Buat model di Ollama:**
   ```bash
   # Pastikan file Modelfile dan mistral-unnes-Q4_K_M.gguf berada di direktori yang sama
   ollama create mistral-unnes -f Modelfile
   ```

3. **Test model:**
   ```bash
   ollama run mistral-unnes
   ```

4. **Contoh penggunaan:**
   ```
   >>> Apa itu Universitas Negeri Semarang?
   >>> Siapa rektor UNNES saat ini?
   >>> Sebutkan fakultas yang ada di UNNES!
   ```

## ⚙️ Konfigurasi Teknis

### Memory Optimization untuk T4 GPU

- **4-bit quantization** untuk mengurangi penggunaan VRAM
- **LoRA (Low-Rank Adaptation)** dengan rank 16
- **Gradient checkpointing** untuk memory efficiency
- **Batch size 1** dengan gradient accumulation 4
- **Mixed precision training** (FP16/BF16)

### Training Parameters

- **Learning rate:** 2e-4
- **Epochs:** 3
- **Max sequence length:** 2048
- **LoRA rank:** 16
- **LoRA alpha:** 16
- **Dropout:** 0.05

## 📊 Dataset

Dataset berisi 95 pasangan pertanyaan-jawaban tentang UNNES meliputi:

- Informasi umum universitas
- Sejarah dan perkembangan
- Struktur organisasi
- Fakultas dan program studi
- Visi, misi, dan tujuan
- Prestasi dan pencapaian

Format dataset:
```json
{
  "instruction": "Pertanyaan tentang UNNES",
  "input": "",
  "output": "Jawaban yang akurat dan informatif"
}
```

## 🔧 Troubleshooting

### Jika mengalami Out of Memory (OOM):

1. **Kurangi batch size:**
   ```python
   per_device_train_batch_size=1  # Sudah minimal
   ```

2. **Kurangi sequence length:**
   ```python
   max_seq_length = 1024  # Dari 2048
   ```

3. **Kurangi LoRA rank:**
   ```python
   r=8  # Dari 16
   ```

### Jika training terlalu lambat:

1. **Kurangi jumlah epochs:**
   ```python
   num_train_epochs=2  # Dari 3
   ```

2. **Gunakan subset dataset:**
   ```python
   dataset = dataset.select(range(50))  # Gunakan 50 data pertama
   ```

## 📈 Monitoring Training

Notebook akan menampilkan:
- Progress training per step
- Loss value
- Memory usage
- Sample output setelah training

## 🎯 Tips untuk Hasil Optimal

1. **Kualitas Dataset:** Pastikan data training berkualitas dan konsisten
2. **Hyperparameter Tuning:** Eksperimen dengan learning rate dan LoRA rank
3. **Validation:** Test model dengan pertanyaan yang tidak ada di dataset training
4. **Iterative Improvement:** Tambahkan data training berdasarkan performa model

## 📝 Catatan Penting

- Model ini dioptimalkan khusus untuk pertanyaan tentang UNNES
- Untuk pertanyaan umum di luar UNNES, model mungkin kurang akurat
- Selalu test model sebelum deployment ke production
- Backup model original sebelum fine-tuning

## 🤝 Kontribusi

Untuk meningkatkan model:
1. Tambahkan data training yang lebih beragam
2. Eksperimen dengan hyperparameter berbeda
3. Test dengan berbagai jenis pertanyaan
4. Dokumentasikan hasil eksperimen

## 📞 Support

Jika mengalami masalah:
1. Periksa log error di Colab
2. Pastikan semua dependencies terinstall
3. Cek penggunaan memory GPU
4. Restart runtime jika diperlukan

---

**Selamat mencoba fine-tuning! 🚀**