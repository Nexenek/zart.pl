# A takie gówno do zabawy z vulcan api lol
**Teraz działa z różnymi kluczami!**

---
# Jak tego używać?
Well no zacznijmy od pobrania pythona. Ja osobiście używałem wersji `3.12.5`

Pythona możecie pobrać z oficjalnej strony, odpowiednie instrukcje dla waszego systemu operacyjnego napewo też tam są.

Kiedy już macie pythona to teraz stwórzmy sobie wirtualne środowisko, tak aby nie mieć żadnych dziwnych konfliktów:

Na systemach Unixowych (takie jak Linux / MacOS):
```bash
python3 -m venv venv
source ./venv/bin/activate
```
Na Windowsie:
```cmd
python -m venv venv
.\venv\Scripts\activate
```
teraz możemy zainstalować wymagane biblioteki:

Unix:
```bash
python3 -m pip install -U -r requirements.txt
```
Windows:
```cmd
python -m pip install -U -r requirements.txt
```

na sam koniec **bardzo ważny punkt** - musimy zainstalować *sztuczne* przeglądarki biblioteki playwirght

unix:
```bash
python3 -m playwright install
```
*(na niektórych dystrybucjach linuxa może wyświetlić się komunikat o braku wymaganych bibliotek ale możecie go zignorować)*

Windows:
```cmd
python -m playwright install
```

that's it

### Uruchamianie skryptu

Zanim tak po prostu uruchomicie skrypt wejdzcie do pliku `literaljoke.py` i podajcie swoje `hasło` i `login` w *odpowiednie miejsce na górze pliku*. Możecie też zmienić daty `od` i `do` aby uzyskać plan lekcji z innego okresu

```python
################################### Dane logowania #######################################

login = 'LOGIN_DO_EDUVULCAN'
haselko = 'HASŁO_DO_EDUVULCAN'

dataOd='2024-09-01T22:00:00.000Z'
dataDo='2024-09-08T21:59:59.999Z'

################################### Dane logowania #######################################
```

Teraz kiedy to macie gotowe powinniście być w stanie bez problemu uruchomić skrypt:
unix:
```bash
python3 literaljoke.py
```
Windows:
```cmd
python literaljoke.py
```

### Przed następnym uruchomieniem
Za każdym razem gdy zamkniecie CMD/terminal musicie uruchomić ponownie wasze wirtualne środowisko

unix:
```bash
source ./venv/bin/activate
```
Windows:
```
.\venv\Scripts\activate
```

i po uruchomieniu jednej z tych komend możecie znowu używać skryptu

---

*note: nie testowałem nic z tego na Windowsie*