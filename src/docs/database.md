# Introductie

## db_context.py

### context() en db_contex()

Deze functie maakt een databaseverbinding op basis van de omgevingsvariabelen die zijn opgeslagen in Azure. Het is de
centrale methode voor het tot stand brengen van een verbinding met de database.

### execute_query()

Deze functies zijn verantwoordelijk voor het tot stand brengen en beheren van verbindingen met de database, gebaseerd op
omgevingsvariabelen die zijn opgeslagen in Azure. Ze zijn essentieel voor een veilige en efficiënte interactie met de
database.

De context()-functie maakt een directe databaseverbinding en retourneert een cursor en connection. Deze worden gebruikt
om SQL-query’s uit te voeren en transacties af te handelen. Het is een fundamentele functie die overal in de applicatie
kan worden gebruikt waar een databaseverbinding nodig is.

De db_context()-functie bouwt voort op context() en biedt een contextmanager (met het with-statement) voor een
eenvoudiger beheer van de levenscyclus van databaseverbindingen. Het zorgt ervoor dat resources zoals de cursor en
connection automatisch worden vrijgegeven, zelfs bij fouten. Dit maakt het een veilige en elegante manier om met de
database te werken.

### Use Cases

- Wanneer de applicatie toegang tot de
  database nodig heeft, gebruikt deze functie de opgehaalde cursor en connection om efficiënt met de database te
  communiceren. Zowel de cursor als de verbinding worden geretourneerd voor verder gebruik in query-uitvoering of
  transacties.

## generate_data.py

### initialize_db

e initialize_db-functie zorgt ervoor dat de benodigde database-tabellen worden aangemaakt, maar alleen als deze nog niet
bestaan. Als de tabellen al aanwezig zijn in de database, gebeurt er niets en wordt er geen wijziging aangebracht. Deze
tabellen worden gebruikt om gegevens over studenten, docenten, cursussen en hun onderlinge relaties op te slaan.
Hierdoor wordt een gestructureerde en robuuste database-infrastructuur opgezet zonder onnodige duplicatie.

#### Entiteiten

1. **students**  
   Opslag van gegevens over studenten.
    - **id**: *Uniek identificatienummer* van de student (**primair sleutel**).
    - **first_name**: *Voornaam* van de student.
    - **surname**: *Achternaam* van de student.
    - **email**: *Unieke e-mail* van de student.

2. **courses**  
   Opslag van gegevens over cursussen.
    - **id**: *Uniek identificatienummer* van de cursus (**primair sleutel**).
    - **name**: *Naam* van de cursus.
    - **directory_name**: *Naam van de map* waarin de cursusgegevens zijn opgeslagen.

3. **teachers**  
   Opslag van gegevens over docenten.
    - **id**: *Uniek identificatienummer* van de docent (**primair sleutel**).
    - **first_name**: *Voornaam* van de docent.
    - **surname**: *Achternaam* van de docent.
    - **email**: *Unieke e-mail* van de docent.

4. **teacher_courses**  
   Relatietabel die docenten koppelt aan hun cursussen.
    - **teacher_id**: *Verwijzing naar het id* van een docent (*foreign key naar `teachers`*).
    - **course_id**: *Verwijzing naar het id* van een cursus (*foreign key naar `courses`*).
    - **PRIMARY KEY**: Gecombineerd uit **teacher_id** en **course_id**.

5. **student_courses**  
   Relatietabel die studenten koppelt aan hun cursussen.
    - **student_id**: *Verwijzing naar het id* van een student (*foreign key naar `students`*).
    - **course_id**: *Verwijzing naar het id* van een cursus (*foreign key naar `courses`*).
    - **PRIMARY KEY**: Gecombineerd uit **student_id** en **course_id**.

6. **logs**  
   Opslag van logboekgegevens voor het bijhouden van gebeurtenissen en statusupdates bij cursus events
    - **id**: *Uniek identificatienummer* voor elke logregel (**primair sleutel**).
    - **course_instance**: *Naam of ID* van de cursusinstantie waarop het log betrekking heeft.
    - **event**: Beschrijving van het *type gebeurtenis*.
    - **status**: *Status* van de gebeurtenis (bijv. “success”, “failure”).
    - **timestamp**: *Tijdstempel* van wanneer de gebeurtenis heeft plaatsgevonden (*standaard huidige tijd*).

#### Use cases

- Deze functie wordt op de achtergrond aangeroepen wanneer een cursus wordt aangemaakt of geüpdatet via het admin
  dashboard. Dit gebeurt door middel van een route die is gedefinieerd in `routes.py`.
- functie wordt ook op de achtergrond uitgevoerd wanneer een cursus wordt aangemaakt of geüpdatet via Power Automate en
  de NiFi-endpoints. Dit proces maakt eveneens gebruik van een route in `routes.py`.

### insert_*()

Deze functies voegen gegevens toe aan de bijbehorende tabellen in de database:
• insert_student: Voegt een student toe aan de database als deze nog niet bestaat.
• insert_teacher: Voegt een docent toe aan de database als deze nog niet bestaat.
• insert_course: Registreert een nieuwe cursus in de database.
• insert_student_course_relation: Legt een relatie vast tussen een student en een cursus.
• insert_teacher_course_relation: Legt een relatie vast tussen een docent en een cursus.
• insert_log: Voegt logs toe voor elk cursus event in `routes.py`

### read_and_import_course()

De functie read_and_import_courses importeert cursus-, student- en docentgegevens vanuit vooraf gegenereerde
JSON-bestanden in de database. Het proces omvat de volgende kernactiviteiten:
• Controleert of de map met cursusgegevens (courses) correct is ingesteld en toegankelijk.
• Doorloopt de beschikbare cursussen in de courses-map en leest de JSON-bestanden:
• result_{course_name}.json: Bevat cursusinformatie en gekoppelde studenten.
• config_{course_name}.json: Bevat docenteninformatie die aan de cursus is gekoppeld.
• Voegt cursusinformatie toe aan de database.
• Importeert studenten die aan de cursus zijn gekoppeld en legt hun gegevens en relaties met de cursus vast in de
database.
• Importeert docenten die aan de cursus zijn gekoppeld en legt hun gegevens en relaties met de cursus vast in de
database.
• Verwerkt alle gegevens en commit de wijzigingen naar de database.

Deze functie biedt een proces om cursusgegevens uit Canvas inclusief gerelateerde studenten en
docenten te lezen en te . Het legt bovendien de onderlinge relaties vast, waardoor de database compleet en
consistent blijft.

#### Use cases

- Deze functie wordt op de achtergrond aangeroepen wanneer een cursus wordt aangemaakt of geüpdatet via het admin
  dashboard. Dit gebeurt door middel van een route die is gedefinieerd in `routes.py`.
- functie wordt ook op de achtergrond uitgevoerd wanneer een cursus wordt aangemaakt of geüpdatet via Power Automate en
  de NiFi-endpoints. Dit proces maakt eveneens gebruik van een route in `routes.py`.

## course_data.py

Dit bestand bevat een reeks zoekfuncties die worden gebruikt om, na het inloggen van een student of docent, te bepalen
welk dashboard (student of docent) moet worden weergegeven voor een specifieke cursus. Hierbij worden databasequery’s
uitgevoerd om relevante gegevens op te halen, zoals cursussen waaraan de gebruiker is gekoppeld. Deze functionaliteit
zorgt ervoor dat de juiste inhoud en opties worden getoond, afgestemd op de rol en betrokkenheid van de gebruiker.

## dashboards.py

Dit bestand bevat functies om dashboards van studenten te vinden, zowel lokaal als in de blob storage. 