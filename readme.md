=======================
SUBMISSION ETL PIPELINE
=======================

👤 Nama: Ikirahman
📂 Proyek: ETL Pipeline Pengajuan Barang OPD

========================
1. CARA JALANKAN PIPELINE
========================

1. Buka terminal / command prompt.
2. Aktifkan virtual environment (jika menggunakan).
3. Jalankan perintah berikut:
   
   ```bash
   python main.py
   ```

4. Pipeline akan menjalankan proses berikut:
   - Extract data dari sumber
   - Transformasi data
   - Load data ke:
     - File CSV (output.csv)
     - Google Sheets
     - PostgreSQL database

========================
2. CARA JALANKAN UNIT TEST
========================

1. Jalankan perintah:
   
   ```bash
   pytest tests/
   ```

2. Ini akan menjalankan semua unit test dari:
   - test_extract.py
   - test_transform.py
   - test_load.py

========================
3. CARA JALANKAN TEST COVERAGE
========================

1. Install plugin coverage:
   
   ```bash
   pip install coverage
   ```

2. Jalankan coverage untuk semua test:
   
   ```bash
   coverage run -m pytest tests/
   coverage report -m
   ```

3. Untuk lihat HTML report:
   
   ```bash
   coverage html
   ```

   Buka file `htmlcov/index.html` di browser untuk melihat hasil visual.

========================
4. URL GOOGLE SHEETS
========================

🔗 Spreadsheet Public:
https://docs.google.com/spreadsheets/d/1uVHGPZVP8YTV7o6msLMliSqWz3_DhswVrWxqiTovRc0/edit?usp=sharing

(Catatan: Pastikan sudah diatur ke "Anyone with the link can view")

========================
5. STRUKTUR FOLDER SUBMISSION
========================
```
├── README.md
├── google-sheets-api.json
├── main.py
├── product.csv
├── requirements.txt
├── submission.txt
├── readme.md
├── test
│   ├── test_extract.py
│   ├── test_load.py
│   └── test_transform.py
└── utils
    ├── __pycache__
    │   ├── extract.cpython-312.pyc
    │   ├── load.cpython-312.pyc
    │   └── transform.cpython-312.pyc
    ├── extract.py
    ├── load.py
    └── transform.py
```
========================
6. KETERANGAN TAMBAHAN
========================

- Script ini menggunakan modul modular (extract, transform, load) sesuai dengan prinsip ETL.
- Telah diuji dengan unit test.
- Telah memiliki test coverage untuk setiap modul.
