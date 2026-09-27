#  LifeLink

**Intelligent Blood Availability, Exchange & Emergency Response Network**

> LifeLink connects patients, blood banks, and verified donors in one intelligent network — helping people find available blood, enabling blood banks to redistribute excess inventory, predicting shortages before they happen, and coordinating emergencies through a one-tap system.

---

## The Problem

> "The blood exists, but the person who needs it cannot find it quickly."

One blood bank may have surplus inventory while another nearby faces a critical shortage, with no effective way to coordinate between them. Meanwhile, valuable blood units can expire unused while patients elsewhere urgently need the same blood group. LifeLink bridges this gap by connecting blood banks, patients, and verified donors through a unified, intelligent network.
---

## What LifeLink Does

-  **Search** — Find nearby verified blood banks with real-time (and freshness-scored) availability
-  **Predict** — Forecast shortages before a blood group hits zero
-  **Rescue** — Flag units nearing expiry and match them to real demand elsewhere
-  **Balance** — Identify redistribution/exchange opportunities between blood banks
-  **One-Tap Emergency (SOS)** — Patient presses "Need Blood Now" → system searches institutional inventory, then escalates to verified donors if needed
-  **Network Map** — City-wide live view of blood availability (critical/low/healthy/excess)
-  **Verified Network** — Identity-verified users, donors, and institutions only

For the full breakdown of each module, escalation logic, and system design, see **[ARCHITECTURE.md](./ARCHITECTURE.md)**.

---

## Tech Stack

| Layer | Tech |
|---|---|
| Frontend | React + Tailwind CSS |
| Backend | Supabase + PostgreSQL |
| AI/ML | Python (forecasting + matching/optimization) |
| Maps | Maps API (location, distance) |
| Auth | OTP + sandbox identity/institutional verification |
| Notifications | App / SMS / Email |

---

## Demo Flow

1. Log in as a user → search a rare blood group → see nearby verified availability
2. Switch to a blood-bank account → view live inventory, shortage predictions, expiry alerts
3. Trigger a redistribution recommendation (excess ↔ shortage)
4. Activate an emergency request → watch institutional search → fallback to donor network
5. View the city-wide blood map

---

## Team

*LIFELINK* 
.
.
.
Gaurav Pandey | 
Mishika Agarwal |
Om Saini

---

**FIND BLOOD → PREDICT SHORTAGES → RESCUE INVENTORY → BALANCE SUPPLY → COORDINATE EMERGENCIES**
