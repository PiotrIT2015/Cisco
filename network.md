Bardzo szczegółowe! W tej wiadomości zawarłeś/aś pytania dotyczące **DHCP, routingu statycznego/dynamicznego, konfiguracji EtherChannel/LACP** oraz **DNS/diagnostyki sieci (`curl`, `dig`)** i **konfiguracji OSPF**.

Oto Twoje pytania i odpowiedzi zebrane w jednym miejscu.

---

## 🧭 **Zestawienie Zagadnień Sieciowych**

### **1. DHCP: Adres IP i Brama Domyślna**

DHCP (Dynamic Host Configuration Protocol) i brama domyślna są kluczowe, ponieważ:

* **DHCP** automatycznie przydziela urządzeniom adres IP, maskę podsieci, serwery DNS oraz najważniejsze: **adres bramy domyślnej (`default-router`)**.
* **Brama domyślna** (Default Gateway) to adres **routera**, który jest pierwszym punktem wyjścia dla każdego pakietu kierowanego do sieci **innej** niż lokalna. Bez niej host nie może komunikować się z Internetem ani innymi podsieciami.

### **2. DHCP: Komendy Cisco**

| Komenda Cisco | Opis Funkcji |
| :--- | :--- |
| `ip dhcp excluded-address 192.168.1.1 192.168.1.10` | Rezerwuje adresy IP z zakresu 192.168.1.1 do 192.168.1.10. Zapobiega ich dynamicznemu przydzieleniu, pozostawiając je dla urządzeń ze stałym IP (serwery, drukarki, routery). |
| `ip dhcp pool LAN` | Tworzy nową pulę DHCP o nazwie **LAN**. Następne komendy konfigurują ustawienia tej puli (sieć, brama, DNS). |
| `network 192.168.1.0 255.255.255.0` | Definiuje adres sieci i maskę dla puli LAN. |
| `default-router 192.168.1.1` | Ustawia bramę domyślną dla wszystkich klientów z puli LAN. |

---

### **3. Routing: Statyczny vs. Dynamiczny**

| Cecha | **Routing Statyczny** | **Routing Dynamiczny** (np. OSPF, RIP, EIGRP) |
| :--- | :--- | :--- |
| **Mechanizm** | Trasy konfigurowane ręcznie przez administratora (`ip route`). | Trasy uczone i automatycznie wymieniane między routerami za pomocą protokołów. |
| **Adaptacja do zmian** | Brak; awaria łącza wymaga ręcznej zmiany trasy. | Automatyczna; protokół sam znajduje nową najlepszą ścieżkę. |
| **Zastosowanie** | Małe, stabilne sieci (lub trasa domyślna do Internetu). | Duże i średnie sieci korporacyjne. |

---

### **4. Router-on-a-Stick i Ramki Ethernet**

| Koncept | Rola | Warstwa OSI |
| :--- | :--- | :--- |
| **Ramka (Frame)** | Jednostka danych zawierająca adresy MAC. Służy do przesyłania danych w obrębie tej samej sieci logicznej (VLAN). | 2 (Warstwa łącza danych) |
| **Adresy MAC** | **Adres MAC docelowy** i **źródłowy** – służą do identyfikacji ramki i kierowania jej przez **przełączniki**. | 2 |
| **Router-on-a-Stick** | Technika routingu między VLAN-ami: jeden fizyczny port routera (trunk) obsługuje wiele VLAN-ów za pomocą podinterfejsów i znaczników 802.1Q. | 2 (trunk) i 3 (routing) |

---

### **5. EtherChannel/LACP**

**EtherChannel** (lub LAG/Link Aggregation) łączy wiele fizycznych łączy Ethernet w jedno **logiczne łącze**, aby zwiększyć przepustowość i zapewnić redundancję.

| Komenda Cisco | Opis Funkcji |
| :--- | :--- |
| `channel-group 2 mode active` | Przypisuje interfejs do logicznej grupy numer 2 i aktywuje protokół **LACP** (Link Aggregation Control Protocol) w trybie **aktywnym**. Tryb aktywny inicjuje negocjacje. |
| `show lacp 2 neighbor` | Wyświetla szczegółowe informacje o sąsiednim urządzeniu (przełączniku), z którym próbuje utworzyć EtherChannel za pomocą LACP. |
| **Tryb Pasywny** | Oczekuje, aż sąsiad (skonfigurowany w trybie **aktywnym**) zainicjuje negocjacje LACP. |

---

### **6. Konfiguracja OSPF (Routing Dynamiczny)**

**OSPF (Open Shortest Path First)** jest protokołem routingu stanu łącza.

| Komenda Cisco | Opis Funkcji |
| :--- | :--- |
| `router ospf 1` | **Uruchamia proces OSPF** na routerze z numerem procesu 1. Wszystkie routery w tej samej domenie routingu powinny używać tego samego numeru procesu. |
| `network 172.20.0.1 0.0.0.255 area 0` | Nakazuje routerowi **ogłaszać sieć** (adres IP interfejsu) i interfejs, do którego jest podłączona, w procesie OSPF. Maska odwrócona (`0.0.0.255` dla /24) określa zakres adresów, które zostaną ogłoszone. |

---

### **7. Narzędzia Diagnostyczne (Linux/Unix)**

| Polecenie | Rola | Zastosowanie |
| :--- | :--- | :--- |
| `cat /etc/resolv.conf` | Wyświetla plik konfiguracyjny klienta DNS. | Pokazuje, jakie serwery DNS są używane przez system. |
| `curl -v 8.8.8.8` | Próbuje nawiązać połączenie HTTP/TCP z IP `8.8.8.8` (port 80) i wyświetla szczegóły połączenia. | Testuje łączność TCP do serwera (choć `8.8.8.8` to serwer DNS, więc zwraca błąd 404). |
| `dig www.google.com` | Narzędzie diagnostyczne DNS (Domain Information Groper). | Wysyła zapytanie do serwera DNS o adresy IP (`A`/`AAAA`) dla domeny `www.google.com`. |

---

Chcesz, abym teraz skupił się na konkretnym fragmencie konfiguracji, np. dokładniejszej analizie EtherChannel lub OSPF?