import gspread
from oauth2client.service_account import ServiceAccountCredentials
from email.message import EmailMessage
import ssl
import smtplib


scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

creds = ServiceAccountCredentials.from_json_keyfile_name("C:\\Users\\tinch\\Documents\\ZPD\\versija 3\\api-key.json", scopes=scopes)

file = gspread.authorize(creds)
workbook = file.open("zpd-anketas-rezultati")
worksheet = workbook.sheet1
all_values = worksheet.get_all_values()

age_column = 3
points_column = len(all_values[0]) - 1
alertness_points_column = len(all_values[0]) - 2
transport_points_column = len(all_values[0]) - 3
evening_points_column = len(all_values[0]) - 4
school_points_column = len(all_values[0]) - 5

average_sums = {}
average_alertness_sums = {}
average_transport_sleep_sums = {}
average_evening_sleep_sums = {}
average_school_sleep_sums = {}

#miegainība transportā
for age in range(11, 18):
    total_sum = 0
    count = 0

    for row in all_values:
        if row[age_column] == str(age):
            points = int(row[transport_points_column])

            total_sum += points
            count += 1

    if count > 0:
        average_transport_sleep_sum = total_sum / count
        average_transport_sleep_sums[f"Age_{age}"] = average_transport_sleep_sum
    else:
       average_transport_sleep_sums[f"Age_{age}"] = None

for age, average_transport_sleep_sum in average_transport_sleep_sums.items():
    if average_transport_sleep_sum is not None:
        print(f"miegainiba transporta {age}: {average_transport_sleep_sum:.2f}")
        
#možums skolā
for age in range(11, 18):
    total_sum = 0
    count = 0

    for row in all_values:
        if row[age_column] == str(age):
            points = int(row[alertness_points_column])

            total_sum += points
            count += 1

    if count > 0:
        average_alertness_sum = total_sum / count
        average_alertness_sums[f"Age_{age}"] = average_alertness_sum
    else:
        average_alertness_sums[f"Age_{age}"] = None

for age, average_alertness_sum in average_alertness_sums.items():
    if average_alertness_sum is not None:
        print(f"mozums skola {age}: {average_alertness_sum:.2f}")

#miegainība vakarā
for age in range(11, 18):
    total_sum = 0
    count = 0

    for row in all_values:
        if row[age_column] == str(age):
            points = int(row[evening_points_column])

            total_sum += points
            count += 1

    if count > 0:
        average_evening_sleep_sum = total_sum / count
        average_evening_sleep_sums[f"Age_{age}"] = average_evening_sleep_sum
    else:
       average_transport_sleep_sums[f"Age_{age}"] = None

for age, average_evening_sleep_sum in average_evening_sleep_sums.items():
    if average_evening_sleep_sum is not None:
        print(f"miegainiba vakara {age}: {average_evening_sleep_sum:.2f}")

#miegainība skolā
for age in range(11, 18):
    total_sum = 0
    count = 0

    for row in all_values:
        if row[age_column] == str(age):
            points = int(row[school_points_column])

            total_sum += points
            count += 1

    if count > 0:
        average_school_sleep_sum = total_sum / count
        average_school_sleep_sums[f"Age_{age}"] = average_school_sleep_sum
    else:
       average_transport_sleep_sums[f"Age_{age}"] = None

for age, average_school_sleep_sum in average_school_sleep_sums.items():
    if average_school_sleep_sum is not None:
        print(f"miegainiba skola {age}: {average_school_sleep_sum:.2f}")

#vidējais katram vecumam
for age in range(11, 18):
    total_sum = 0
    count = 0

    for row in all_values:
        if row[age_column] == str(age):
            points = int(row[points_column])

            total_sum += points
            count += 1

    if count > 0:
        average_sum = total_sum / count
        average_sums[f"Age_{age}"] = average_sum
    else:
        average_sums[f"Age_{age}"] = None

for age, average_sum in average_sums.items():
    if average_sum is not None:
        print(f"videjais rezultats {age}: {average_sum:.2f}")

for row in all_values[1:]:
    epasts = row[1]
    age = row[3]
    sleep_in_school = row[-5]
    sleep_in_evening = row[-4]
    sleep_in_transport = row[-3]
    alertness_in_school = row[-2]
    sum_of_points = row[-1]

    if age == "11":
        message = f"            Liels paldies, ka izpildīji manu aptauju! Tavu sniegto atbilžu rezultātā ieguvi {sum_of_points} punktus. Vidējais punktu skaits cilvēkiem Tavā vecumā ir {average_sums['Age_11']:.2f} Maksimālais punktu skaits ir 80. \n            Jo lielāks punktu skaits, jo attiecīgi miegaināks/a tu ikdienā jūties. Augstāki rezultāti var arī norādīt uz iespējamu miega traucējumu klātbūtni vai noslieci uz traucējumiem kā insomnia un miega apnoja.\n            Tests iekļāva arī jautājumus, kas nosaka Tavu miegainību dažādās ikdienas situācijās - Miegainību skolā, miegainību vakarā, miegainību transportā un modrību skolā. Attiecīgi šiem faktoriem tavi rezultāti ir šādi: \n            Miegainība skolā - {sleep_in_school} punkti no 25. Vidējais - {average_school_sleep_sums['Age_11']:.2f}\n            Miegainība vakarā - {sleep_in_evening} punkti no 15. Vidējais - {average_evening_sleep_sums['Age_11']:.2f}\n            Miegainība tranportā - {sleep_in_transport} punkti no 15. Vidējais - {average_transport_sleep_sums['Age_11']:.2f}\n            Modrība skolā - {alertness_in_school} punkti no 25. Vidējais - {average_alertness_sums['Age_11']:.2f}\n            Ņem vērā, ka KPMA nav tests, ko izmanto lai izteiktu diagnozi, bet gan tests, kas ļauj pusaudzim pašam izvērtēt savu enerģijas daudzumu dienas laikā. Ja uztraucies par iegūto punktu skaitu, kā arī ilgstoši jau ikdienā izjūti miega traucējumu simptomus (pastiprinātu nogurumu dienas laikā, galvassāpes, koncentrēšanās un uzmanības noturēšanas grūtības, garastāvokļa svārstības, pastiprinātu kairināmību, agresivitāti, atmiņas un kustību koordinācijas traucējumus u.c.), sazinies ar savu vecāku vai aizbildni, informē par savu uztraukumu un simptomiem, un iespējams sazinies ar ģimenes ārstu. Lūk arī daži resursi lai vairāk uzzinātu par miega traucējumiem, to ārstēšanu un KPMA projektu.\n            Pamatinformācija par miega traucējumiem: \n            https://www.spkc.gov.lv/lv/miega-traucejumi?utm_source=https%3A%2F%2Fwww.google.com%2F \n            Ieteikumi miega uzlabošanai (Epilepsijas un miega medicīnas centra miega speciāliste-pediatre Marta Celmiņa): \n            https://medicine.lv/raksti/6-izplatitakie-miega-traucejumi-un-ieteikumi-miega-uzlabosanai-stasta-specialiste \n            Klīvlendas Pusaudžu Miegainības aptaujas pētījums (Angliski):\n            https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2045721/"
    elif age =="12":
        message = f"            Liels paldies, ka izpildīji manu aptauju! Tavu sniegto atbilžu rezultātā ieguvi {sum_of_points} punktus. Vidējais punktu skaits cilvēkiem Tavā vecumā ir {average_sums['Age_12']:.2f} Maksimālais punktu skaits ir 80. \n            Jo lielāks punktu skaits, jo attiecīgi miegaināks/a tu ikdienā jūties. Augstāki rezultāti var arī norādīt uz iespējamu miega traucējumu klātbūtni vai noslieci uz traucējumiem kā insomnia un miega apnoja.\n            Tests iekļāva arī jautājumus, kas nosaka Tavu miegainību dažādās ikdienas situācijās - Miegainību skolā, miegainību vakarā, miegainību transportā un modrību skolā. Attiecīgi šiem faktoriem tavi rezultāti ir šādi: \n            Miegainība skolā - {sleep_in_school} punkti no 25. Vidējais - {average_school_sleep_sums['Age_12']:.2f}\n            Miegainība vakarā - {sleep_in_evening} punkti no 15. Vidējais - {average_evening_sleep_sums['Age_12']:.2f}\n            Miegainība tranportā - {sleep_in_transport} punkti no 15. Vidējais - {average_transport_sleep_sums['Age_12']:.2f}\n            Modrība skolā - {alertness_in_school} punkti no 25. Vidējais - {average_alertness_sums['Age_12']:.2f}\n            Ņem vērā, ka KPMA nav tests, ko izmanto lai izteiktu diagnozi, bet gan tests, kas ļauj pusaudzim pašam izvērtēt savu enerģijas daudzumu dienas laikā. Ja uztraucies par iegūto punktu skaitu, kā arī ilgstoši jau ikdienā izjūti miega traucējumu simptomus (pastiprinātu nogurumu dienas laikā, galvassāpes, koncentrēšanās un uzmanības noturēšanas grūtības, garastāvokļa svārstības, pastiprinātu kairināmību, agresivitāti, atmiņas un kustību koordinācijas traucējumus u.c.), sazinies ar savu vecāku vai aizbildni, informē par savu uztraukumu un simptomiem, un iespējams sazinies ar ģimenes ārstu. Lūk arī daži resursi lai vairāk uzzinātu par miega traucējumiem, to ārstēšanu un KPMA projektu.\n            Pamatinformācija par miega traucējumiem: \n            https://www.spkc.gov.lv/lv/miega-traucejumi?utm_source=https%3A%2F%2Fwww.google.com%2F \n            Ieteikumi miega uzlabošanai (Epilepsijas un miega medicīnas centra miega speciāliste-pediatre Marta Celmiņa): \n            https://medicine.lv/raksti/6-izplatitakie-miega-traucejumi-un-ieteikumi-miega-uzlabosanai-stasta-specialiste \n            Klīvlendas Pusaudžu Miegainības aptaujas pētījums (Angliski):\n            https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2045721/"
    elif age =="13":
        message = f"            Liels paldies, ka izpildīji manu aptauju! Tavu sniegto atbilžu rezultātā ieguvi {sum_of_points} punktus. Vidējais punktu skaits cilvēkiem Tavā vecumā ir {average_sums['Age_13']:.2f} Maksimālais punktu skaits ir 80. \n            Jo lielāks punktu skaits, jo attiecīgi miegaināks/a tu ikdienā jūties. Augstāki rezultāti var arī norādīt uz iespējamu miega traucējumu klātbūtni vai noslieci uz traucējumiem kā insomnia un miega apnoja.\n            Tests iekļāva arī jautājumus, kas nosaka Tavu miegainību dažādās ikdienas situācijās - Miegainību skolā, miegainību vakarā, miegainību transportā un modrību skolā. Attiecīgi šiem faktoriem tavi rezultāti ir šādi: \n            Miegainība skolā - {sleep_in_school} punkti no 25. Vidējais - {average_school_sleep_sums['Age_13']:.2f}\n            Miegainība vakarā - {sleep_in_evening} punkti no 15. Vidējais - {average_evening_sleep_sums['Age_13']:.2f}\n            Miegainība tranportā - {sleep_in_transport} punkti no 15. Vidējais - {average_transport_sleep_sums['Age_13']:.2f}\n            Modrība skolā - {alertness_in_school} punkti no 25. Vidējais - {average_alertness_sums['Age_13']:.2f}\n            Ņem vērā, ka KPMA nav tests, ko izmanto lai izteiktu diagnozi, bet gan tests, kas ļauj pusaudzim pašam izvērtēt savu enerģijas daudzumu dienas laikā. Ja uztraucies par iegūto punktu skaitu, kā arī ilgstoši jau ikdienā izjūti miega traucējumu simptomus (pastiprinātu nogurumu dienas laikā, galvassāpes, koncentrēšanās un uzmanības noturēšanas grūtības, garastāvokļa svārstības, pastiprinātu kairināmību, agresivitāti, atmiņas un kustību koordinācijas traucējumus u.c.), sazinies ar savu vecāku vai aizbildni, informē par savu uztraukumu un simptomiem, un iespējams sazinies ar ģimenes ārstu. Lūk arī daži resursi lai vairāk uzzinātu par miega traucējumiem, to ārstēšanu un KPMA projektu.\n            Pamatinformācija par miega traucējumiem: \n            https://www.spkc.gov.lv/lv/miega-traucejumi?utm_source=https%3A%2F%2Fwww.google.com%2F \n            Ieteikumi miega uzlabošanai (Epilepsijas un miega medicīnas centra miega speciāliste-pediatre Marta Celmiņa): \n            https://medicine.lv/raksti/6-izplatitakie-miega-traucejumi-un-ieteikumi-miega-uzlabosanai-stasta-specialiste \n            Klīvlendas Pusaudžu Miegainības aptaujas pētījums (Angliski):\n            https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2045721/"
    elif age == "14":
        message = f"            Liels paldies, ka izpildīji manu aptauju! Tavu sniegto atbilžu rezultātā ieguvi {sum_of_points} punktus. Vidējais punktu skaits cilvēkiem Tavā vecumā ir {average_sums['Age_14']:.2f} Maksimālais punktu skaits ir 80. \n            Jo lielāks punktu skaits, jo attiecīgi miegaināks/a tu ikdienā jūties. Augstāki rezultāti var arī norādīt uz iespējamu miega traucējumu klātbūtni vai noslieci uz traucējumiem kā insomnia un miega apnoja.\n            Tests iekļāva arī jautājumus, kas nosaka Tavu miegainību dažādās ikdienas situācijās - Miegainību skolā, miegainību vakarā, miegainību transportā un modrību skolā. Attiecīgi šiem faktoriem tavi rezultāti ir šādi: \n            Miegainība skolā - {sleep_in_school} punkti no 25. Vidējais - {average_school_sleep_sums['Age_14']:.2f}\n            Miegainība vakarā - {sleep_in_evening} punkti no 15. Vidējais - {average_evening_sleep_sums['Age_14']:.2f}\n            Miegainība tranportā - {sleep_in_transport} punkti no 15. Vidējais - {average_transport_sleep_sums['Age_14']:.2f}\n            Modrība skolā - {alertness_in_school} punkti no 25. Vidējais - {average_alertness_sums['Age_14']:.2f}\n            Ņem vērā, ka KPMA nav tests, ko izmanto lai izteiktu diagnozi, bet gan tests, kas ļauj pusaudzim pašam izvērtēt savu enerģijas daudzumu dienas laikā. Ja uztraucies par iegūto punktu skaitu, kā arī ilgstoši jau ikdienā izjūti miega traucējumu simptomus (pastiprinātu nogurumu dienas laikā, galvassāpes, koncentrēšanās un uzmanības noturēšanas grūtības, garastāvokļa svārstības, pastiprinātu kairināmību, agresivitāti, atmiņas un kustību koordinācijas traucējumus u.c.), sazinies ar savu vecāku vai aizbildni, informē par savu uztraukumu un simptomiem, un iespējams sazinies ar ģimenes ārstu. Lūk arī daži resursi lai vairāk uzzinātu par miega traucējumiem, to ārstēšanu un KPMA projektu.\n            Pamatinformācija par miega traucējumiem: \n            https://www.spkc.gov.lv/lv/miega-traucejumi?utm_source=https%3A%2F%2Fwww.google.com%2F \n            Ieteikumi miega uzlabošanai (Epilepsijas un miega medicīnas centra miega speciāliste-pediatre Marta Celmiņa): \n            https://medicine.lv/raksti/6-izplatitakie-miega-traucejumi-un-ieteikumi-miega-uzlabosanai-stasta-specialiste \n            Klīvlendas Pusaudžu Miegainības aptaujas pētījums (Angliski):\n            https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2045721/"
    elif age == "15":
        message = f"            Liels paldies, ka izpildīji manu aptauju! Tavu sniegto atbilžu rezultātā ieguvi {sum_of_points} punktus. Vidējais punktu skaits cilvēkiem Tavā vecumā ir {average_sums['Age_15']:.2f} Maksimālais punktu skaits ir 80. \n            Jo lielāks punktu skaits, jo attiecīgi miegaināks/a tu ikdienā jūties. Augstāki rezultāti var arī norādīt uz iespējamu miega traucējumu klātbūtni vai noslieci uz traucējumiem kā insomnia un miega apnoja.\n            Tests iekļāva arī jautājumus, kas nosaka Tavu miegainību dažādās ikdienas situācijās - Miegainību skolā, miegainību vakarā, miegainību transportā un modrību skolā. Attiecīgi šiem faktoriem tavi rezultāti ir šādi: \n            Miegainība skolā - {sleep_in_school} punkti no 25. Vidējais - {average_school_sleep_sums['Age_15']:.2f}\n            Miegainība vakarā - {sleep_in_evening} punkti no 15. Vidējais - {average_evening_sleep_sums['Age_15']:.2f}\n            Miegainība tranportā - {sleep_in_transport} punkti no 15. Vidējais - {average_transport_sleep_sums['Age_15']:.2f}\n            Modrība skolā - {alertness_in_school} punkti no 25. Vidējais - {average_alertness_sums['Age_15']:.2f}\n            Ņem vērā, ka KPMA nav tests, ko izmanto lai izteiktu diagnozi, bet gan tests, kas ļauj pusaudzim pašam izvērtēt savu enerģijas daudzumu dienas laikā. Ja uztraucies par iegūto punktu skaitu, kā arī ilgstoši jau ikdienā izjūti miega traucējumu simptomus (pastiprinātu nogurumu dienas laikā, galvassāpes, koncentrēšanās un uzmanības noturēšanas grūtības, garastāvokļa svārstības, pastiprinātu kairināmību, agresivitāti, atmiņas un kustību koordinācijas traucējumus u.c.), sazinies ar savu vecāku vai aizbildni, informē par savu uztraukumu un simptomiem, un iespējams sazinies ar ģimenes ārstu. Lūk arī daži resursi lai vairāk uzzinātu par miega traucējumiem, to ārstēšanu un KPMA projektu.\n            Pamatinformācija par miega traucējumiem: \n            https://www.spkc.gov.lv/lv/miega-traucejumi?utm_source=https%3A%2F%2Fwww.google.com%2F \n            Ieteikumi miega uzlabošanai (Epilepsijas un miega medicīnas centra miega speciāliste-pediatre Marta Celmiņa): \n            https://medicine.lv/raksti/6-izplatitakie-miega-traucejumi-un-ieteikumi-miega-uzlabosanai-stasta-specialiste \n            Klīvlendas Pusaudžu Miegainības aptaujas pētījums (Angliski):\n            https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2045721/"
    elif age == "16":
        message = f"            Liels paldies, ka izpildīji manu aptauju! Tavu sniegto atbilžu rezultātā ieguvi {sum_of_points} punktus. Vidējais punktu skaits cilvēkiem Tavā vecumā ir {average_sums['Age_16']:.2f} Maksimālais punktu skaits ir 80. \n            Jo lielāks punktu skaits, jo attiecīgi miegaināks/a tu ikdienā jūties. Augstāki rezultāti var arī norādīt uz iespējamu miega traucējumu klātbūtni vai noslieci uz traucējumiem kā insomnia un miega apnoja.\n            Tests iekļāva arī jautājumus, kas nosaka Tavu miegainību dažādās ikdienas situācijās - Miegainību skolā, miegainību vakarā, miegainību transportā un modrību skolā. Attiecīgi šiem faktoriem tavi rezultāti ir šādi: \n            Miegainība skolā - {sleep_in_school} punkti no 25. Vidējais - {average_school_sleep_sums['Age_16']:.2f}\n            Miegainība vakarā - {sleep_in_evening} punkti no 15. Vidējais - {average_evening_sleep_sums['Age_16']:.2f}\n            Miegainība tranportā - {sleep_in_transport} punkti no 15. Vidējais - {average_transport_sleep_sums['Age_16']:.2f}\n            Modrība skolā - {alertness_in_school} punkti no 25. Vidējais - {average_alertness_sums['Age_16']:.2f}\n            Ņem vērā, ka KPMA nav tests, ko izmanto lai izteiktu diagnozi, bet gan tests, kas ļauj pusaudzim pašam izvērtēt savu enerģijas daudzumu dienas laikā. Ja uztraucies par iegūto punktu skaitu, kā arī ilgstoši jau ikdienā izjūti miega traucējumu simptomus (pastiprinātu nogurumu dienas laikā, galvassāpes, koncentrēšanās un uzmanības noturēšanas grūtības, garastāvokļa svārstības, pastiprinātu kairināmību, agresivitāti, atmiņas un kustību koordinācijas traucējumus u.c.), sazinies ar savu vecāku vai aizbildni, informē par savu uztraukumu un simptomiem, un iespējams sazinies ar ģimenes ārstu. Lūk arī daži resursi lai vairāk uzzinātu par miega traucējumiem, to ārstēšanu un KPMA projektu.\n            Pamatinformācija par miega traucējumiem: \n            https://www.spkc.gov.lv/lv/miega-traucejumi?utm_source=https%3A%2F%2Fwww.google.com%2F \n            Ieteikumi miega uzlabošanai (Epilepsijas un miega medicīnas centra miega speciāliste-pediatre Marta Celmiņa): \n            https://medicine.lv/raksti/6-izplatitakie-miega-traucejumi-un-ieteikumi-miega-uzlabosanai-stasta-specialiste \n            Klīvlendas Pusaudžu Miegainības aptaujas pētījums (Angliski):\n            https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2045721/"
    elif age == "17":
        message = f"            Liels paldies, ka izpildīji manu aptauju! Tavu sniegto atbilžu rezultātā ieguvi {sum_of_points} punktus. Vidējais punktu skaits cilvēkiem Tavā vecumā ir {average_sums['Age_17']:.2f} Maksimālais punktu skaits ir 80. \n            Jo lielāks punktu skaits, jo attiecīgi miegaināks/a tu ikdienā jūties. Augstāki rezultāti var arī norādīt uz iespējamu miega traucējumu klātbūtni vai noslieci uz traucējumiem kā insomnia un miega apnoja.\n            Tests iekļāva arī jautājumus, kas nosaka Tavu miegainību dažādās ikdienas situācijās - Miegainību skolā, miegainību vakarā, miegainību transportā un modrību skolā. Attiecīgi šiem faktoriem tavi rezultāti ir šādi: \n            Miegainība skolā - {sleep_in_school} punkti no 25. Vidējais - {average_school_sleep_sums['Age_17']:.2f}\n            Miegainība vakarā - {sleep_in_evening} punkti no 15. Vidējais - {average_evening_sleep_sums['Age_17']:.2f}\n            Miegainība tranportā - {sleep_in_transport} punkti no 15. Vidējais - {average_transport_sleep_sums['Age_17']:.2f}\n            Modrība skolā - {alertness_in_school} punkti no 25. Vidējais - {average_alertness_sums['Age_17']:.2f}\n            Ņem vērā, ka KPMA nav tests, ko izmanto lai izteiktu diagnozi, bet gan tests, kas ļauj pusaudzim pašam izvērtēt savu enerģijas daudzumu dienas laikā. Ja uztraucies par iegūto punktu skaitu, kā arī ilgstoši jau ikdienā izjūti miega traucējumu simptomus (pastiprinātu nogurumu dienas laikā, galvassāpes, koncentrēšanās un uzmanības noturēšanas grūtības, garastāvokļa svārstības, pastiprinātu kairināmību, agresivitāti, atmiņas un kustību koordinācijas traucējumus u.c.), sazinies ar savu vecāku vai aizbildni, informē par savu uztraukumu un simptomiem, un iespējams sazinies ar ģimenes ārstu. Lūk arī daži resursi lai vairāk uzzinātu par miega traucējumiem, to ārstēšanu un KPMA projektu.\n            Pamatinformācija par miega traucējumiem: \n            https://www.spkc.gov.lv/lv/miega-traucejumi?utm_source=https%3A%2F%2Fwww.google.com%2F \n            Ieteikumi miega uzlabošanai (Epilepsijas un miega medicīnas centra miega speciāliste-pediatre Marta Celmiņa): \n            https://medicine.lv/raksti/6-izplatitakie-miega-traucejumi-un-ieteikumi-miega-uzlabosanai-stasta-specialiste \n            Klīvlendas Pusaudžu Miegainības aptaujas pētījums (Angliski):\n            https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2045721/"

    email_sender = 'kpmaptauja@gmail.com'
    email_password = 'nedo susa vupa roli'

    subject = 'KPMA Aptaujas Rezultāti'
    body = message
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = epasts
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, epasts, em.as_string())
