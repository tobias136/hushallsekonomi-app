# hushallsekonomi-app
Syfte:
att ha en app som hjälper till med budgetering av privatekonomi. appen skall ha koll på budget över 12 månader framåt och ha ett balanskonto för tidigare månader. tanken är att varje sub-kategori skall ha ett balanskonto, där jag kan "låna" från framtiden, re-balansera mellan olika sub-kategorier.

Exempelfall:
Klädbudget/månad a 2000 kr
Lunch/månad a 1500 kr
Jag vill köpa ett par byxor och en jacka för 2500 kr. Möjligheten skall då finnas att re-balansera mellan dessa två konton, där jag "tar" 500 kr från lunchkontot och "ger" till klädkontot.

Körning av CLI:
TBD

Strukturöversikt:
TBD

Budget


--------------------------------------------
Makefile
--------------------------------------------
 Vad du kan göra nu:

Kommando	Effekt
make reset	Raderar kategorier.json och import_*.json.
make test	Kör alla enhetstester med pytest.
make run-import	Importerar csv/test_bank.csv och kör hela kategoriseringsflödet.
make format	Formaterar din kod enligt PEP8-standard.
make lint	Kollar kodkvalitet, hittar misstag och ger förbättringstips.

📌 Instruktioner för att börja använda:
Lägg filen som Makefile i roten av hushallsekonomi-app/.

Öppna terminalen i projektmappen.

Kör exempelvis:

bash
Kopiera
Redigera
make reset
make run-import
make test


köra tester:
pytest tests/
# eller
python -m unittest discover tests


köra olika funktioner:
    importera data och generera datafil:
    python3 app/CLI/main.py importera csv/Lönekonto_test_april.csv

    rapportering:
    python3 app/CLI/main.py report data/import_2025-05-03.json

    report latest:
    python3 app/CLI/main.py report-latest --save csv
    python3 app/CLI/main.py report-latest --save markdown
    python3 app/CLI/main.py report-latest --save json

    budget-check:
    python3 app/CLI/main.py budget-check
    med egna paths:
    python3 app/CLI/main.py budget-check --budget-path=json/budget.json --transactions-path=data/import_2025-05-03.json



Kör flöde från start till slut:
1. Importera CSV
bash
Kopiera
Redigera
python3 app/CLI/main.py import --file csv/lonekonto_2025-05_verkliga.csv
➡️ Skapar JSON-fil (t.ex. data/import_2025-05-21.json)

2. Kategorisera transaktioner (om inte redan gjort)
bash
Kopiera
Redigera
python3 app/CLI/main.py categorize --file data/import_xxx.json
➡️ Använder/uppdaterar kategorier.json

3. Generera rapport
bash
Kopiera
Redigera
python3 app/CLI/main.py report-latest
➡️ Terminalutskrift + eventuell export

4. Kör budgetkontroll
bash
Kopiera
Redigera
python3 app/CLI/main.py budget-check
➡️ Jämför utfall med budget.json
