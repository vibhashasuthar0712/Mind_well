<div align="center">

# 🌿 Wellora

### Workplace Mental Wellbeing, Reimagined

**A privacy-conscious, activity-based workplace wellbeing platform designed to help employees pause, reflect, and seek support — without relying only on traditional questionnaires.**

<br>

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge\&logo=python\&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge\&logo=fastapi\&logoColor=white)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-D71F00?style=for-the-badge\&logo=sqlalchemy\&logoColor=white)](https://www.sqlalchemy.org/)
[![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge\&logo=sqlite\&logoColor=white)](https://www.sqlite.org/)
[![JavaScript](https://img.shields.io/badge/JavaScript-Frontend-F7DF1E?style=for-the-badge\&logo=javascript\&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge\&logo=github\&logoColor=white)](https://github.com/vibhashasuthar0712/wellora)
[![Render](https://img.shields.io/badge/Deployed%20on-Render-46E3B7?style=for-the-badge\&logo=render\&logoColor=black)](https://render.com/)

<br>

### 🚀 [Live Demo](https://mind-well-1.onrender.com/) · 💻 [GitHub Repository](https://github.com/vibhashasuthar0712/wellora)

<br>

> **Your wellbeing. Your privacy. Your support.**

</div>

---

## 🌱 About Wellora

**Wellora** is a workplace mental wellbeing platform that explores a more human-centered alternative to traditional questionnaire-only approaches.

Instead of repeatedly asking employees direct questions about stress, anxiety, or wellbeing, Wellora gives them **voluntary ways to interact with the platform** through games, conversations, relaxation activities, check-ins, and private journaling.

The platform can use interaction patterns as **additional wellbeing signals over time**, while recognizing that these signals are **not medical diagnoses**.

### The core idea

```text
Traditional Approach
        │
        ▼
   Ask Questions
        │
        ▼
   Collect Answers
        │
        ▼
   Assess Wellbeing


              VS


             Wellora
                │
                ▼
        Voluntary Engagement
                │
        ┌───────┼────────┐
        ▼       ▼        ▼
      Play    Talk     Relax
        │       │        │
        └───────┼────────┘
                ▼
       Observe Patterns
                │
                ▼
        Identify Signals
                │
                ▼
       Offer Appropriate
            Support
                │
                ▼
       Human Follow-up
```

---

# ✨ Why Wellora?

Workplace wellbeing is not always as simple as asking:

> *"Are you stressed?"*

Employees may:

* Feel uncomfortable answering direct questions
* Avoid discussing personal problems
* Prefer private reflection
* Need a short break rather than an assessment
* Want someone or something to talk to
* Need human support when a situation becomes concerning

Wellora therefore focuses on **choice, engagement, privacy, and support**.

---

# 🧩 Core Features

<div align="center">

|           🎮           |        💬        |           🧘          |          📝         |           📔           |
| :--------------------: | :--------------: | :-------------------: | :-----------------: | :--------------------: |
|    **Play & Check**    | **Talk & Share** |   **Relax & Reset**   |     **Check-in**    |   **Private Journal**  |
| Interactive activities |  AI conversation | Breathing & grounding | Optional reflection | Personal writing space |

</div>

---

## 🎮 01 — Play & Check

Employees can choose from lightweight interactive activities rather than being forced through a questionnaire.

### Available activities

| Activity            | What it explores                |
| ------------------- | ------------------------------- |
| 🎯 **Focus Hunt**   | Reaction time, accuracy, errors |
| ⚡ **Reaction Rush** | Response speed                  |
| 🧠 **Memory Match** | Memory interaction patterns     |
| 🌈 **Color Flow**   | Interaction consistency         |
| 🧩 **Choice Quest** | Choice and response patterns    |

These activities are designed to generate **possible wellbeing signals**, not diagnostic conclusions.

### Important distinction

```text
One result
   ↓
Limited meaning

Repeated patterns
   ↓
More useful context

Patterns + voluntary context
   ↓
Potential wellbeing signal
```

---

## 💬 02 — Talk & Share

Sometimes employees simply want to talk.

The **Talk & Share** feature provides an AI-supported conversational space where employees can:

* Express their thoughts
* Reflect on their situation
* Receive general supportive suggestions
* Explore simple coping strategies
* Ask for guidance

### AI limitations are part of the design

Wellora does **not** assume AI can perfectly understand someone's mental state.

AI may:

* Misunderstand context
* Miss non-verbal signals
* Receive incomplete information
* Fail to recognize the seriousness of a situation

Therefore, Wellora explores a **human-in-the-loop support model** rather than making AI the final authority.

---

## 🧘 03 — Relax & Reset

A dedicated space for employees who simply need to pause.

Includes simple wellbeing activities such as:

* 🌬️ Breathing
* 🌱 Grounding
* 🧘 Relaxation
* ⏸️ Short mental resets

No assessment is required.

---

## 📝 04 — Optional Check-in

Employees can optionally provide a short wellbeing check-in.

The check-in is:

* Voluntary
* Lightweight
* Designed to complement activities
* Not intended as a medical assessment

---

## 📔 05 — Private Journal

Sometimes people don't want to talk.

They just want somewhere to write.

Wellora provides a dedicated journal where employees can privately reflect on thoughts and experiences.

### Journal features

* ✍️ Write personal thoughts
* 💾 Save entries
* 📖 View previous entries
* 🗑️ Delete entries
* 🌱 Optional post-writing reflection

The journal is kept separate from the HR/responder wellbeing dashboard.

> *"I'm not sharing this with anyone. I'm just writing because sometimes writing makes me feel a little better."*

---

# 🚨 From Detection to Support

One of Wellora's important design questions is:

> **What happens after a concerning signal is detected?**

Rather than treating detection as the end of the process, Wellora explores a workflow for appropriate human follow-up.

```text
┌─────────────────┐
│     Employee    │
└────────┬────────┘
         │
         ▼
┌─────────────────────┐
│ Play / Talk / Relax │
│ / Check-in          │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  Wellbeing Signals  │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│     Risk Engine     │
└─────────┬───────────┘
          │
     ┌────┴─────┐
     │          │
     ▼          ▼
   Normal   Concerning
     │          │
     │          ▼
     │    ┌────────────┐
     │    │ Responder  │
     │    └─────┬──────┘
     │          │
     │          ▼
     │    ┌────────────┐
     │    │ HR/Support │
     │    └────────────┘
     │
     ▼
 Continue Use
```

---

# 🖥️ Product Screenshots

> Add real screenshots from the deployed application here.

### 🏠 Employee Dashboard

<p align="center">
  <img src="assets/screenshots/employee-dashboard.png" alt="Wellora Employee Dashboard" width="850">
</p>

---

### 🎮 Play & Check

<p align="center">
  <img src="assets/screenshots/play-check.png" alt="Wellora Play and Check" width="850">
</p>

---

### 💬 Talk & Share

<p align="center">
  <img src="assets/screenshots/talk-share.png" alt="Wellora Talk and Share" width="850">
</p>

---

### 🧘 Relax & Reset

<p align="center">
  <img src="assets/screenshots/relax-reset.png" alt="Wellora Relax and Reset" width="850">
</p>

---

### 📔 Private Journal

<p align="center">
  <img src="assets/screenshots/private-journal.png" alt="Wellora Private Journal" width="850">
</p>

---

### 🚨 Responder Dashboard

<p align="center">
  <img src="assets/screenshots/responder-dashboard.png" alt="Wellora Responder Dashboard" width="850">
</p>

---

# 🌐 Live Demo

<div align="center">

## 🚀 [Open Wellora](https://mind-well-1.onrender.com/)

**Try the deployed prototype**

<br>

### 💻 [View Source Code on GitHub](https://github.com/vibhashasuthar0712/wellora)

</div>

> **Demo:** Wellora is currently a prototype designed for demonstration, evaluation, and concept validation. It is not a production clinical or emergency-response system.

---

# 🏗️ Architecture

```text
                         ┌───────────────────┐
                         │      WELLORA      │
                         └─────────┬─────────┘
                                   │
             ┌─────────────────────┼─────────────────────┐
             │                     │                     │
             ▼                     ▼                     ▼
      ┌─────────────┐       ┌─────────────┐       ┌─────────────┐
      │ Play & Check│       │ Talk & Share│       │ Relax &Reset│
      └──────┬──────┘       └──────┬──────┘       └──────┬──────┘
             │                     │                     │
             └─────────────────────┼─────────────────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │ Optional Check-in │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │ Wellbeing Signals │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │    Risk Engine    │
                         └─────────┬─────────┘
                                   │
                         ┌─────────┴─────────┐
                         ▼                   ▼
                    ┌─────────┐        ┌───────────┐
                    │ Normal  │        │Concerning │
                    └────┬────┘        └─────┬─────┘
                         │                   │
                         ▼                   ▼
                     Continue          ┌───────────┐
                                       │ Responder │
                                       └─────┬─────┘
                                             │
                                             ▼
                                       ┌───────────┐
                                       │HR/Support │
                                       └───────────┘
```

---

# 🛠️ Tech Stack

<div align="center">

| Layer              | Technology                        |
| :----------------- | :-------------------------------- |
| 🎨 Frontend        | HTML5 · CSS3 · JavaScript         |
| ⚙️ Backend         | Python · FastAPI                  |
| 🗄️ Database       | SQLite                            |
| 🔗 ORM             | SQLAlchemy                        |
| 🤖 AI              | AI-powered conversational support |
| 🚀 Deployment      | Render                            |
| 📦 Version Control | Git · GitHub                      |

</div>

---

# 📁 Project Structure

```text
wellora/
│
├── main.py
├── database.py
├── models.py
├── risk_engine.py
│
├── index.html
├── employee.html
├── checkin.html
├── hr.html
├── responder.html
├── journal.html
├── relax.html
├── talk.html
│
├── game.html
├── reaction.html
├── memory.html
├── color.html
├── choice.html
│
├── requirements.txt
├── add_journal_column.py
├── .gitignore
└── mindwell.db
```

---

# 🚀 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/vibhashasuthar0712/wellora.git
cd wellora
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate it

**Windows**

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Start the application

```bash
uvicorn main:app --reload
```

### 6. Open Wellora

```text
http://127.0.0.1:8000
```

---

# 🔗 Important Routes

| Route        | Purpose              |
| :----------- | :------------------- |
| `/`          | Login / Landing Page |
| `/employee`  | Employee Dashboard   |
| `/game`      | Focus Hunt           |
| `/reaction`  | Reaction Rush        |
| `/memory`    | Memory Match         |
| `/color`     | Color Flow           |
| `/choice`    | Choice Quest         |
| `/talk`      | Talk & Share         |
| `/relax`     | Relax & Reset        |
| `/journal`   | Private Journal      |
| `/checkin`   | Optional Check-in    |
| `/responder` | Responder Dashboard  |
| `/hr`        | HR Dashboard         |
| `/health`    | API Health Check     |

---

# 🔐 Privacy & Safety

Wellora is designed with privacy and responsible AI use in mind.

### Principles

* Participation is voluntary.
* Activities are not medical diagnostic tests.
* AI does not replace professional mental-health care.
* Journal entries are separated from HR/responder wellbeing dashboards.
* Wellbeing signals should not be interpreted in isolation.
* Concerning situations should involve appropriate human support.
* The system recognizes the limitations of detecting mental states through online interaction.

### ⚠️ Important

Wellora is a **wellbeing support prototype**, not:

* A medical diagnostic system
* A replacement for a psychologist or mental-health professional
* An emergency-response service
* A guaranteed risk-detection system

---

# 📊 Wellbeing Signal Philosophy

Wellora is built around **patterns rather than isolated scores**.

```text
                 ┌─────────────────────┐
                 │   Activity Result   │
                 └──────────┬──────────┘
                            │
                            ▼
                    Limited Context
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Repeated Patterns   │
                 └──────────┬──────────┘
                            │
                            ▼
                  Additional Context
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Possible Signal     │
                 └──────────┬──────────┘
                            │
                            ▼
                     Human Support
```

This reduces the risk of treating a single game score or response as proof of a person's mental-health condition.

---

# 💡 What Makes Wellora Different?

| Traditional Approach          | 🌿 Wellora                                   |
| :---------------------------- | :------------------------------------------- |
| Questionnaire-heavy           | Multiple voluntary interaction options       |
| Direct questions              | Games, conversation, relaxation & reflection |
| Single assessment             | Patterns over time                           |
| Detection-focused             | Detection → response → follow-up             |
| AI as the main solution       | AI + human support                           |
| Limited private reflection    | Dedicated private journal                    |
| One-size-fits-all interaction | Employee chooses how to engage               |

---

# 🎯 Project Goals

Wellora aims to make workplace wellbeing support:

* 🌱 More approachable
* 🧠 More human-centered
* 🔐 More privacy-conscious
* 🎮 Less questionnaire-dependent
* 💬 More conversational
* 🤝 More support-oriented
* 🇮🇳 Practical and affordable for workplace environments

---

# 🔮 Future Scope

Possible future improvements include:

* 📈 Long-term wellbeing trend analysis
* 🤖 Advanced NLP and conversational safety
* 🧠 Personalized wellbeing recommendations
* 🔐 Strong authentication
* 👥 Role-based access control
* 🗄️ Production-grade database infrastructure
* 📱 Mobile application
* 🔔 Improved responder notifications
* 🧑‍⚕️ Professional support integration
* 🔄 Structured follow-up workflows
* 🔒 Stronger privacy, consent, retention, and security controls
* 📊 Privacy-preserving organizational wellbeing analytics

---

# ⚠️ Current Prototype Limitations

Wellora is currently a **working prototype**.

Current limitations include:

* Activity signals cannot diagnose mental-health conditions.
* AI responses are not professional medical advice.
* Online interaction cannot capture every aspect of a person's wellbeing.
* Authentication is currently prototype-oriented.
* SQLite is suitable for the current demonstration but would need production-grade persistence for real deployment.
* Production deployment would require stronger authentication, authorization, encryption, consent management, auditing, data retention controls, and security testing.
* Emergency situations should always be handled through appropriate real-world emergency or professional support systems.

---

# 👩‍💻 Author

<div align="center">

### Vibhasha Suthar

**Aspiring Data Scientist · Machine Learning & NLP Enthusiast**

Interested in:

`Machine Learning` · `NLP` · `Deep Learning` · `Data Analytics` · `AI Applications` · `FastAPI` · `Deployment`

<br>

[![GitHub](https://img.shields.io/badge/GitHub-vibhashasuthar0712-181717?style=for-the-badge\&logo=github)](https://github.com/vibhashasuthar0712)

</div>

---

# ⭐ Support the Project

If you find the idea behind Wellora interesting:

⭐ **Star the repository**
🍴 **Explore the code**
💡 **Share feedback**
🚀 **Try the live demo**

<br>

<div align="center">

## 🌿 Wellora

### *Your wellbeing. Your privacy. Your support.*

**Built to explore a more human-centered approach to workplace wellbeing.**

<br>

**[🚀 Live Demo](https://mind-well-1.onrender.com/) 
[💻 GitHub](https://github.com/vibhashasuthar0712/wellora)**

</div>
