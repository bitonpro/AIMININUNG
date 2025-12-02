# 🌐 ALL BITON Cloud Infrastructure Plan v1.1
**גרסה דו־לשונית | Hebrew + English**  
**תאריך עדכון:** 2 בדצמבר 2025  
**מהנדס תשתיות ראשי:** X-GPT GUIDES™  

---

## 📋 תקציר / Executive Summary
**עברית:**  
מסמך זה מתעד גרסה מעודכנת של תכנון מלא למערך ענן היברידי המשולב בבינה מלאכותית, כרייה, שירותי אינטרנט ותקשורת.  
השדרוג המרכזי: שימוש מושכל בקרדיטים מ-Vast.ai (382 $) והפרדה בין משאבים קבועים (Reserved) וגמישים (On-Demand).  

**English:**  
This document details the updated hybrid cloud infrastructure combining AI, mining, web services, and communication.  
Major update: optimized usage of Vast.ai credits ($382) and split between **Reserved (AI)** and **On-Demand (Mining)** compute tiers.

---

## ⚖️ חוקיות / Legality
- **Alibaba Cloud:** Mining is **forbidden**; AI and web services are allowed.  
- **Vast.ai:** Mining is **allowed** when funded by crypto.  
- **Regulation (Israel):** Mining is legal; taxation 25 %–50 %.  

**Key rule:**  
Do *not* mine on Alibaba Cloud — account termination risk.  
Use Alibaba only for management, APIs, Grafana and AI coordination.

---

## 🧠 ארכיטקטורה / Architecture

### 🧩 Management Layer – Alibaba Cloud
| Server | Role | Specs | Notes |
|---------|------|-------|-------|
| **A1** | Web/API (Abraham-AI Core) | 4 vCPU · 8 GB RAM · 100 GB SSD | Host API + Logic Core |
| **A2** | Monitoring (Grafana + Prometheus) | 4 vCPU · 8 GB RAM · 60 GB SSD | Dashboards |
| **A3** | Database | 2 vCPU · 4 GB RAM · 60 GB SSD | PostgreSQL / MySQL |
| **A4** | Dev/Test | 4 vCPU · 8 GB RAM | Windows Server sandbox |

---

### ⚙️ Compute Layer – Vast.ai
| Instance | Purpose | GPU / CPU / RAM | Mode | Notes |
|-----------|----------|-----------------|------|-------|
| **V1** | Main Mining | RTX 5090 · 16 vCPU · 64 GB | On-Demand | For cryptocurrency mining |
| **V2** | AI / Gaming | RTX 5090 · 16 vCPU · 64 GB | **Reserved** | Stable AI runtime |
| **V3** | Parallel Mining | RTX 5090 · 8 vCPU · 32 GB | On-Demand | Optional profit booster |

**Reserved Mode (V2):**  
Ensures persistent IP, checkpoint stability and no *RE-SCHEDULE* events after shutdown.  
Ideal for Abraham-AI model serving and LLM inference.

---

### 💾 Storage Layer
- **Google Drive 30 TB** – Backups & logs.  
- **Alibaba OSS** – Optional archival tier.  

---

## 💰 תקציב / Budget (Updated)
| Category | Monthly Cost ($) | Notes |
|-----------|-----------------|-------|
| Alibaba Management | 150 – 200 | Servers + DB |
| Vast.ai Compute | **0 (covered by $382 credits)** | Free until credits expire |
| CDN / APIs / Domains | 50 – 100 | Optional services |
| Reserve for tax / expansion | ≈ 52 | Safety buffer |
| **Total Actual Spend** | **≈ 250 – 350 $ (≤ 1 200 ₪)** | Reduced cost due to credits |

---

## 🎯 רווחיות כרייה / Mining Profitability
| Coin | Gross $/day | Net $/day | Monthly Net |
|------|--------------|-----------|--------------|
| Flux | 5.15 | 1.55 | ≈ 46.5 $ |
| Qubitcoin | 0.57 | 0.21 | ≈ 6.3 $ |
| Abelian | 4.00 | 0.40 | ≈ 12.0 $ |

*Profit varies with coin price, network difficulty, and power cost.*

---

## 🚀 שלבי יישום / Implementation Steps
1. **Days 0–3:** Create Alibaba Free Tier → deploy A1–A4 via Docker.  
2. **Days 4–7:** Fund Vast.ai with crypto → activate V1 (On-Demand).  
3. **Week 2:** Enable V2 (Reserved) for Abraham-AI → connect Grafana.  
4. **Month 1+:** Optimize GPU usage → expand mining if profitable.  

---

## 🔐 אבטחה / Security
- Firewall + SSH keys + 2FA.  
- Monitor costs (Vast.ai can rise fast).  
- Backup to Google Drive + local.  

---

## 🤖 הערות AI / AI Notes
- Structured for autonomous parsing by X-GPT GUIDES™ and Abraham-AI.  
- Tables are machine-readable (budget / architecture / roles).  
- Intended for dynamic cloud orchestration.  

---

## 📞 קשר / Contact
**Project:** ALL BITON  
**Website:** [www.all.biton.pro](http://www.all.biton.pro)  
**Version:** 1.1 **Status:** Operational Blueprint  
**Chief Engineer:** X-GPT GUIDES™  
