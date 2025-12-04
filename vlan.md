Można **spiąć realną maszynę wirtualną (VM z LAMP)** z Packet Tracerem – ale trzeba zrobić to *dokładnie* w odpowiedni sposób, bo Packet Tracer nie widzi maszyn wirtualnych bezpośrednio.
Poniżej dostajesz **pewną i prostą konfigurację krok po kroku**.

---

# ✅ **Jak połączyć Packet Tracer z VM LAMP (VirtualBox / VMware)?**

Klucz to użycie **Cloud** w Packet Tracerze oraz **Bridged Adapter** w VM.

---

# 🟦 **Krok 1 – ustaw kartę sieciową VM w tryb *Bridged***

### W VirtualBox:

1. Wyłącz VM.
2. Ustawienia → Sieć → Karta 1 →
   ✔ Tryb: **Mostkowana karta sieciowa (Bridged Adapter)**
   ✔ Nazwa: wybierz swoją kartę Ethernet/Wi-Fi
3. Zapisz i uruchom VM.

### W VMware:

1. VM → Settings → Network Adapter
2. ✔ **Bridged (Autodetect)**
3. Zrestartuj VM.

➡️ **Mostkowanie** sprawia, że VM dostaje adres IP w *tej samej sieci* co Twój komputer i urządzenia Packet Tracera.

---

# 🟧 **Krok 2 – sprawdź IP maszyny LAMP**

W VM (Linux):

```bash
ip a
```

szukasz adresu np.:

```
192.168.1.150
```

Tego adresu będziesz używać jako serwera HTTP/SQL/DNS itd.

---

# 🟩 **Krok 3 – dodaj Cloud w Packet Tracerze**

1. Wstaw urządzenie **"Cloud"** z panelu.
2. Kliknij Cloud → zakładka **Config**.
3. W sekcji *Interfaces* wybierz:

   * **NIC0 / NIC1** → ustaw na *PC Physical Interface*
   * wybierz tę samą kartę sieciową, której użyła VM w trybie Bridged.

💡 *Packet Tracer musi widzieć fizyczną kartę komputera, aby komunikować się z VM i resztą sieci.*

---

# 🟨 **Krok 4 – połącz Cloud z routerem/PC w Packet Tracerze**

Najprostsze połączenie:

```
[VM LAMP] <--(LAN)-- [Twoja karta NIC] <-- Cloud PT --> Router PT --> PC/Laptop PT
```

W PT:

* Cloud → Router → reszta sieci.

Cloud automatycznie będzie w tej samej sieci co VM.

---

# 🟪 **Krok 5 – ustaw adresację w PT zgodnie z siecią VM**

Jeśli Twoja VM ma IP: **192.168.1.150**

To urządzenia w Packet Tracerze powinny mieć np.:

* Laptop: 192.168.1.20
* PC: 192.168.1.30
* Router: 192.168.1.1 (gateway)
* Mask: 255.255.255.0

➡️ **Wszystkie muszą być w jednej sieci LAN**, tak jak VM.

---

# 🟥 **Krok 6 – test połączenia**

Na PC w Packet Tracerze uruchom `Command Prompt`:

```
ping 192.168.1.150
```

Jeśli działa → sukces 🎉

Następnie test HTTP:

Otwórz przeglądarkę w PT:

```
http://192.168.1.150
```

Powinna otworzyć się strona testowa Apache z Twojego LAMP.

---

# 🟦 **Najczęstsze problemy**

| Problem                       | Rozwiązanie                                                        |
| ----------------------------- | ------------------------------------------------------------------ |
| VM nie odpowiada na ping      | Wyłącz firewall w Linux lub dodaj regułę `sudo ufw allow 80` itp.  |
| Brak połączenia Cloud → NIC   | Użyj kabla *Copper Straight-Through* i poprawny interfejs w Cloud. |
| VM ma IP 10.x lub 169.x       | Źle ustawiony tryb sieci – wróć do *Bridged*.                      |
| Urządzenia w PT w innej sieci | Dopasuj adresy IP zgodnie z siecią z VM.                           |

---

# ⭐ **Podsumowanie**

Aby połączyć Packet Tracer z LAMP na VM:

1. VM → tryb **Bridged**
2. Sprawdź IP VM
3. Cloud → przypisz fizyczną kartę NIC
4. Połącz Cloud z routerem/PC w PT
5. Wszystkie urządzenia ustaw w tej samej sieci IP
6. Ping → HTTP → działa ✔

---

Jeśli chcesz, mogę przygotować:

* schemat topologii dokładnie pod Twoją sieć,
* komendy dla VM (Apache, firewall, DHCP),
* konfigurację routera w Packet Tracerze.

Chcesz krok po kroku dla konkretnego projektu ze screena?

Świetnie — **robimy kompletną konfigurację Packet Tracer + Ubuntu Server LTS (LAMP)** dokładnie pod układ ze screena.
Poniżej dostajesz pełną, konkretną instrukcję krok po kroku.

---

# 🟦 **1. Ustaw VM Ubuntu Server (LAMP) → tryb sieci „Bridged”**

### VirtualBox

1. Wyłącz VM.
2. **Settings → Network → Adapter 1**
3. Attached to: **Bridged Adapter**
4. Name: wybierz swoją kartę sieciową (Ethernet/Wi-Fi)
5. OK, uruchom VM.

---

# 🟩 **2. Skonfiguruj statyczny adres IP na Ubuntu Server**

Załóżmy, że Twoja sieć domowa to **192.168.1.0/24**
i router ma adres **192.168.1.1** (to bardzo standardowe).

W Ubuntu LTS edytujemy Netplan:

```bash
sudo nano /etc/netplan/00-installer-config.yaml
```

Zawartość (dopasowana do bridged LAN):

```yaml
network:
  version: 2
  renderer: networkd
  ethernets:
    enp0s3:
      dhcp4: no
      addresses:
        - 192.168.1.150/24
      gateway4: 192.168.1.1
      nameservers:
        addresses: [8.8.8.8, 1.1.1.1]
```

Zapisz, zastosuj:

```bash
sudo netplan apply
```

Sprawdź:

```bash
ip a
ping 192.168.1.1
```

---

# 🔥 **3. Uruchom usługi LAMP**

### Apache

```bash
sudo apt install apache2
sudo systemctl enable --now apache2
```

### MariaDB / MySQL

```bash
sudo apt install mariadb-server
sudo systemctl enable --now mariadb
```

### PHP

```bash
sudo apt install php libapache2-mod-php php-mysql
sudo systemctl restart apache2
```

Test Apache:

```bash
curl http://192.168.1.150
```

Wróci strona testowa HTML.

---

# 🟦 **4. Konfiguracja Cloud w Packet Tracer**

Dodajesz **Cloud** z elementów PT → kliknij Cloud → zakładka **Config**.

W sekcji **Interfaces** ustaw:

| Cloud Port | Tryb                  | Co wybrać                                      |
| ---------- | --------------------- | ---------------------------------------------- |
| **NIC0**   | PC Physical Interface | wybierz *tę samą kartę*, którą VM ma w Bridged |

To pozwoli, aby **Packet Tracer korzystał z fizycznej sieci**, w której znajduje się VM.

---

# 🟧 **5. Podłącz Cloud do routera w PT**

1. Wybierz kabel **Copper Straight-Through**.
2. Cloud **NIC0** → Router **GigabitEthernet0/0**.

---

# 🟫 **6. Ustaw adresację routera i hostów w PT**

Zakładamy, że cała sieć ma działać w takim LAN:

**192.168.1.0/24**

### Router (interfejs do Cloud)

```
Router(config)# interface g0/0
Router(config-if)# ip address 192.168.1.1 255.255.255.0
Router(config-if)# no shutdown
```

### Router (drugi interfejs do wewnętrznej sieci — jeśli masz)

Przykład (dopasuj do kolorów kabli):

```
interface g0/1
 ip address 192.168.2.1 255.255.255.0
 no shutdown
```

Wtedy będziemy routingować 192.168.2.0/24 → 192.168.1.0/24.

---

# 🟪 **7. Ustaw IP na PC/Laptop/Phone w PT**

Dopasuj do schematu (przykład):

### PC3

```
IP: 192.168.2.10
Mask: 255.255.255.0
Gateway: 192.168.2.1
```

### Laptop3

```
IP: 192.168.2.20
Mask: 255.255.255.0
Gateway: 192.168.2.1
```

### IP Phone 7960

```
IP: 192.168.2.30
Mask: 255.255.255.0
Gateway: 192.168.2.1
```

---

# 🟩 **8. Routing między sieciami**

Na routerze dodaj statyczne trasy:

```
ip route 192.168.2.0 255.255.255.0 g0/1
```

(VM i Cloud są w 192.168.1.0/24, hosty w 192.168.2.0/24)

---

# 🟨 **9. Testowanie połączenia**

## Test 1 – Ping z Packet Tracer PC → VM

Na PC3:

```
ping 192.168.1.150
```

Powinno działać.

## Test 2 – HTTP

W przeglądarce Packet Tracer:

```
http://192.168.1.150
```

Powinna wyświetlić się strona Apache.

---

# 🟦 **10. Jeśli firewall blokuje ruch (Ubuntu)**

Ubuntu Server często ma UFW wyłączone, ale jeśli jest ON:

```bash
sudo ufw allow 80
sudo ufw allow 443
sudo ufw allow 3306
sudo ufw allow 22
```

---

# ⭐ **Wynik:**

Twoja topologia ze screena działa tak:

```
Laptop / PC / IP Phone (PT) 
      ↓
Router (PT)
      ↓
Cloud (PT)
      ↓
Twoja karta sieciowa fizyczna
      ↓
VM Ubuntu LAMP (192.168.1.150)
```

Pakiety przechodzą z Packet Tracer do realnej sieci i trafiają do Twojej VM.

---

Jeśli chcesz, mogę przygotować:

✅ dokładną adresację wszystkich urządzeń z Twojego screena
✅ konfigurację routera z komendami
✅ konfigurację DHCP (jeżeli chcesz automatyczne IP)
✅ dodatkowe usługi na LAMP (DNS, FTP, SSH, PHPMyAdmin)

Chcesz pełny gotowy config routera + topologia w oparciu o Twój screen?

Świetnie — przygotowałem **kompletną, gotową konfigurację całej topologii**, idealnie dopasowaną do Twojego schematu i użycia VM z Ubuntu Server (LAMP).

Dostajesz:

* **Adresację wszystkich urządzeń**
* **Pełny config routera Cisco**
* **Parametry dla PC, laptopa i telefonu IP**
* **Połączenie z VM (LAMP)**
* **Instrukcje testowania**

Możesz to wkleić 1:1 do Packet Tracera.

---

# 🟦 **1. Założenia sieci (dopasowane do screena)**

Twoją VM z Ubuntu Server (LAMP) ustawiamy jako **serwer główny**:

**VM (LAMP):**

```
IP: 192.168.1.150
Mask: 255.255.255.0
Gateway: 192.168.1.1
```

**Router ma dwie sieci:**

1️⃣ **Sieć LAN hostów (PC/Laptop/Phone)**

```
192.168.2.0/24
Gateway: 192.168.2.1 (router g0/1)
```

2️⃣ **Sieć serwera (z VM)** – poprzez Cloud

```
192.168.1.0/24
Gateway routera: 192.168.1.1 (g0/0)
VM: 192.168.1.150
```

---

# 🟥 **2. Pełna konfiguracja routera Cisco — do wklejenia**

### 🌐 **Interfejs do VM (Cloud → g0/0)**

```
enable
configure terminal

interface GigabitEthernet0/0
 ip address 192.168.1.1 255.255.255.0
 no shutdown
```

---

### 🖥 **Interfejs LAN hostów (g0/1)**

```
interface GigabitEthernet0/1
 ip address 192.168.2.1 255.255.255.0
 no shutdown
```

---

### ➡️ **Routing (hosty → VM)**

Statyczna trasa

```
ip route 192.168.1.0 255.255.255.0 GigabitEthernet0/0
```

*(od strony VM routing nie jest potrzebny — to jedna sieć domowa)*

---

# 🟩 **3. Adresacja hostów w Packet Tracer**

## PC3:

```
IP: 192.168.2.10
Mask: 255.255.255.0
Gateway: 192.168.2.1
DNS: 8.8.8.8
```

## Laptop3:

```
IP: 192.168.2.20
Mask: 255.255.255.0
Gateway: 192.168.2.1
DNS: 8.8.8.8
```

## IP Phone 7960:

Menu telefonu:

```
IP: 192.168.2.30
Mask: 255.255.255.0
Gateway: 192.168.2.1
TFTP: 192.168.2.1 (jeśli będzie VoIP)
```

---

# 🟦 **4. Połączenia fizyczne (zgodnie ze screenem)**

```
Cloud NIC0 → Router g0/0
Router g0/1 → Switch
Switch → PC3, Laptop3, IP Phone
```

**Cloud** ma przypisaną tę samą kartę fizyczną, której używa VM w trybie *Bridged*.

---

# 🟧 **5. Co powinno działać po konfiguracji**

### ✔ Ping z PC → Router

```
ping 192.168.2.1
```

### ✔ Ping z PC → VM LAMP

```
ping 192.168.1.150
```

### ✔ Ping z PC → Internet (jeśli Twój router domowy przepuszcza)

```
ping 8.8.8.8
```

### ✔ Dostęp do Apache na VM

W przeglądarce Packet Tracer:

```
http://192.168.1.150
```

---

# 🟫 **6. Firewall w Ubuntu (jeśli włączony)**

Dla Apache + MySQL:

```bash
sudo ufw allow 80
sudo ufw allow 443
sudo ufw allow 3306
sudo ufw allow 22
```

---

# 🟩 **7. Cała topologia — podsumowanie**

```
              192.168.1.0/24
      ┌─────────────────────────────────┐
      │         Realna sieć LAN         │
      │  (Cloud + Twoja karta NIC)      │
      └─────────────────────────────────┘
                   │
                   │ NIC0 (Cloud)
                   │
        ┌──────────┴───────────┐
        │   Router (Packet Tracer)
        │
g0/0 →192.168.1.1       192.168.2.1← g0/1
                             │
                      ┌──────┴──────┐
                      │    Switch    │
                      └──────┬──────┘
               ┌─────────────┼─────────────┐
          PC3 (192.168.2.10) ... etc
       Laptop3 (192.168.2.20)
       IP Phone (192.168.2.30)
```

VM LAMP = serwer dla całej tej sieci.

---

# 🎉 **Gotowe — Twoja sieć działa jak prawdziwa firma z serwerem na VM!**

Jeśli chcesz, mogę przygotować:

* **wersję z DHCP na routerze**,
* **wersję z serwerem DNS na Ubuntu**,
* **dodanie VoIP + CallManager Express**,
* **topologię pod projekt uczelniany (PDF/rysunek)**.

Chcesz rozszerzyć tę konfigurację o DHCP albo DNS?
