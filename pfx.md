Poniżej masz **konkretną, praktyczną procedurę** instalacji certyfikatu *.pfx na serwerze Apache w Linux **z użyciem bash**.

## ✔️ Krok 1: Wyodrębnij certyfikat i klucz prywatny z pliku .pfx

Plik **PFX** zawiera certyfikat, klucz prywatny i CA bundle. Musimy je rozdzielić.

```bash
# 1. Klucz prywatny
openssl pkcs12 -in cert.pfx -nocerts -out privkey_encrypted.key

# 2. Usuń hasło z klucza (Apache wymaga klucza bez hasła)
openssl rsa -in privkey_encrypted.key -out privkey.key

# 3. Certyfikat publiczny
openssl pkcs12 -in cert.pfx -clcerts -nokeys -out cert.crt

# 4. Certyfikaty CA (jeśli są w pfx)
openssl pkcs12 -in cert.pfx -cacerts -nokeys -out chain.crt
```

System zapyta o hasło do `.pfx`.

Finalnie otrzymasz pliki:

* `privkey.key`
* `cert.crt`
* `chain.crt` (opcjonalnie)

---

## ✔️ Krok 2: Przenieś pliki do katalogu Apache

Najczęściej:

```bash
sudo mv privkey.key /etc/ssl/private/
sudo mv cert.crt /etc/ssl/certs/
sudo mv chain.crt /etc/ssl/certs/
sudo chmod 600 /etc/ssl/private/privkey.key
```

---

## ✔️ Krok 3: Skonfiguruj Apache (VirtualHost port 443)

Edytuj konfigurację SSL:

```bash
sudo nano /etc/apache2/sites-available/default-ssl.conf
```

lub w CentOS/RHEL:

```bash
sudo nano /etc/httpd/conf.d/ssl.conf
```

Dodaj/zmień:

```apache
<VirtualHost *:443>
    ServerName twojadomena.pl

    SSLEngine on
    SSLCertificateFile      /etc/ssl/certs/cert.crt
    SSLCertificateKeyFile   /etc/ssl/private/privkey.key
    SSLCertificateChainFile /etc/ssl/certs/chain.crt

    DocumentRoot /var/www/html
</VirtualHost>
```

---

## ✔️ Krok 4: Włącz SSL i restart Apache

Debian/Ubuntu:

```bash
sudo a2enmod ssl
sudo a2ensite default-ssl
sudo systemctl restart apache2
```

CentOS/RHEL:

```bash
sudo systemctl restart httpd
```

---

## ✔️ Krok 5: Sprawdź czy certyfikat działa

```bash
openssl s_client -connect twojadomena.pl:443 -servername twojadomena.pl
```

Powinieneś zobaczyć łańcuch certyfikatów.

---

## ✔️ Jeśli chcesz, mogę przygotować:

✅ automatyczny skrypt bash do konwersji i instalacji
✅ konfigurację VirtualHost pod Twoją domenę
✅ wersję pod Apache na CentOS/RHEL lub Ubuntu

Chcesz skrypt „one-click”?

Utworzenie pliku **PFX** ($*.pfx$), który zawiera zarówno certyfikat, jak i klucz prywatny, za pomocą wiersza poleceń (cmd) w systemie Windows, wymaga zazwyczaj użycia narzędzi dostępnych w pakietach deweloperskich, takich jak **Windows SDK** lub **OpenSSL**.

-----

## 🛠️ Metoda 1: Użycie Pvk2Pfx (Windows SDK)

Ta metoda jest przeznaczona do konwersji starszych formatów klucza prywatnego ($*.pvk$) i certyfikatu ($*.cer$ lub $*.spc$) na format PFX. Narzędzie **Pvk2Pfx.exe** wchodzi w skład pakietu **Windows SDK**.

### Wymagania wstępne

Musisz mieć:

1.  Plik klucza prywatnego (np. `MyCert.pvk`).
2.  Plik certyfikatu (np. `MyCert.cer` lub `MyCert.spc`).
3.  Zainstalowany **Windows SDK** (narzędzie Pvk2Pfx.exe znajduje się zazwyczaj w folderze w rodzaju `C:\Program Files (x86)\Windows Kits\10\bin\x64\`).

### Polecenie

Użyj następującego formatu polecenia, zastępując nazwy plików i hasła swoimi danymi:

```cmd
"C:\Ścieżka\Do\Pvk2Pfx.exe" -pvk MyCert.pvk -pi HasloPvk -spc MyCert.cer -pfx MyCert.pfx -po HasloPfx
```

  * **-pvk MyCert.pvk**: Określa wejściowy plik klucza prywatnego.
  * **-pi HasloPvk**: Określa hasło klucza prywatnego (jeśli jest).
  * **-spc MyCert.cer**: Określa wejściowy plik certyfikatu.
  * **-pfx MyCert.pfx**: Określa nazwę wyjściowego pliku PFX.
  * **-po HasloPfx**: Określa hasło, którym zostanie zaszyfrowany plik PFX.

-----

## 🌐 Metoda 2: Użycie OpenSSL

Jeśli masz certyfikat w formacie **PEM** ($*.pem$, często używany jest też $*.crt$ dla certyfikatu i $*.key$ dla klucza prywatnego), możesz użyć narzędzia **OpenSSL**, które jest bardzo popularne, choć wymaga oddzielnej instalacji w systemie Windows.

### Wymagania wstępne

1.  Zainstalowany **OpenSSL** i ustawiona ścieżka w PATH lub uruchomienie cmd/PowerShell z katalogu `bin` OpenSSL.
2.  Plik certyfikatu (np. `cert.crt`).
3.  Plik klucza prywatnego (np. `klucz.key`).

### Polecenie

Użyj następującego polecenia, podając plik certyfikatu, klucza prywatnego i nazwę pliku PFX. Narzędzie poprosi Cię o podanie hasła do zabezpieczenia pliku PFX.

```cmd
openssl pkcs12 -export -out certyfikat.pfx -inkey klucz.key -in cert.crt
```

  * **-export**: Określa, że ma być wykonany eksport.
  * **-out certyfikat.pfx**: Nazwa pliku wyjściowego PFX.
  * **-inkey klucz.key**: Wejściowy plik klucza prywatnego.
  * **-in cert.crt**: Wejściowy plik certyfikatu.

-----

## 💾 Gdzie się zapisze plik PFX?

Plik PFX ($*.pfx$) utworzony za pomocą **Pvk2Pfx.exe** lub **OpenSSL** zapisze się w **katalogu, w którym aktualnie znajduje się wiersz poleceń (cmd)**, chyba że w poleceniu podasz pełną, bezwzględną ścieżkę do pliku wyjściowego (np. `-pfx C:\MojeCerty\MyCert.pfx`).

Aby sprawdzić aktualny katalog, wpisz w cmd:

```cmd
cd
```

Zazwyczaj jest to:

  * Katalog użytkownika (np. `C:\Users\TwojaNazwaUzytkownika`).
  * Katalog, z którego uruchomiono narzędzie (np. katalog `bin` OpenSSL).
  * Katalog, do którego ręcznie przeszedłeś za pomocą polecenia `cd`.
  
  To, skąd weźmiesz pliki **CRT** ($*.crt$, czyli certyfikat) i **KEY** ($*.key$, czyli klucz prywatny), zależy od tego, **skąd pierwotnie wziął się certyfikat** na Twoim komputerze z Windows 10 OEM (Original Equipment Manufacturer).

W systemie Windows certyfikaty i klucze prywatne są przechowywane w **Magazynie Certyfikatów Windows**, a nie jako luźne pliki. Aby uzyskać oddzielne pliki $*.crt$ i $*.key$, musisz:

1.  **Wyeksportować certyfikat publiczny** do pliku $*.crt$ lub $*.cer$.
2.  **Wyeksportować certyfikat razem z kluczem prywatnym** do pliku **PFX** ($*.pfx$), a następnie użyć zewnętrznego narzędzia, aby **wyodrębnić** z niego klucz prywatny do pliku $*.key$.

-----

## 🔑 Krok 1: Eksport Certyfikatu Publicznego (Plik $*.crt$ / $*.cer$)

Certyfikat publiczny możesz wyeksportować bezpośrednio z Menedżera Certyfikatów.

1.  **Otwórz Menedżera Certyfikatów:**
      * Naciśnij $Win + R$, wpisz `certmgr.msc` i naciśnij Enter. (Dla certyfikatów użytkownika)
      * Jeśli potrzebujesz certyfikatu komputera/systemu, naciśnij $Win + R$, wpisz `mmc`, a następnie z menu **Plik** wybierz **Dodaj/Usuń przystawkę** i dodaj **Certyfikaty** dla **Konta komputera**.
2.  **Lokalizacja:** Znajdź swój certyfikat (zazwyczaj w folderze **Osobisty** $\rightarrow$ **Certyfikaty**).
3.  **Eksport:** Kliknij prawym przyciskiem myszy na certyfikat $\rightarrow$ **Wszystkie zadania** $\rightarrow$ **Eksportuj**.
4.  **Kreator Eksportu Certyfikatów:**
      * Kliknij **Dalej**.
      * **Ważne\!** Wybierz opcję: **Nie, nie eksportuj klucza prywatnego**.
      * Jako format wybierz **X.509 zakodowany w formacie Base-64 (.CER)**.
      * Zapisz plik pod wybraną nazwą (np. `moj_certyfikat.cer` lub `moj_certyfikat.crt`).

**Wynik:** Otrzymasz plik **`moj_certyfikat.crt`** (lub $*.cer$), który zawiera wyłącznie certyfikat publiczny.

-----

## 🗝️ Krok 2: Wyodrębnienie Klucza Prywatnego (Plik $*.key$)

System Windows **nie pozwala** na bezpośredni eksport klucza prywatnego do pliku $*.key$ (format PEM). Najpierw musisz wyeksportować **certyfikat z kluczem prywatnym** do formatu PFX, a następnie użyć narzędzia **OpenSSL** do konwersji.

### ⚠️ Warunek Wstępny

Eksport klucza prywatnego jest możliwy **tylko** wtedy, gdy podczas importu (lub generowania) certyfikatu zaznaczono opcję, że **klucz prywatny jest eksportowalny**. Jeśli ta opcja była wyłączona, eksport klucza prywatnego nie będzie możliwy.

### 2A. Eksport do PFX

1.  **Ponownie otwórz Menedżera Certyfikatów** i przejdź do swojego certyfikatu (jak w Kroku 1).
2.  Kliknij prawym przyciskiem myszy $\rightarrow$ **Wszystkie zadania** $\rightarrow$ **Eksportuj**.
3.  **Kreator Eksportu Certyfikatów:**
      * Kliknij **Dalej**.
      * **Ważne\!** Wybierz opcję: **Tak, eksportuj klucz prywatny**. (Jeśli ta opcja jest wyszarzona, klucz jest nieeksportowalny).
      * Wybierz format **Wymiana informacji osobistych – PKCS \#12 (.PFX)**.
      * **Ustaw hasło** — jest to klucz do zabezpieczenia pliku $*.pfx$. Zapamiętaj je\!
      * Zapisz plik (np. `kopia_zapasowa.pfx`).

**Wynik:** Otrzymasz plik **`kopia_zapasowa.pfx`**, który zawiera zarówno certyfikat, jak i klucz prywatny, zaszyfrowane hasłem.

### 2B. Konwersja PFX na KEY za pomocą OpenSSL

Aby wyodrębnić klucz prywatny w formacie $*.key$ (PEM), musisz użyć narzędzia **OpenSSL** (musisz je zainstalować, jeśli go nie masz).

**Użyj poniższego polecenia w wierszu poleceń (cmd) lub PowerShell, będąc w katalogu, gdzie masz OpenSSL (lub mając dodaną ścieżkę do PATH):**

```cmd
openssl pkcs12 -in kopia_zapasowa.pfx -nocerts -out klucz_prywatny.key
```

  * System poprosi Cię o podanie **hasła** do pliku $*.pfx$ (tego, które ustawiłeś w punkcie 2A).
  * Następnie poprosi Cię o **nowe hasło** dla klucza prywatnego ($*.key$), a następnie o jego potwierdzenie.

**Wynik:** Otrzymasz plik **`klucz_prywatny.key`**, który zawiera klucz prywatny w formacie PEM.

-----

## 💡 Podsumowanie Roli OEM

Fakt posiadania Windows 10 w wersji OEM (licencja preinstalowana) **nie ma bezpośredniego wpływu** na Twoje własne certyfikaty i klucze prywatne. 
Certyfikaty systemowe i klucze licencyjne używane przez producenta (OEM) są oddzielne i zazwyczaj nie są dostępne do eksportu przez użytkownika. Procedura eksportu dotyczy **Twoich certyfikatów**, 
które sam zainstalowałeś lub które zostały wygenerowane przez aplikację.


