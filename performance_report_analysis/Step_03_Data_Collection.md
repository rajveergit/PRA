# Step 3 — Data Collection
## Phase: Data Collection
**Guideline:** Collect PDFs, policies, manuals, or datasets

---

## 3.1 Data Sources

### 3.1.1 Primary Document Types

| Document Type | Example Source | Format |
|---|---|---|
| Vehicle Owner Manuals | Maruti Suzuki, Tata Motors official websites | PDF |
| Engine Performance Reports | ARAI (Automotive Research Association of India) | PDF |
| NCAP Safety Test Reports | Global NCAP, Bharat NCAP | PDF |
| Emission Certification Data | CAFE norms, BS6 compliance sheets | PDF / CSV |
| Service Bulletins / TSBs | OEM dealer portals (public samples) | PDF |
| Dyno Test Reports | Open automotive research papers | PDF |
| OBD-II Fault Code Database | SAE J1979 public dataset | CSV / TXT |

### 3.1.2 Sample Dataset Folder Structure
```
data/
├── raw/
│   ├── maruti_swift_owner_manual_2023.pdf
│   ├── tata_nexon_performance_report.pdf
│   ├── ncap_safety_report_creta_2023.pdf
│   ├── bs6_emission_standards.pdf
│   ├── obd2_fault_codes.csv
│   └── engine_dyno_test_results.txt
```

---

## 3.2 Data Collection Strategy
1. **Manual Download** — Collect PDFs from official OEM websites and government portals
2. **Web Scraping** (where permitted) — Extract structured performance tables
3. **Public Research Databases** — IEEE, ResearchGate automotive papers
4. **Synthetic Data Generation** — Create sample performance reports to supplement real data for testing purposes

---

## 3.3 Data Volume

| Document Category | Count | Avg. Pages |
|---|---|---|
| Owner Manuals | 5 | 250 pages |
| Performance Reports | 8 | 30 pages |
| Safety Reports | 4 | 20 pages |
| Emission Data | 3 | 15 pages |
| OBD Fault Code DB | 1 | 500+ entries |

**Total estimated tokens after chunking:** ~2.5 million tokens

---

## 3.4 Useful Public Links for Data
- ARAI Reports: https://www.araiindia.com
- Global NCAP: https://www.globalncap.org
- Bharat NCAP: https://bharatncap.com
- OBD Codes Reference: https://www.obd-codes.com

---

## Checklist
- [ ] At least 5 documents collected across different categories
- [ ] Folder structure created (`data/raw/`)
- [ ] Data sources documented with links
- [ ] Document count and page estimates noted
- [ ] All files confirmed to be text-based PDFs (not scanned)
