Projectdocumentatie - INNO Dashboard

Dit project bevat een INNO Dashboard voor zowel studenten 
als docenten. De applicatie maakt gebruik van Flask voor de backend en Keycloak 
voor authenticatie. Hieronder vind je een overzicht van de belangrijkste onderdelen en functionaliteiten binnen de applicatie.

Inhoudsopgave

Bestandstructuur
Hoofdapplicatie - app.py
Authenticatie - auth.py
Routes - routes.py
Frontend - index.html, CSS en JS

.
├── app.py                 # Hoofdapplicatie bestand
├── auth.py                # Authenticatie logica en Keycloak-integratie
├── routes.py              # Hoofdapplicatieroutes voor student- en docentdashboards
├── static                 # Frontend bestanden
│   ├── css
│   │   └── login.css      # Stijlen voor de loginpagina
│   ├── images
│   │   └── hu-logo.svg    # Logo van de Hogeschool Utrecht
│   └── js
│       └── login.js       # JavaScript voor login-interacties
└── templates
    └── login
        └── index.html     # HTML-bestand voor de loginpagina


Hoofdapplicatie - app.py
Het bestand app.py bevat de configuratie en initiële opzet van de Flask-applicatie. Dit bestand doet het volgende:

Initialiseert de Flask-applicatie.
Verwijst de hoofdroutes door naar routes.py.
Registreert de authenticatiefunctionaliteit via een blueprint vanuit auth.py.
Start de server op poort 5101 in debugmodus.
Belangrijkste functies en instellingen:

create_app(): Deze functie maakt en configureert de Flask-applicatie en registreert de blueprints.
if __name__ == '__main__':: Hiermee wordt de applicatie opgestart als het bestand direct wordt uitgevoerd.
Authenticatie - auth.py
Dit bestand bevat de authenticatielogica en Keycloak-integratie. Hierin worden functies gedefinieerd voor:

Loginverwerking (login()): Authenticeert de gebruiker via Keycloak. Bij succesvolle login wordt een token opgehaald en opgeslagen in de sessie.
Loginpagina (login_page()): Laadt de loginpagina vanuit de templates-directory.
Loginvereiste Decorator (login_required): Controleert of de gebruiker is ingelogd; anders wordt een foutmelding weergegeven.
Rolgebaseerde Decorator (role_required): Zorgt ervoor dat de gebruiker de vereiste rol heeft (bijvoorbeeld teachers of students).
Deze decorators worden gebruikt binnen routes.py om toegang te beperken tot specifieke dashboardroutes voor studenten en docenten.

Routes - routes.py
Het bestand routes.py bevat de hoofdroutes van de applicatie en definieert welke inhoud wordt weergegeven op basis van de gebruikerstoegang.

Belangrijkste routes:

/ (Hoofdpagina):
Controleert of de gebruiker is ingelogd en verwijst door naar /teacher_dashboard voor docenten of /student_dashboard voor studenten.
/teacher_dashboard (Docentendashboard):
Toont het volledige dashboard voor docenten door de juiste HTML-inhoud vanuit de courses-directory te laden.
Gebruikt glob om de juiste map met de vereiste bestanden te vinden en laadt index.html voor weergave.
/student_dashboard (Studentendashboard):
Toont een welkomstboodschap met de naam van de student. Hier worden de gegevens uit de JWT-token gehaald om de naam van de ingelogde student te tonen.
Statische bestanden (/css/<filename>, /js/<filename>):
Deze routes zorgen ervoor dat CSS- en JavaScript-bestanden correct worden geladen.
Dashboardroute (dashboard):

Deze route (/dashboard) controleert of de gebruiker een geldige autorisatieheader heeft en geeft op basis van de rol de juiste JSON-respons (docent of student).
Frontend - index.html, CSS en JS
Het frontend bestaat uit de volgende onderdelen:

HTML (index.html): Loginpagina en formulier voor het invoeren van gebruikersnaam en wachtwoord. Gebruikt een button om in te loggen.
CSS (login.css): Stijlt de loginpagina, inclusief formuliervelden en knoppen.
JavaScript (login.js): Verwerkt de loginfunctionaliteit en communiceert met de backend via een POST-verzoek naar /auth/login.
login.js:

Wanneer de gebruiker op de knop "Inloggen" klikt, wordt een POST-verzoek verzonden met de inloggegevens.
Bij succesvolle login worden tokens opgeslagen in localStorage, en wordt de gebruiker doorgestuurd naar /teacher_dashboard of /student_dashboard, afhankelijk van de geretourneerde rol.

Keycloak wordt gebruikt om gebruikers te authenticeren en tokens te beheren. Het keycloak_openid-object, gedefinieerd in keycloak_config, biedt methoden om gebruikersinformatie op te halen en de sessiestatus te verifiëren.

Decorators

login_required: Verplicht de gebruiker om ingelogd te zijn.
role_required: Verplicht dat de gebruiker een bepaalde rol heeft om toegang te krijgen tot de route. Gebruikt binnen het teacher_dashboard en student_dashboard.
Tokenbeheer

Tokens worden opgehaald bij een succesvolle login en opgeslagen in session['token']. De JWT-token bevat rolinformatie om de juiste dashboardinhoud weer te geven.

Dit document biedt een overzicht van de belangrijkste onderdelen binnen het project en legt de flow en toegangspaden uit. Bij vragen kun je de specifieke routes of decorators aanpassen en uitbreiden met de bestaande structuur.