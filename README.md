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
