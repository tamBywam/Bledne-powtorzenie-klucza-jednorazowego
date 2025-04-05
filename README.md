# Szyfr Jednorazowy – Opis i Zadanie

## Zasada działania

Zasadą szyfru jednorazowego jest **niepowtarzalność klucza**.  
Formuły szyfrowania i deszyfrowania:

- `E(k, m) = k ⊕ m`
- `D(k, c) = k ⊕ c`

Jeśli dwie wiadomości są zaszyfrowane tym samym kluczem `k`, to można obliczyć:

- `m1 ⊕ m2 = c1 ⊕ c2`

Znajomość `xor` dwóch wiadomości niesie już pewne informacje, a każda uzyskana informacja jest **z definicji złamaniem szyfru**, nawet jeśli nie prowadzi do całkowitego odszyfrowania tekstu.

## Analiza xor

W zadaniu pokazującym możliwości uzyskania informacji ze znajomości `xor`, założymy, że szyfrowane są **wyłącznie litery i spacje**. Dla uproszczenia można też założyć, że litery są wyłącznie **małe**.

Zakładamy, że cały tekst (angielski) jest kodowany standardowo kodem ASCII:
- Spacja ma numer `32`
- Małe litery: `97–122`

W notacji heksadecymalnej:
- Spacja: `0x00100000`
- Małe litery: `0x011.....`

Wynik operacji `xor`:
- `xor` dwóch liter: zaczyna się od **trzech zer**
- `xor` litery i spacji: zaczyna się od **010**

Znając `m1 ⊕ m2`, jeśli pierwsze trzy bity to `010`, to **jeden ze znaków jest spacją**, więc:

- `m1 ⊕ m2 ⊕ 00100000` daje **drugi ze znaków**, choć nie wiadomo który.

Przykład:
- Jeśli mamy do dyspozycji `m1 ⊕ m2` oraz `m2 ⊕ m3`
  - Jeśli pierwsza para ma spację, a druga nie — spacją jest `m1`, wyliczamy `m2` i `m3`
  - Jeśli obie mają spacje — prawdopodobnie `m2`, wyliczamy pozostałe znaki

Inny przypadek:
- Jeśli `m3 ⊕ m1 = 00000000` → `m1 = m3`
  - Możliwe, że `m1` i `m3` to spacje, a `m2` to jakiś znak

Jeśli znamy więcej przykładów kryptogramów powstałych z użyciem tego samego klucza, to istnieje **duża szansa na odtworzenie dokładnych tekstów**.

---

## Zadanie

Program o nazwie `xor` powinien umożliwiać wywołanie z linii rozkazowej z następującymi opcjami:

- `-p` – przygotowanie tekstu do przykładu działania
- `-e` – szyfrowanie
- `-k` – kryptoanaliza wyłącznie w oparciu o kryptogram

### Nazwy plików:

- `orig.txt`: plik zawierający dowolny tekst
- `plain.txt`: plik z tekstem zawierającym co najmniej kilkanaście linijek równej długości (np. 64)
- `key.txt`: plik zawierający klucz (ciąg dowolnych znaków o wymaganej długości)
- `crypto.txt`: plik z tekstem zaszyfrowanym (każda linijka = operacja `⊕` z kluczem)
- `decrypt.txt`: plik z tekstem odszyfrowanym.  
  Jeśli nie można odszyfrować znaku — należy wstawić **znak podkreślenia** `_`.

> **Uwaga**: pod uwagę będą brane **wyłącznie programy z kryptoanalizą**.
