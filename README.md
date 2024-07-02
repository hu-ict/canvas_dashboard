# canvas_dashboard
# Inleiding
Deze Python modules genereren een set van statische html-pagina's op basis van gegevens uit Canvas. De basis zijn de Canvas opdrachten (Assignments). 
# De workflow
Er wordt gebruik gemaakt van verschillende stappen om tot het dashboard te komen.
![Activity Diagram](dashboard.png)
## Stap 1 - Genereren nieuwe instance (tenant)
Om een nieuwe course omgeving te maken:
- run het Python script `generate_start.py`
Gebruik wordt gemaakt van het `course_instances.json`. Als dit bestand nog niet bestaat wordt deze gemaakt in de directory `.\courses`

Er wordt gevraagd naar een naam van de `instance` bijvoorbeeld `inno-sep24`. De `category` moet opgegeven worden, bijvoorbeeld `inno_courses`. Geef ook het `canvas_course_id` op.
Hier worden attributen in JSON formaat opgegeven:
```json 
{
  "api_key": "api_key from Canvas",
  "canvas_course_id": 39869,
  "grade_levels": "grade",
  "projects_groep_name": "Project Groups",
  "slb_groep_name": "SLB Groep",
  "start_date": "2024-02-12T00:00:00Z",
  "end_date": "2024-07-12T23:59:59Z",
  "progress": {
      "name": "progress",
      "levels": "progress",
      "show_points": true,
      "assignment_groups": [
      ]
  },
  "attendance_perspective": "",
  "template_path": ".//courses//feb24_inno//templates//",
  "target_path": "C://Users//berend.wilkens//OneDrive - Stichting Hogeschool Utrecht//General//dashboard//",
  "target_slb_path": "C://Users//berend.wilkens//Stichting Hogeschool Utrecht//INNO - SLB - General//INNO dashboard - SLB//",
  "config_file_name": ".//courses//feb24_inno//config_feb24_inno.json",
  "course_file_name": ".//courses//feb24_inno//course_feb24_inno.json",
  "results_file_name": ".//courses//feb24_inno//result_feb24_inno.json",
  "progress_file_name": ".//courses//feb24_inno//progress_feb24_inno.json",
  "workload_file_name": ".//courses//feb24_inno//workload_feb24_inno.json",
  "attendance_report": ".//courses//feb24_inno//attendance_report.csv",
  "perspectives": {
    "team": {
      "name": "team",
      "levels": "samen",
      "show_points": false
    },
    "gilde": {
      "name": "gilde",
      "levels": "samen5",
      "show_points": false
    },
    "kennis": {
      "name": "kennis",
      "levels": "niveau",
      "show_points": true
    }
  },
  "roles": [
    {
      "short": "AI",
      "name": "AI - Engineer",
      "btn_color": "btn-warning",
      "assignment_groups": [],
      "students": []
    },
    {
      "short": "BIM",
      "name": "Business Analist",
      "btn_color": "btn-success",
      "assignment_groups": [],
      "students": []
    },
    {
      "short": "CSC-C",
      "name": "Cloud",
      "btn_color": "btn-danger",
      "assignment_groups": [],
      "students": []
    },
    {
      "short": "CSC_S",
      "name": "Security",
      "btn_color": "btn-danger",
      "assignment_groups": [],
      "students": []
    },
    {
      "short": "SD_B",
      "name": "Back-end developer",
      "btn_color": "btn-dark",
      "assignment_groups": [],
      "students": []
    },
    {
      "short": "SD_F",
      "name": "Front-end developer",
      "btn_color": "btn-primary",
      "assignment_groups": [],
      "students": []
    },
    {
      "short": "TI",
      "name": "Embedded - Engineer",
      "btn_color": "btn-info",
      "assignment_groups": [],
      "students": []
    }
  ]
}
```
## Stap 2 - Aanpassen start.json
Ontwerp de perspectieven en rollen door de `start.json` aan te passen.
## Stap 3 - Genereren configuratie
Door het uitvoeren van het Python script `generate_config.py`. De Canvas API wordt aangeroepen om de structuur van Canvas uit te lezen.
- Canvas secties (Sections)
- Opdrachtgroepen (AssignmentGroups)
- Projectgroepen (
- Docenten (Users)

Verder worden de attributen aangemaakt (gekopieerd uit `start.json`):
- Perspectiven
- Rollen
  
Dit bestand is ook weer een JSON-bestand met de naam `config_file_name` uit `start.json`
## Stap 4a - Verrijken config perspectieven
Het `config_file_name` bestand moet verrijkt worden met extra gegevens en logica.
### Perspectives
- Verwijder de niet relevante `perspectives` of voeg er toe.
- Bepaal welke `levels` gebruikt worden, dit is een koppeling met de niveaus in het `labels_colors.json` bestand.
- Bepaal of er punten getoond moeten worden met `show_points` in het dashboard.
- `assignment_group` heeft een `id` vanuit Canvas meegekregen, deze worden in de lijst toegevoegd per `perspective`.
```
"perspectives": {
  "team": {
  "name": "team",
  "levels": "samen",
  "show_points": false,
  "show_flow: true,
  "assignment_groups": [73974]
},
"gilde": {
  "name": "gilde",
  "levels": "samen5",
  "show_points": false,
  "show_flow: true,
  "assignment_groups": [73983]
},
"kennis": {
  "name": "kennis",
  "levels": "niveau",
  "show_points": true,
  "show_flow: true,
  "assignment_groups": [73113]
}

```
### AssignmentGroups
- Verwijder de niet relevante `assignment_group`.
- controlleer de `total_points`
- vul de `lower_points` en de `upper_points` voor de bandbreedte (onder niveau en boven niveau)
  `teachers`, `roles` en `assignments` wordt later automatisch gevuld,
```
"strategy": "EXP_POINTS",
"upper_c": 4,
"lower_c": -1,
"total_points": 89,
"lower_points": 44,
"upper_points": 56,
```
- `strategy` kent meerdere opties: `NONE`, `EXP_POINTS`, `LIN_POINTS`, `POINTS`, `LINEAIR`, `EXPONENTIAL`, `CONSTANT`, `FIXED`, `ATTENDANCE`.
### Strategy
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

## Stap 4b Verrijken groepen, rollen en docenten
### Roles
- Verwijder de niet relevante `roles`.

Het id van de `assignment_groups` binnen de rollen vullen:
```
    {
      "short": "AI",
      "name": "AI - Engineer",
      "btn_color": "btn-warning",
      "assignment_groups": [62149]
    },
```
### Secties
Secties worden gebruikt voor de rol van een student of de klas- waarin de student zit.
- Verwijder de niet relevante `secties`.
- Verrijk een sectie met de `role`, dit is de short name van de `role` uit de `roles` lijst in deze json.
### Teachers
- Verwijder de niet relevante `teachers`.
Hier worden de `projects` en `assignment_groups` aan de `teachers` gekoppeld. 
- `projects` hebben een `id` vanuit Canvas meegekregen, deze worden in de lijst toegevoegd per `teacher`.
- `assignment_groups` hebben ook een `id` vanuit Canvas meegekregen, deze worden in de lijst toegevoegd per `teacher`.
## Stap 5 - Lees assignments
Door het uitvoeren van het Python script `generate_course.py` wordt het json bestand `course_file_name` gemaakt. De assignments worden gelezen en aan het perspectief gekoppeld. De bandbreedte  (onder, op en boven niveau) wordt bepaald door de `strategy`. Stap 4a moet uitgevoerd zijn.
## Stap 6 - Lees studenten
Studenten worden uit Canvas gelezen. De project groepen en rollen worden gevuld. Docenten worden aan de juiste groepen gekoppeld. Start daarvoor het script: `generate_student.py`. Stap 4a, 4b en 5 moeten uitgevoerd zijn.

Wanneer de structuur van studenten en assigments niet wijzigd kunnen bij een snapshot stap 1 tm 6 overgeslagen worden.
## Stap 7 - Resultaten
De volgende stap is de resultaten/submissions uitlezen uit Canvas. Er wordt intensief gebruik gemaakt van de Canvas-API. Hier zijn twee varianten beschikbaar:
- `generate_results.py`
- `generate_submissions.py`

Als met attendance gewerkt wordt wordt het csv bestand ingelezen en gekoppeld aan het juiste perspectief. De voortgang wordt ook bepaald.
## Stap 8 - Dashboard
Genereer de visuals:
- `generate_plotly.py`
- `generate_dashboard.py`
## Stap 9 - Publiceren
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

Het `team_id` wordt verkregen met de GraphQL MSTeams interface. De `team_id`s worden in de lijst boven in het schript toegevoegd.
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

