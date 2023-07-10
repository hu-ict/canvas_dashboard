# canvas_dashboard
## Inleiding
Deze Python modules genereren een set van statische html-pagina's op basis van gegevens uit Canvas. De basis zijn de Canvas opdrachten (Assignments).
# De workflow
Er wordt gebruik gemaakt van verschillende stappen om dat het dashboard te komen.
## Stap 1
start met:
`start.json`
Hier worden attributen in JSON formaat opgegeven:
```json 
{
  "api_key": "api_key from Canvas",
  "course_id": 39872,
  "projects_groep_name": "Project Groups",
  "slb_groep_name": "SLB Groep",
  "peil_perspective": "peil",
  "config_file_name": "config_sep23.json",
  "course_file_name": "course_sep23.json",
  "results_file_name": "results_sep23.json",
  "start_date": "2023-09-04T00:00:00Z",
  "end_date": "2024-02-02T23:59:59Z",
  "perspectives": [
    {
      "name": "team",
    },
    {
      "name": "gilde",
    },
    {
      "name": "kennis",
    },
    {
      "name": "peil",
    }
  ]

}
```
## Stap 2
Door het uitvoeren van het Python script `generate_config.py`. De Canvas API wordt aangeroepen om de structuur van Canvas uit te lezen.
- Opdrachtgroepen (AssignmentGroups)
- Projectgroepen 
- Canvas secties (Sections)
- Docenten (Users)
Verder worden de attributen aangemaakt:
- Perspectiven
- Rollen
Dit bestand is ook weer een JSON-bestand met de naam `config_file_name` uit `start.json`
## Stap 3
Het `config_file_name` bestand moet verrijkt worden met extra gegevens en logica.
### Secties
Verwijder de niet relevante `secties`.
### Teachers
Hier worden de projecten en assignment_groups aan de docenten gekoppeld. 
- Projecten hebben een `id` vanuit Canvas meegekregen, deze worden in de lijst toegevoegd per docent.
- assignment_groups hebben ook een `id` vanuit Canvas meegekregen, deze worden in de lijst toegevoegd per docent.

De volgende stap is de resultaten uitlezen uit Canvas. Er wordt intensief gebruik gemaakt van de Canvas-API.
