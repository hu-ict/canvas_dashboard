# canvas_dashboard
# Inleiding
Deze Python modules genereren een set van statische html-pagina's op basis van gegevens uit Canvas. De basis zijn de Canvas opdrachten (Assignments). 
# De workflow
Er wordt gebruik gemaakt van verschillende stappen om tot het dashboard te komen.
# Stap 1 - Nieuwe omgeving
Om een geheel nieuwe omgeving te maken op je persoonlijke computer/laptop run het Python script `generate_environment.py`. Er wordt gevraagd om je persoonlijk `Canvas-Api_Key`. Deze sleutel wordt opgeslagen het bestand `msteams_api.json` binnen de map `environment`. Deze sleutel is zeer persoonlijk en moet dus niet gaan rondslingeren. Het bestand `environment.json` wordt ook hier aangemaakt. Daarnaast wordt de directory `.\courses` gemaakt.
# Stap 2 - Nieuwe cursus
Aanmaken van een nieuwe cursus, bijvoorbeeld `TICT-V1SE1-24` of `TICT-V3SE6-25`. Dit is nog niet de cursus instantie. Om een nieuwe cursus omgeving te maken, run het Python script `generate_new_course.py`. Er wordt contact gezocht met Canvas om AssignmentGroups op te halen en te vragen of deze relevant zijn voor het portfolio. Er wordt nu een `dashboard.json` gemaakt en de bijbehorende cursus map. In het bestand zijn wat standaard zaken in geregeld, maar er moet goed naar gekeken worden of de verschillenda attributen goed staan. In dit bestand staat de basale structuur van het portfolio in de cursus. Je kan dit bestand ook kopiëren van een collega.
## Attributen `dashboard.json`
### `dashboard_tabs`
### `groups_1`
### `groups_2`
### `assignment_groups`
### `perspectives`
### `level_moments`
### `grade_moments`
### `learning_outcomes`

# Stap 3 - Nieuwe cursus instantie
Om een nieuwe cursus omgeving te maken, run het Python script `generate_new_course_instance.py`. 
- Er wordt aangevraagd onder welke cursus deze instantie valt.
- Daarna een naam voor de instantie gervraagd, bijvoorbeeld: `TICT-V1SE1-24_feb26` of `TICT-V3SE6-25_feb26`. 
- Geef ook de periode aan, bijvoorbeeld `feb26`.
- Canvas ID wordt gevraagd.
- De relevantie van de secties wordt aangegeven door een vraag uit het systeem.
- Er wordt een copy van `dashboard.json` gemaakt in de aangemaakte map van de instantie met de naam van de instantie.
# Stap 4 - Configuratie opzetten
Door het uitvoeren van het Python script `generate_config.py`. De Canvas API wordt aangeroepen om de structuur van Canvas uit te lezen.
- Canvas secties (Sections)
- Opdrachtgroepen (AssignmentGroups)
- Projectgroepen (
- Docenten (Users)
Verder worden de attributen aangemaakt (gekopieerd uit `dashboard.json`) en gegenereerd uit de (template) code op basis van de instance category:
- Perspectiven
- Rollen
Dit bestand is ook weer een JSON-bestand met de naam `config_[instance].json` uit op basis van de `instance_name`.
Daarnaast wordt een excel bestand gegeneerd (`trm_[instance].xlsx`) om de docenten makkelijk en overzichtelijk aan groepen te koppelen. Dit bestand volgens de wensen aanpassen en opslaan.
## Stap 5 Docent verantwoordelijkheden importeren
Het `config.json` bestand moet verrijkt worden met de docent verantwoordelijkheden. Dit wordt gedaan met het Python script `read_trm.py`. Niet relevante `teachers` worden verwijderd.

In principe is de configuratie van een nieuwe instantie klaar.

# Toelichting op de attributen in `config_[instance].json`.
## principal_assignment_group_id
Dit attribuut welke docent de verantwoordelijke is van een `student_group` op basis van de `assignment_group`.
```json
"principal_assignment_group_id": 0,
```
## sections
- Verwijder de niet relevante `section` elementen.
## attendance
```
"attendance": {
"name": "attendance",
"title": "Aanwezigheid",
"levels": "attendance",
"show_points": true,
"show_flow": false,
"strategy": "ATTENDANCE",
"total_points": 100,
"lower_points": 75,
"upper_points": 90,
"policy": {
  "starting_days": [
    1
  ],
  "recurring": "WEEKLY",
  "times": 20,
  "exceptions": [
    3,
    12,
    19,
    20
  ]
},
```
## level_moments
```
  "level_moments": {
    "name": "level_moments",
    "title": "Peilmomenten",
    "levels": "progress",
    "moments": [
      "Peilmoment 1",
      "Peilmoment 2"
    ],
    "assignment_groups": []
  },
```
## grade_moments
```
  "grade_moments": {
    "name": "grade_moments",
    "title": "Beoordelingsmomenten",
    "levels": "grade",
    "moments": [
      "Beoordeling"
    ],
    "assignment_groups": []
  },
```
### perspectives
- Verwijder de niet relevante `perspective` elementen of voeg er toe.
```
"portfolio": {
  "name": "portfolio",
  "title": "Portfolio",
  "show_points": false,
  "show_flow": true,
  "total_points": 0,
  "assignment_group_ids": [],
  "assignment_sequences": [],
  "bandwidth": {
    "points": []
  }
}
```
- Bepaal of er punten getoond moeten worden met `show_points` in het dashboard en of de voortgang als `show_flow` wordt getoond.
- Elke `assignment_group` onder in de json heeft een `id` vanuit Canvas meegekregen, deze worden in de lijst aan het element `assignment_group_ids`.
- Het attribuut `total_points` en de elementen `assignment_sequences` en `bandwidth` worden later bepaald in het script `generate_course.py`.
## learning_outcomes
## roles
- Verwijder de niet relevante `roles`.
Het id van de `assignment_groups` binnen de rollen vullen idien relevant:
```
{
  "short": "AI",
  "name": "AI - Engineer",
  "btn_color": "btn-warning",
  "assignment_groups": [62149]
},
```
## teachers
- Verwijder de niet relevante `teacher` elementen.
## assignment_groups
- Verwijder de niet relevante `assignment_group` elementen.
```
{
  "name": "Project",
  "id": 92883,
  "groups": "project",
  "role": "Iedereen",
  "strategy": "EXP_POINTS",
  "lower_c": 1,
  "upper_c": 7,
  "total_points": 114.0,
  "lower_points": 58,
  "upper_points": 74,
  "levels": "samen",
  "assignment_sequences": [],
  "bandwidth": []
}
```
- Vul de `lower_points` en de `upper_points` voor de bandbreedte (onder niveau en boven niveau). Indien nodig ook `lower_c` en `up
- Het elementen `total_points`, `bandwidth` en `assignment_sequences` wordt later automatisch gevuld door het scrip `generate_course.py`,

Binnen een `assignment_group` hebben we `assignments`, deze kunnen gebudeld worden d.m.v. `assignment_sequence`. Dit wordt gebundeld op basis van een hashtag in de opdracht naam.
### 
- `strategy` kent meerdere opties: `NONE`, `EXP_POINTS`, `LIN_POINTS`, `POINTS`, `LINEAIR`, `EXPONENTIAL`, `CONSTANT`, `FIXED`, `ATTENDANCE`.

De strategiën `EXP_POINTS`, `LIN_POINTS`, `POINTS` en `CONSTANT` worden het meest gebruikt. De strategie `ATTENDANCE` lijkt veel op `CONSTANT`.

Met de constanten `lower_points` en `upper_points` worden de einddoelen van de onderwijseenheid bepaald. Wanneer de student onder `lower_points` scoort heeft de student niet het verwachtte niveau en zal het perspectief niet halen. Wanneer de student boven `upper_points` scoort gaat deze het boven niveau het perspectief afronden. Daar tussen in wordt het op niveau. Deze einddoelen worden volgens een bepaalde strategie terug geinterpoleerd, daardoor ontstaat er een bandbreedte in de tijd.

De volgende formule wordt gebruikt bij de strategy `EXP_POINTS` en `EXPONENTIAL`
```
y = ax2 + bx + c
```
- y: opgebouwde waarde
- x: tijd
- a: groeipotentieel of leervermogen
- b: wat je al geleerd hebt en opnieuw laat zien
- c: initieel zichtbaar

De constande a, b, en c hebben een waarde groter dan 0.

Bij de strategy `CONSTANT` is de waarde constant in de tijd. De constanten a en b zijn nul en de constante c wordt gelijkgesteld aan `lower_points` en `uppper_points`.

Bij `POINTS` wordt de bandbreedte bepaald hoeveel punten er voor elk portfolio-item gehaald kan worden. Minder dan 55% in onder bandbreedte en boven 80% boven bandbreedte en dit cummulatief in de tijd. 


### sections
Secties worden gebruikt voor de rol van een student of de klas- waarin de student zit.
- Verwijder de niet relevante `secties`.
- Verrijk een sectie met de `role`, dit is de short name van de `role` uit de `roles` lijst in deze json.
### teachers
- Verwijder de niet relevante `teachers`.
Hier worden de `projects` en `assignment_groups` aan de `teachers` gekoppeld. 
- `projects` hebben een `id` vanuit Canvas meegekregen, deze worden in de lijst toegevoegd per `teacher`. Als alternatief en makkelijker optie is om een uniek deel uit de naam van de project_group mee te geven. Bijvoorbeeld de klascode (PROP) `V1A`.
- `assignment_groups` hebben ook een `id` vanuit Canvas meegekregen, deze worden in de lijst toegevoegd per `teacher`. Optioneel
### groups_1
Deze zijn al opgehaald uit Canvas. De volgende attributen moeten gevuld worden:
nog aanvullen
### groups_2
Deze zijn al opgehaald uit Canvas. De volgende attributen moeten gevuld worden:
nog aanvullen

## Stap 4 - upload config
De configuratie is nu klaar, deze wordt in de `config-dot-json` Canvas pagina geplaatst. De configuratie wijzigd zeer weinig tijdens het lopen van de cursus.

# Stap A Extraheren data uit Canvas
De stap maakt gebruik van de `Canvas-Api_Key`. Alle communicatie met Canvas wordt uitgevoerd. Er wordt alleen gelezen. In het script `run_env_2.py` voert twee subscripts uit:
- `generate_course(course_instance)`
- `generate_results(course_instance)`
De eerste is nodig op wijzigingen in opdrachten en studentgroepen opnieuw te importeren. De assignments worden gelezen en aan het perspectief gekoppeld. De bandbreedte (onder, op en boven niveau) wordt bepaald door de `strategy`. Studenten worden gelezen. De project groepen en rollen worden gevuld. Docenten worden aan de juiste groepen gekoppeld. Studenten die de cursus nog niet geaccepteerd hebben worden wél meegenomen in de studentenlijst, maar hebben nog geen login naam (email) in Canvas. Wanneer de structuur en inhoud van studenten en assignments niet wijzigd kunnen bij een snapshot stap 5 en 6 overgeslagen worden.Dit levert het bestand 'course_[instance].json` op. Het tweede script leest alle resulten uit Canvas en produceert het 'results_[instance].json` bestand.
Als met attendance gewerkt wordt wordt het csv bestand ingelezen en gekoppeld aan het juiste perspectief. De voortgang wordt ook bepaald. Op basis van de parameters `Attendance` en `Geldidge reden` worden punten toegekend.
- `absent` 0 punten afwezig (geen geldige reden)
- `absent` 1 punt afwezig (geldige reden)
- `late` 1 punt te laat (geen geldige reden)
- `late` 2 punten te laat (geldige reden)
- `present` 2 punten aanwezig
# Stap B Genereren HTML en Plotly
## Stap B1 - Dashboard
Genereer het docenten overzicht
- `generate_dashboard.py`
Genereer de overzichten van de studenten:
- `generate_plotly.py`
- `generate_dashboard.py`
## Stap B2 - Publiceren
Kopieer files naar de teams oneDrive voor docenten
- `publish_dashboard.py`
Kopieeer de JPG en HTML naar het private channel van de student
- `publish_student_files.py`
Bovenstaande stappen kunnen ook gemodelleerd worden met de 
- `runner.py`
# Werken met MSTeams kanalen
## Stap 1 Aanmaken teams
Aanmaken teams in MSTeams. Je hebt voor elke max 30 studenten een team nodig.
## Stap 2 Aanmaken kanalen
Privé kanalen worden aangemaakt binnen een bestaand team. Er geldt een maximum van 30 privékanalen in ieder team. Het script:
- `generate_channels.py`

Het `team_id` wordt verkregen met de GraphQL MSTeams interface. De `team_id`s worden in de lijst boven in het script toegevoegd.
- `teams = ["b7cf78ae-8c6f-460d-a47a-d4bc2b8b2f18"]`

De lijst van studenten wordt uit `course.json` gehaald.

Dit script maakt een privékanaal en en voegt de de gebruiker (student) toe aan het team én het kanaal. Het json `msteams_api.json` bestand wordt gebruikt voor het opslaan en uitlezen van de api_keys. De api_key verloopt binnen een dag. Ik werk met een update van de key via de Graph Explorer. De api_key wordt in het api bestand gezet onder `gen_token`.

Als je de naam van de `student_group` als `team_name` wilt gebruiken moet je het script aanpassen.
## Stap 3 Uilezen kanaal UID
Met het volgende script worden de id's van de kanalen gekoppeld aan de studenten in de `course.json`. Het json `msteams_api.json` bestand wordt gebruikt voor het opslaan en uitlezen van de api_keys.
- `update_sites.py`

De api_key verloopt binnen een dag. Ik werk met een update van de key via de Graph Explorer. De api_key wordt handmatig in het api bestand gezet `my_token`.
## Stap 4 Kopieren bestanden
- `publish_student_files.py`

Kopieert de bestanden (html en jpg) naar het teamskanaal. Het json `msteams_api.json` bestand wordt gebruikt voor het opslaan en uitlezen van de api_keys. De api_key verloopt binnen een dag. Ik werk met een update van de key via de Graph Explorer. De api_key wordt handmatig in het api bestand gezet `my_token`.

