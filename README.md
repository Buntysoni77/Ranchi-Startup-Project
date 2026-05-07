<img width="1895" height="886" alt="Screenshot 2026-05-07 161255" src="https://github.com/user-attachments/assets/0d1b1a7b-9d2a-4c01-ba22-731afa1c4eb6" />
<img width="1901" height="892" alt="Screenshot 2026-05-07 161233" src="https://github.com/user-attachments/assets/7877ee64-0160-46ed-b50c-8b470db11238" />
<img width="1510" height="892" alt="Screenshot 2026-05-07 161324" src="https://github.com/user-attachments/assets/e816b5af-f3db-4cb0-ab8b-5773400c53eb" />
<img width="1900" height="881" alt="Screenshot 2026-05-07 161206" src="https://github.com/user-attachments/assets/0017f9e3-c347-4f8c-a212-60a41805a30e" />
# 🏆 Jharkhand Scout — Business Intelligence Dashboard

> A data-driven startup recommendation engine for Jharkhand districts and localities, powered by India Census 2011 data.

![Dashboard](https://images.unsplash.com/photo-1497366216548-37526070297c?q=80&w=1200)

---

## 📌 What is this project?

**Jharkhand Scout** is a business analytics dashboard that helps entrepreneurs, investors, and policymakers identify the **best startup opportunities** in any area of Jharkhand — based on real census data, not guesswork.

Select a **District** → Select a **Locality** → Get a **data-backed business recommendation** with reasons.

---

## 🎯 Problem it Solves

Most people starting a business ask:
- *"What business should I start here?"*
- *"Is there demand for a gym / pharmacy / coaching center in my area?"*
- *"Which areas have untapped potential?"*

This project answers all of that using **real government census data**.

---

## 🗂️ Project Structure

```
Ranchi_Startup_Project/
├── app.py                          # Streamlit frontend UI
├── scripts/
│   └── run_analysis.py             # Data analysis + CSV generation
├── data/
│   ├── raw/
│   │   └── hlpca-colnames.csv
│   └── processed/
│       ├── jharkhand_analytics.csv # District-level scores
│       ├── area_mapping.csv        # Area-level recommendations
│       └── district_business_map.csv
├── static/
│   └── scout.png                   # Logo
├── india-districts-census-2011.csv # Source data
├── requirements.txt
└── README.md
```

---

## 🧠 How the Data Analysis Works

### Step 1 — Raw Data Source
- **India Census 2011** (`india-districts-census-2011.csv`)
- Contains 100+ columns per district: population, literacy, workers, income, households, sanitation, etc.

### Step 2 — Feature Engineering
From raw census columns, we calculate meaningful business indicators:

| Feature | Formula | What it means |
|---|---|---|
| `Literacy_Rate` | Literate / Population × 100 | Education level |
| `Talent_Score` | Graduates / Literate × 100 | Higher education density |
| `Urban_Ratio` | Urban HH / Total HH × 100 | Urbanisation level |
| `Youth_Ratio` | Age 0-29 / Population × 100 | Young population share |
| `Agri_Worker_Ratio` | Agri Workers / Total Workers × 100 | Farming dependency |
| `High_Income_Ratio` | HH earning >1.5L / Total HH × 100 | Spending power |
| `Mobile_Penetration` | Mobile HH / Total HH × 100 | Digital readiness |
| `Internet_Penetration` | Internet HH / Total HH × 100 | Connectivity |
| `Low_Sanitation` | 100 - Latrine Coverage | Healthcare gap indicator |
| `Population_Density` | Population / Max Population × 100 | Footfall potential |

### Step 3 — Z-Score Normalisation
Each feature is converted to a **Z-score** — comparing each district to the Jharkhand state average:
- Z > 0 → Above average
- Z < 0 → Below average

This makes all features comparable regardless of scale.

### Step 4 — Business Scoring
**25 business types** are defined, each with weighted census features:

```
Gym / Fitness Center     = Urban_Ratio(0.4) + High_Income(0.35) + Youth(0.25)
Coaching Center          = Literacy(0.4) + Youth(0.35) + Talent(0.25)
Agri-Input Store         = Agri_Workers(0.5) + Rural(0.3) + Workforce(0.2)
Hospital / Clinic        = Population(0.35) + Elderly(0.3) + Low_Sanitation(0.35)
...and 21 more
```

Each business gets a **composite score** per district = sum of (weight × Z-score).

### Step 5 — District Top 5
For each district, businesses are ranked by score → **Top 5 best-fit businesses** selected.

### Step 6 — Zone Type Detection (Area Level)
Since census data is district-level, we derive **zone type** for each area using district data ratios:

```
commercial  → High Urban + High Income + High Other Workers
student     → High Talent + High Youth + Urban
residential → Urban + Income + Low Agri
industrial  → High Other Workers + Urban + Low Agri
rural       → High Agri + Low Urban + Low Income
```

Areas within a district are assigned different zones based on their index position + district's dominant characteristics — ensuring **every locality gets a unique recommendation**.

### Step 7 — Final Area Recommendation
**Intersection logic:**
```
Area Recommendation = District Top5 ∩ Zone Preferred List
```
- If Ranchi's top5 = [IT Training, Hostel, Gym, Restaurant, Pharmacy]
- And Bariatu zone = Student
- Student preferred = [Coaching, Hostel, Stationery, Cloud Kitchen]
- **Match = Hostel / PG Accommodation** ✅

---

## 🏢 25 Business Ideas Covered

| Category | Businesses |
|---|---|
| 🎓 Education | Coaching Center, Hostel/PG, IT Training, Spoken English, Vocational School |
| 🏥 Health | Pharmacy, Hospital, Gym, Mental Health Clinic, Diagnostic Lab, Ayurvedic Center |
| 🍽️ Food | Restaurant, Cloud Kitchen, Chai Franchise, Organic Food Store |
| 💰 Finance | FinTech Kiosk, Electronics Shop, Insurance Agency |
| 🌾 Agriculture | Kisan Store, Cold Storage, Dairy Distribution, Solar Energy |
| 🚚 Commerce | Logistics Hub, Stationery Shop, Real Estate Agency |

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| **Python** | Core language |
| **Pandas** | Data processing & analysis |
| **NumPy** | Z-score calculations |
| **Streamlit** | Web dashboard UI |
| **Census 2011 CSV** | Primary data source |

---

## 🚀 How to Run

**1. Clone the repository**
```bash
git clone https://github.com/Buntysoni77/Ranchi-Startup-Project.git
cd Ranchi-Startup-Project
```

**2. Create virtual environment**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Run analysis (generates CSVs)**
```bash
python scripts/run_analysis.py
```

**5. Start the dashboard**
```bash
streamlit run app.py
```

---

## 📊 Output Files

| File | Description |
|---|---|
| `jharkhand_analytics.csv` | District scores, Z-scores, top recommendations |
| `area_mapping.csv` | Area-level recommendations with zone type, rank 1/2/3 |
| `district_business_map.csv` | Flat table of top 5 businesses per district |

---

## 🔍 Example Output

| District | Area | Zone | Recommendation |
|---|---|---|---|
| Ranchi | Bariatu | Student | Hostel / PG Accommodation |
| Ranchi | Piska More | Rural | Digital Skill / IT Training |
| Bokaro | Sector 4 | Commercial | Real Estate / Rental Agency |
| Dhanbad | Jharia | Industrial | Logistics / Delivery Hub |
| Gumla | Basia | Rural | Agri-Input / Kisan Store |

---

## 📈 Why This is a Real Data Analytics Project

- ✅ No hardcoded recommendations — everything derived from census numbers
- ✅ Z-score normalisation for fair district comparison
- ✅ Weighted multi-factor scoring per business type
- ✅ Zone detection algorithm using 5 census features
- ✅ Intersection logic for area-level precision
- ✅ 100+ census columns processed into actionable insights

---

## 👨‍💻 Author

**Bunty Soni**
GitHub: [@Buntysoni77](https://github.com/Buntysoni77)

---

## 📄 License

MIT License — free to use and modify.

---

<center><b>© 2026 JHARKHAND SCOUT | PROPELLING DIGITAL GROWTH IN THE HEARTLAND</b></center>
