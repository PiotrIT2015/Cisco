Jasne! Wyjaśnię krok po kroku, jak w Ubuntu stworzyć lokalną domenę i adres e-mail przy użyciu `mailutils` i terminala. Zakładam, że chcesz skonfigurować **lokalny serwer pocztowy** dla testów lub prostego użytku – nie publiczny serwer mailowy (to wymaga dodatkowej konfiguracji i np. Postfixa z DNS/MX).

---

### 1. Instalacja `mailutils`

`mailutils` to pakiet umożliwiający wysyłanie i odbieranie maili z terminala. W Ubuntu instalacja wygląda tak:

```bash
sudo apt update
sudo apt install mailutils
```

Podczas instalacji może pojawić się okienko konfiguracji **Postfixa** (który jest używany przez `mailutils`):

* Wybierz **Internet Site** (jeśli chcesz, żeby lokalny system działał jako serwer pocztowy).
* Wprowadź **system mail name** – np. `mojadomena.local`.

---

### 2. Konfiguracja lokalnej domeny

Jeśli chcesz wysyłać maila np. na `user@mojadomena.local`, musisz dodać użytkownika w systemie:

```bash
sudo adduser user
```

Podczas tworzenia ustawisz hasło użytkownika – będzie ono potrzebne do logowania lokalnego.
Ten użytkownik automatycznie będzie obsługiwał adres e-mail `user@mojadomena.local`.

> W systemie Linux adres e-mail lokalnego użytkownika wygląda zwykle tak: `user@hostname`.
> `hostname` możesz sprawdzić poleceniem:
>
> ```bash
> hostname
> ```

Jeśli chcesz, możesz zmienić hostname na swoją domenę lokalną:

```bash
sudo hostnamectl set-hostname mojadomena.local
```

---

### 3. Wysyłanie e-maili przez terminal

Aby wysłać maila:

```bash
echo "Treść wiadomości" | mail -s "Temat wiadomości" odbiorca@example.com
```

Przykład lokalny:

```bash
echo "Cześć, to test" | mail -s "Testowy mail" user@mojadomena.local
```

* `-s` – temat maila
* `odbiorca@example.com` – adres e-mail odbiorcy

---

### 4. Odbieranie maili w terminalu

Aby sprawdzić skrzynkę użytkownika:

```bash
mail
```

* W terminalu pojawi się lista wiadomości.
* Numery wiadomości możesz czytać poleceniem np.: `1` (i Enter).
* `d` usuwa wiadomość, `q` wychodzi.

---

### 5. Dodatkowe uwagi

* To działa **lokalnie** na Ubuntu – maile nie będą wychodzić na Internet, dopóki nie skonfigurujesz prawdziwego serwera SMTP (np. Postfix z MX i rekordami DNS).
* Jeśli planujesz wysyłkę na zewnętrzne adresy, będziesz musiał skonfigurować Postfix + uwierzytelnianie SMTP (np. przez Gmail, SendGrid lub własny serwer).

---

Jeśli chcesz, mogę zrobić dla Ciebie **kompletny mini-przewodnik krok po kroku od zera**, żeby mieć w Ubuntu działającą lokalną domenę z własnym mailem, którą można testować z terminala i przeglądarki.

Chcesz, żebym to przygotował?

Dobrze widzę, co się dzieje: w WSL (Windows Subsystem for Linux) domyślnie **nie działa pełny serwer pocztowy** tak jak w typowym Ubuntu. `mailutils` działa, ale nie ma działającego demona SMTP ani lokalnego systemu kolejkowania poczty, więc wysyłanie maili do samego siebie nic nie daje – stąd `No mail for piotr`.

Kilka kluczowych punktów i rozwiązań:

---

### 1️⃣ `hostnamectl` w WSL

* W WSL `hostnamectl` zadziała, ale zmiana hostname nie wpływa na działanie lokalnej poczty w taki sam sposób jak w normalnym Linuxie.
* To nie jest problem – można zostawić `krk.local`.

---

### 2️⃣ Dlaczego `mail` nic nie pokazuje

* `mail` odczytuje **lokalną skrzynkę pocztową w `/var/mail/username`**.
* W normalnym Ubuntu Postfix (lub inny MTA) odbiera wiadomości lokalnie i zapisuje je tam.
* W WSL **Postfix nie działa domyślnie**, więc żadne maile nie trafiają do `/var/mail/piotr`.

---

### 3️⃣ Jak przetestować wysyłanie maili w WSL

Masz dwie opcje:

#### a) Skonfigurować Postfix (lokalny lub przez SMTP)

1. Zainstaluj Postfix:

```bash
sudo apt install postfix
```

2. Wybierz **Local only** (jeśli testujesz lokalnie) lub **Internet Site** (jeśli chcesz wysyłać na zewnątrz).
3. Teraz lokalne maile `echo "test" | mail -s "test" piotr@krk.local` będą trafiać do `/var/mail/piotr` i `mail` powinno je pokazać.

#### b) Wysyłanie maili przez zewnętrzny serwer SMTP

* W WSL wygodniej jest użyć np. Gmaila lub innego SMTP do wysyłania maili, np. przez `msmtp` lub `swaks`.
* Wtedy maile można wysyłać na dowolny adres, a nie tylko lokalny.

---

### 4️⃣ Wskazówka do testów lokalnych

* Po zainstalowaniu Postfix w WSL, sprawdź logi:

```bash
tail -f /var/log/mail.log
```

* Wysyłanie maili:

```bash
echo "Test" | mail -s "Test" piotr
mail
```

Teraz powinno działać.

---

Jeśli chcesz, mogę przygotować **dokładną instrukcję krok po kroku dla WSL**, żeby lokalny `mail` w końcu działał i wyświetlał wiadomości.

Chcesz, żebym to zrobił?
