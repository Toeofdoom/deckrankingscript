### First time setup
Set up google sheets api according to https://developers.google.com/sheets/api/quickstart/python and put credentials.json in this folder

Edit the variables in autorankings to point to the correct spreadsheet/sheets

RANKINGS_SPREADSHEET_ID should be the tag in the url of the spreadsheet eg.
https://docs.google.com/spreadsheets/d/THIS_ID_HERE

Install all dependencies with:

    pip install --upgrade choix google-api-python-client google-auth-httplib2 google-auth-oauthlib

### Spreadsheet format
DATA_RANGE - By default, it reads games from the spreadsheet named "Data" formatted as:
Deck 1|Score|Deck 2|Score
---|---|---|---
Engihot|3|Ghostwriter|2
Engihot|3|Givaqueen|0
Engihot|2|Fanpenny|3
Engihot|3|Jones|2
Engihot|3|Spacehook|1
Engihot|3|Haukea|1
Engihot|2|Lysander|3
Ghostwriter|2|Fanpenny|3
Givaqueen|3|Fanpenny|1
Givaqueen|3|Spacehook|1
Givaqueen|3|Haukea|0
Givaqueen|2|Lysander|3

RANKINGS_RANGE, BACKUP_RANKINGS_RANGE - By default, rankings are printed in the sheet named "AutoRankings" in this format:
Deck|Ranking|Deck|Previous Ranking
---|---|---|---
Crow|1801.240374|Backforge|1800.456769
Backforge|1801.240374|Kudravi|1800.456769
Kudravi|1801.240374|Remy|1800.456769
Haukea|1788.095813|Haukea|1787.17334
Nuke|1772.083618|Nuke|1771.221925
Virun|1757.955958|Virun|1757.262089
Singingview|1755.847593|Singingview|1755.097799
Qing|1752.611028|Qing|1751.932815
Engihot|1744.629027|Engihot|1743.576319
Lysander|1742.405142|Lysander|1741.757298
Fanpenny|1741.849757|Fanpenny|1741.127943

To run the script, run

    python autorankings.py

### Running without API setup
You can run 

    python inference.py

directly - it will pull data from the "data" section internally. You can copy/paste data directly from a spreadsheet over the existing contents, and the output can be pasted back into a spreadsheet, e.g. the default output is:

    Lysander, 2136.117885667992
    Engihot, 1430.141161578291
    Givaqueen, 1430.0236120510476
    Spacehook, 1255.2688904551655
    Haukea, 1255.2688904551655
    Fanpenny, 1195.056609717526
    Jones, 574.5272124541889
    Ghostwriter, 323.5957376206237
