# Documentație Academică – Modulul de Extragere a Atributelor Psihometrice în Cybersecurity

Această documentație prezintă în detaliu modulul de extragere a atributelor psihometrice folosit în cadrul aplicației de risk management pentru cybersecurity. Modulul se bazează pe trei metode de extragere: folosirea unui model antrenat (ModelExtractor), metoda bazată pe prompturi (PromptExtractor) și metoda bazată pe serviciile Azure (AzureExtractor). De asemenea, sunt discutate cele cinci atribute psihometrice alese – *awareness*, *conscientiousness*, *stress*, *neuroticism* și *risk_tolerance* – împreună cu relevanța lor în domeniul securității cibernetice și raționamentul din spatele alegerii acestor metode.

---

## 1. Introducere

În contextul securității cibernetice, comportamentul uman și factorii psihologici joacă un rol critic în prevenirea și gestionarea atacurilor. Studiile recente indică faptul că anumite trăsături psihometrice pot fi corelate cu comportamentele de risc și susceptibilitatea la atacuri cibernetice. Modulul de extragere a atributelor psihometrice propus vizează cuantificarea a cinci dimensiuni relevante, utilizând tehnologii avansate din domeniul NLP (Natural Language Processing).

---

## 2. Relevanța Atributelor Psihometrice în Cybersecurity

### 2.1. Awareness (Conștientizare)
- **Relevanță:** Nivelul de conștientizare se referă la gradul de cunoaștere al celor mai bune practici în securitate cibernetică. O conștientizare crescută poate conduce la comportamente preventive, reducând expunerea la riscuri.
- **Literatură:** Conform studiilor din domeniul securității cibernetice, angajații cu un nivel ridicat de awareness sunt mai puțin susceptibili la atacuri de tip phishing sau social engineering.

### 2.2. Conscientiousness (Conștiinciozitate)
- **Relevanță:** Această trăsătură indică atenția la detalii și respectarea procedurilor. În mediile critice, cum ar fi cele de securitate IT, o conștiinciozitate ridicată este esențială pentru implementarea corectă a politicilor de securitate.
- **Literatură:** Cercetările psihologice sugerează că persoanele conștiincioase tind să respecte procedurile și regulile, ceea ce reduce erorile umane ce pot duce la breșe de securitate.

### 2.3. Stress
- **Relevanță:** Nivelul de stres influențează semnificativ capacitatea de luare a deciziilor. În situații de criză, un nivel ridicat de stres poate compromite capacitatea de reacție rapidă și corectă la amenințări.
- **Literatură:** Studii în psihologie organizațională arată că stresul cronic poate afecta performanța și poate crește vulnerabilitatea la erori, fiind un factor de risc în mediile de lucru supuse presiunii constante.

### 2.4. Neuroticism
- **Relevanță:** Această dimensiune măsoară tendința de a experimenta emoții negative. În contextul securității, nivelurile ridicate de neuroticism pot influența comportamentul în fața riscurilor, fie prin reacții exagerate, fie prin subestimarea riscurilor.
- **Literatură:** Există studii care corelează nivelurile ridicate de neuroticism cu o susceptibilitate crescută la anxietate și decizii iraționale, aspecte ce pot afecta răspunsul la incidentele de securitate.

### 2.5. Risk Tolerance (Toleranța la Risc)
- **Relevanță:** Direct legată de comportamentul față de riscuri, această dimensiune măsoară gradul de dispus la asumarea riscurilor. Persoanele cu un nivel ridicat de risk tolerance pot lua decizii care expun organizația la atacuri cibernetice.
- **Literatură:** Literatura în domeniul managementului riscului subliniază că o toleranță ridicată la risc poate fi un predictor al comportamentelor imprudente, esențial de monitorizat în cadrul securității cibernetice.

---

## 3. Metodologiile de Extragere a Atributelor

Pentru extragerea celor cinci atribute psihometrice, se folosesc trei metode complementare:

### 3.1. ModelExtractor (Model Bazat pe BERT)
- **Descriere:** Acest extractor utilizează un model BERT preantrenat și fine-tuned pentru problema de regresie pe setul de date psihometrice. Modelul primește textul ca input și returnează cinci scoruri corespunzătoare celor cinci atribute.
- **Beneficii:**
  - **Data-driven:** Abordare bazată pe date, capabilă să învețe relații complexe din text.
  - **Personalizare:** Poate fi recalibrat sau fine-tuned pe seturi de date specifice organizației.
- **Limitări:** Necesită un set de date etichetat corespunzător și resurse computaționale semnificative pentru antrenare.

### 3.2. PromptExtractor (Metodă Bazată pe Prompturi)
- **Descriere:** Această metodă folosește un model de limbaj de mari dimensiuni (ex. GPT-3.5-turbo) pentru a extrage atributele psihometrice prin generarea unui răspuns în format JSON. Se construiește un prompt detaliat care cere analiza textului pe baza celor cinci dimensiuni.
- **Beneficii:**
  - **Flexibilitate:** Nu necesită antrenare suplimentară; se bazează pe cunoștințele vaste ale modelului.
  - **Rapiditate:** Poate oferi rezultate rapide prin tehnici de prompt engineering.
- **Limitări:** Costuri potențial ridicate (în funcție de modelul folosit) și dependența de calitatea promptului; uneori, răspunsurile pot fi inconsistente.

### 3.3. AzureExtractor (Serviciu Azure Text Analytics)
- **Descriere:** Acest extractor utilizează serviciile cognitive Azure pentru a efectua o analiză de sentiment și opinion mining. Răspunsul este mapat pe cele cinci atribute folosind reguli heuristice bazate pe cuvinte-cheie.
- **Beneficii:**
  - **Robustețe:** Folosește un serviciu cloud produs de Microsoft, recunoscut pentru scalabilitate și fiabilitate.
  - **Integrabilitate:** Ușor de integrat într-un flux de lucru deja existent, cu configurare minimă.
- **Limitări:** Mapează rezultatele prin reguli fixe, care pot fi mai puțin adaptabile la variații subtile ale textului.

---

## 4. Beneficiile Metodelor și Alternative Potențiale

### 4.1. Beneficiile Metodelor Folosite
- **Combinarea abordărilor:** Utilizarea simultană a a trei metode (model, prompt și Azure) permite obținerea unor predicții complementare, sporind robustețea evaluării psihometrice.
- **Adaptabilitate:** În funcție de contextul organizațional și de resursele disponibile, se poate alege metoda cea mai potrivită sau se pot combina rezultatele pentru o decizie mai informată.
- **Scalabilitate:** Serviciile cloud (precum Azure) și modelele preantrenate permit scalarea rapidă a sistemului pentru a gestiona volume mari de date.

### 4.2. Alternative și Îmbunătățiri Viitoare
- **Modele de tip Graph Neural Networks (GNN):** Pentru a capta relațiile complexe între angajați și entități, GNN-urile ar putea fi utilizate pentru a integra informațiile din graf într-o evaluare holistică a riscului.
- **Alte servicii cloud:** În loc de Azure, se pot utiliza și servicii precum AWS Comprehend sau Google Cloud Natural Language, care pot oferi analize sentimentale și extragerea entităților.
- **Metode hibride:** O abordare hibridă care combină extragerea bazată pe reguli cu modele învățate automat poate oferi o precizie sporită, integrând atât cunoștințele explicite cât și cele învățate din date.
- **Optimizarea prompturilor:** Pentru metoda bazată pe prompturi, se pot investiga tehnici de optimizare a prompturilor (prompt engineering) și fine-tuning al modelului LLM pentru a obține rezultate mai consistente.

---

## 5. Concluzii

Alegerea celor cinci atribute psihometrice – *awareness*, *conscientiousness*, *stress*, *neuroticism* și *risk_tolerance* – se bazează pe relevanța lor în contextul securității cibernetice, unde factorii umani joacă un rol critic în prevenirea și gestionarea incidentelor. Metodele de extragere prezentate (ModelExtractor, PromptExtractor și AzureExtractor) oferă abordări complementare, fiecare având propriile avantaje și limitări, și permit astfel o evaluare robustă și flexibilă a profilului psihometric al utilizatorilor.

Această soluție modulară și integrată este fundamentată pe principii și tehnici recunoscute în literatura de specialitate și oferă un cadru scalabil pentru monitorizarea și managementul riscurilor din cybersecurity. În viitor, îmbunătățirile pot include integrarea metodelor de tip Graph Neural Networks și optimizarea tehnicilor de prompt engineering, pentru a obține o performanță și o acuratețe sporită.

---

## 6. Referințe

1. **Devlin, J., Chang, M. W., Lee, K., & Toutanova, K. (2018).** BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding. *arXiv preprint arXiv:1810.04805*.
2. **Wolf, T., et al. (2020).** Transformers: State-of-the-Art Natural Language Processing. *Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing: System Demonstrations*.
3. **Bishop, C. M. (2006).** Pattern Recognition and Machine Learning. Springer.
4. **Stajano, F., & Wilson, P. (2006).** Cyber Security: A Matter of Trust. *IEEE Security & Privacy*.
5. Diverse studii în psihologia organizațională privind influența factorilor psihologici (conștiinciozitate, neuroticism, etc.) asupra comportamentului în mediile de risc.

---

## 7. State of the Art

https://arxiv.org/abs/2403.07581

https://huggingface.co/Minej/bert-base-personality#:~:text=Extroversion%3A%20A%20value%20between%200,representing%20the%20predicted%20openness%20trait

https://www.sciencedirect.com/science/article/abs/pii/S0191886916308418#:~:text=analysis%20www,negative%20emotion%20words%20and

https://arxiv.org/html/2407.05943v1#:~:text=%E2%80%9Ctraits%E2%80%9D%20considered%20in%20the%20literature,others%20belong%20to%20the%20agreeableness