# canvas_dashboard
## Inleiding
Deze Python modules genereren een set van statische html-pagina's op basis van gegevens uit Canvas. De basis zijn de Canvas opdrachten (Assignments).
# De workflow
Er wordt gebruik gemaakt van verschillende stappen om dat het dashboeard te komen.
## Stap 1
start met:
`course_config_start.json`
Hier worden drie attributen in JSON formaat opgegeven:
```json 
{
  "api_key": "api_key from Canvas",
  "course_id": 32666,
  "config_file_name": "course_config_inno.json"
}
```
De bestandsnaam is de output van het programma `generate_config.py`. De Canvas API wordt aangeroepen om de structuur van Canvas uit te lezen.
- Opdrachtgroepen (AssignmentGroups)
- Projectgroepen 
- Canvas secties (Sections)
- Docenten (Users)
Dit bestand is ook weer een JSON-bestand met bovengenoemede groepen.
## Stap 2
Het `course_config_inno.json` bestand moet verrijkt worden met extra gegevens en logica.
### Roles
Verwijder de niet relevante `role`.
### Teachers
Hier worden de projecten aan de docenten gekoppeld. Projecten hebben een `id` vanuit Canvas meegekregen, deze worden in de lijst toegevoegd per docent.


De volgende stap is de resultaten uitlezen uit Canvas. Er wordt intensief gebruik gemaakt van de Canvas-API.