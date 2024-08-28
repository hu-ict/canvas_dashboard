# Sequence
Binnen het systeem kennen we een `AssignmentSequence` en een `SubmissionSequence`. In feite zijn het een `Assignment` en `Submission`, maar dan met meerdere mogelijkheden tot inleveren. Een sequence wordt bij elkaar geplaatst door een hashtag met een code in de Assignment.name op te nemen. Een voorbeeld: "Opdracht PROG1: NS-functies (#O1-PROG)".
## De class `AssignmentSequence`
`get_day()` en `get_date` geven de vroegste day en date van de sequence. Het is de oorspronkelijk inleverdatum.
De klasse heeft twee methoden die toelichting verdienen.
- `get_last_passed_assignment(actual_day)`, 
## De class `SubmissionSequence`
get_score()


| Syntax      | Ingeleverd  | Voor deadline | Gewaardeerd | Plot Assignment | Plot Submission |
| :---  | :---  | :---  | :---  | :---  | :---  |
| 1 | Nee | Ja  | Nee | Komende | Geen    |
| 2 | Nee | Nee | Nee | Komende | Actueel |
| 3 | Ja  | Ja  | Nee | Geen    | Actueel |
| 4 | Ja  | Ja  | Ja  | Komende | Actueel |

Een `Assignment` wordt altijd als een klein grijs bolletje getoond. Komende betekent alleen eerste komende Assignment, eventueel op basis van rules. Zie de note onderaan de pagina.

Een `Submission` wordt getoont:
- (bij 2) als er niets is opgeleverd: rood bolletje, day is dag van de laatste niet ingeleverde assignment, waarde
- (bij 3) als er een oplevering nog niet is gewaardeerd: lavendel klein bolletje, day is dag van de niet gewaardeerde assignment, waarde is de hoogste waarde in de submission_sequence
- (bij 4) als een submission is gewaardeerd: kleur bolletje, day is dag van de hoogste submission score, waarde is de hoogste waarde in de submission_sequence

In Submission wordt de volledige sequence meegenomen, dus ook alle voorgaande submissions. Deze wordt in de "hover" geplaatst (pop_up) 

Openstaand punt:
In scenario 4 kan meegenomen worden of een student voldoende waarde heeft gehaald met de Submission(s). Geen voldoende waarde toon dan ook komende Assignment, wel voldoende: toon dan de komende Assignment niet.
