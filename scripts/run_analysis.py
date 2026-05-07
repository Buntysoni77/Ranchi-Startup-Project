import pandas as pd
import numpy as np
import os
 
# ── 25 Business Ideas mapped to Census Data Features ─────────────────────────
BUSINESSES = {
    # ── EDUCATION & SKILL ─────────────────────────────────────────────────────
    "Coaching / Tuition Center": {
        "features": {"Literacy_Rate": 0.4, "Youth_Ratio": 0.35, "Talent_Score": 0.25},
        "tag": "High youth + literacy = strong tuition demand."
    },
    "Hostel / PG Accommodation": {
        "features": {"Talent_Score": 0.4, "Youth_Ratio": 0.35, "Urban_Ratio": 0.25},
        "tag": "Graduate students & migrants = steady PG/hostel demand."
    },
    "Digital Skill / IT Training": {
        "features": {"Talent_Score": 0.4, "Internet_Penetration": 0.35, "Urban_Ratio": 0.25},
        "tag": "Graduates + internet access = IT training gap to fill."
    },
    "Spoken English / Soft Skill Center": {
        "features": {"Youth_Ratio": 0.4, "Literacy_Rate": 0.35, "Urban_Ratio": 0.25},
        "tag": "Young literate urban population = language skill demand."
    },
    "Vocational Trade School": {
        "features": {"Youth_Ratio": 0.35, "Agri_Worker_Ratio": 0.3, "Workforce_Availability": 0.35},
        "tag": "Large non-worker youth = demand for job-ready skill training."
    },
 
    # ── HEALTH & WELLNESS ─────────────────────────────────────────────────────
    "Pharmacy / Medical Store": {
        "features": {"Population_Density": 0.4, "Elderly_Ratio": 0.35, "Urban_Ratio": 0.25},
        "tag": "Dense + aging population = high medicine demand."
    },
    "Hospital / Clinic": {
        "features": {"Population_Density": 0.35, "Elderly_Ratio": 0.3, "Low_Sanitation": 0.35},
        "tag": "Poor sanitation + dense population = critical healthcare gap."
    },
    "Gym / Fitness Center": {
        "features": {"Urban_Ratio": 0.4, "High_Income_Ratio": 0.35, "Youth_Ratio": 0.25},
        "tag": "Urban youth with spending power = fitness culture rising."
    },
    "Mental Health / Counseling Clinic": {
        "features": {"Literacy_Rate": 0.4, "Urban_Ratio": 0.35, "High_Income_Ratio": 0.25},
        "tag": "Educated urban middle class = awareness + demand for mental health."
    },
    "Diagnostic / Pathology Lab": {
        "features": {"Population_Density": 0.4, "Elderly_Ratio": 0.3, "Literacy_Rate": 0.3},
        "tag": "Literate population + aging = demand for preventive diagnostics."
    },
    "Ayurvedic / Herbal Wellness Center": {
        "features": {"Rural_Ratio": 0.4, "Elderly_Ratio": 0.35, "Agri_Worker_Ratio": 0.25},
        "tag": "Rural communities trust traditional medicine = steady clientele."
    },
 
    # ── FOOD & BEVERAGE ───────────────────────────────────────────────────────
    "Restaurant / Dhaba": {
        "features": {"Urban_Ratio": 0.35, "Mobile_Penetration": 0.3, "High_Income_Ratio": 0.35},
        "tag": "Urban + disposable income = dining out culture."
    },
    "Cloud Kitchen / Tiffin Service": {
        "features": {"Youth_Ratio": 0.4, "Mobile_Penetration": 0.35, "Urban_Ratio": 0.25},
        "tag": "Working youth + mobiles = online food order demand."
    },
    "Tea Stall / Chai Franchise": {
        "features": {"Population_Density": 0.45, "Workforce_Availability": 0.3, "Rural_Ratio": 0.25},
        "tag": "High footfall + labour = scalable low-investment chai business."
    },
    "Organic / Local Food Store": {
        "features": {"Agri_Worker_Ratio": 0.4, "Rural_Ratio": 0.35, "Literacy_Rate": 0.25},
        "tag": "Farm produce surplus + aware consumers = farm-to-table opportunity."
    },
 
    # ── FINANCE & TECH ────────────────────────────────────────────────────────
    "Micro-Finance / FinTech Kiosk": {
        "features": {"Mobile_Penetration": 0.4, "Rural_Ratio": 0.35, "Literacy_Rate": 0.25},
        "tag": "Mobile-literate rural households = digital banking gap."
    },
    "Mobile Recharge / Electronics Shop": {
        "features": {"Mobile_Penetration": 0.4, "Youth_Ratio": 0.3, "Population_Density": 0.3},
        "tag": "High mobile users + dense population = accessories & recharge demand."
    },
    "Insurance Agency": {
        "features": {"Literacy_Rate": 0.35, "High_Income_Ratio": 0.35, "Elderly_Ratio": 0.3},
        "tag": "Literate + income + aging = growing insurance awareness."
    },
 
    # ── AGRICULTURE & RURAL ───────────────────────────────────────────────────
    "Agri-Input / Kisan Store": {
        "features": {"Agri_Worker_Ratio": 0.5, "Rural_Ratio": 0.3, "Workforce_Availability": 0.2},
        "tag": "Dominant farming community = seeds, tools, fertilizer demand."
    },
    "Cold Storage / Agri Warehouse": {
        "features": {"Agri_Worker_Ratio": 0.45, "Rural_Ratio": 0.35, "Workforce_Availability": 0.2},
        "tag": "Perishable farm produce + lack of storage = high-value gap."
    },
    "Dairy / Milk Distribution": {
        "features": {"Rural_Ratio": 0.45, "Agri_Worker_Ratio": 0.35, "Population_Density": 0.2},
        "tag": "Rural livestock households = raw milk supply chain opportunity."
    },
 
    # ── COMMERCE & LOGISTICS ──────────────────────────────────────────────────
    "Logistics / Delivery Hub": {
        "features": {"Urban_Ratio": 0.35, "Mobile_Penetration": 0.35, "High_Income_Ratio": 0.3},
        "tag": "E-commerce boom + urban buyers = last-mile delivery gap."
    },
    "Stationery / Printing Shop": {
        "features": {"Youth_Ratio": 0.4, "Literacy_Rate": 0.35, "Population_Density": 0.25},
        "tag": "Student-dense areas = constant stationery & printing demand."
    },
    "Real Estate / Rental Agency": {
        "features": {"Urban_Ratio": 0.4, "High_Income_Ratio": 0.35, "Population_Density": 0.25},
        "tag": "Urban growth + income = property rental & buying demand."
    },
    "Solar / Renewable Energy Dealer": {
        "features": {"Rural_Ratio": 0.4, "Low_Sanitation": 0.3, "Agri_Worker_Ratio": 0.3},
        "tag": "Rural areas with poor grid = solar panel & pump demand."
    },
}
 
def run_analysis():
    print("🧠 Running Business Recommendation Analysis...")
 
    df = pd.read_csv('india-districts-census-2011.csv')
    jh = df[df['State name'].str.upper() == 'JHARKHAND'].copy()
    jh['District'] = jh['District name'].str.title()
 
    H, P = jh['Households'], jh['Population']
 
    # ── Feature Engineering ───────────────────────────────────────────────────
    jh['Literacy_Rate']          = jh['Literate'] / P * 100
    jh['Talent_Score']           = jh['Graduate_Education'] / jh['Literate'] * 100
    jh['Urban_Ratio']            = jh['Urban_Households'] / H * 100
    jh['Rural_Ratio']            = jh['Rural_Households'] / H * 100
    jh['Internet_Penetration']   = jh['Households_with_Internet'] / H * 100
    jh['Mobile_Penetration']     = jh['Households_with_Telephone_Mobile_Phone_Mobile_only'] / H * 100
    jh['Agri_Worker_Ratio']      = (jh['Cultivator_Workers'] + jh['Agricultural_Workers']) / jh['Workers'] * 100
    jh['Workforce_Availability'] = jh['Non_Workers'] / P * 100
    jh['High_Income_Ratio']      = jh[['Power_Parity_Rs_150000_240000','Power_Parity_Rs_240000_330000',
                                        'Power_Parity_Rs_330000_425000','Power_Parity_Above_Rs_545000']].sum(axis=1) / H * 100
    jh['Youth_Ratio']            = jh['Age_Group_0_29'] / P * 100
    jh['Elderly_Ratio']          = jh['Age_Group_50'] / P * 100
    jh['Population_Density']     = P / P.max() * 100
    jh['Low_Sanitation']         = 100 - (jh['Having_latrine_facility_within_the_premises_Total_Households'] / H * 100)
 
    # ── Z-score normalisation ─────────────────────────────────────────────────
    FEATURES = list({f for b in BUSINESSES.values() for f in b['features']})
    for col in FEATURES:
        jh[f'Z_{col}'] = (jh[col] - jh[col].mean()) / (jh[col].std() or 1)
 
    # ── Composite score per business ──────────────────────────────────────────
    for biz, meta in BUSINESSES.items():
        jh[f'Score_{biz}'] = sum(w * jh[f'Z_{feat}'] for feat, w in meta['features'].items())
 
    # ── Top-5 businesses per district ─────────────────────────────────────────
    def top_businesses(row, n=5):
        scores = {b: row[f'Score_{b}'] for b in BUSINESSES}
        return [
            {"rank": i+1, "business": b, "score": round(scores[b], 2),
             "reason": BUSINESSES[b]['tag']}
            for i, b in enumerate(sorted(scores, key=scores.get, reverse=True)[:n])
        ]
 
    jh['Top_Businesses']         = jh.apply(top_businesses, axis=1)
    jh['Primary_Recommendation'] = jh['Top_Businesses'].apply(lambda x: x[0]['business'])
    jh['Primary_Reason']         = jh['Top_Businesses'].apply(lambda x: x[0]['reason'])
 
    # ── Save outputs ──────────────────────────────────────────────────────────
    os.makedirs("data/processed", exist_ok=True)
    jh.to_csv("data/processed/jharkhand_analytics.csv", index=False)
 
    flat = [{"District": row['District'], **biz,
             "Urban_Ratio": round(row['Urban_Ratio'], 1),
             "Literacy_Rate": round(row['Literacy_Rate'], 1),
             "Youth_Ratio": round(row['Youth_Ratio'], 1)}
            for _, row in jh.iterrows() for biz in row['Top_Businesses']]
    pd.DataFrame(flat).to_csv("data/processed/district_business_map.csv", index=False)
 
    ALL_AREAS = {
        "Ranchi": ["Piska More","Lalpur","Kanke","Doranda","Hinoo","Ratu","Namkum","Bariatu","Dhurwa"],
        "Dhanbad": ["Jharia","Saraidhela","Sindri","Katras","Govindpur","Nirsa","Chirkunda"],
        "Bokaro": ["Sector 4","Chas","Bermo","Bokaro Thermal","Gumia","Chandrapura"],
        "Purbi Singhbhum": ["Sakchi","Bistupur","Mango","Parsudih","Ghatshila","Musabani"],
        "Hazaribagh": ["Barkagaon","Barhi","Ichak","Chauparan","Bishnugarh"],
        "Deoghar": ["Jasidih","Madhupur","Satsang Nagar","Castairs Town","Sarath"],
        "Giridih": ["Bengabad","Dumri","Gandey","Jamua","Pirtand"],
        "Palamu": ["Daltonganj","Chainpur","Lesliganj","Panki","Satbarwa"],
        "Garhwa": ["Bhavnathpur","Kandi","Majhiaon","Meral","Nagar Untari"],
        "Chatra": ["Itkhori","Kanhachatti","Pratappur","Simaria","Tandwa"],
        "Kodarma": ["Jhumri Telaiya","Domchanch","Jainagar","Satgawan"],
        "Godda": ["Mahagama","Meherma","Pathargama","Poreyahat","Sundarpahari"],
        "Sahibganj": ["Barharwa","Berheit","Borio","Rajmahal","Taljhari"],
        "Pakur": ["Amrapara","Hiranpur","Littipara","Maheshpur","Pakuria"],
        "Dumka": ["Jama","Jarmundi","Masalia","Ramgarh","Shikaripara"],
        "Jamtara": ["Fatehpur","Kundhit","Nala","Narayanpur"],
        "Ramgarh": ["Bhurkunda","Gola","Mandu","Patratu","Rajrappa"],
        "Khunti": ["Karra","Murhu","Rania","Torpa"],
        "Lohardaga": ["Bhandra","Kuru","Kisko","Senha"],
        "Gumla": ["Basia","Bishunpur","Kamdara","Palkot","Raidih"],
        "Simdega": ["Bano","Jaldega","Kersai","Kurdeg","Thethaitanger"],
        "Pashchimi Singhbhum": ["Chaibasa","Chakradharpur","Jagannathpur","Kiriburu","Noamundi"],
        "Saraikela-Kharsawan": ["Adityapur","Chandil","Gamharia","Kharsawan"],
        "Latehar": ["Balumath","Barwadih","Chandwa","Mahuadanr"],
    }
    rows = [{"District": d, "Area": a} for d, areas in ALL_AREAS.items() for a in areas]
    pd.DataFrame(rows).to_csv("data/processed/area_mapping.csv", index=False)
 
    print("✅ Done!")
    print(jh[['District','Primary_Recommendation']].to_string(index=False))
 
if __name__ == "__main__":
    run_analysis()
