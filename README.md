# Šachová hra v Pythonu pomocí Pygame

Toto je jednoduchá implementace šachové hry pomocí Pygame. Hra umožňuje hrát šachy na desce 8x8 s základním pohybem figurek, včetně propagace pěšců a detekce šachu/šach-matu.

## Funkce
- **Rozložení šachovnice**: Deska je zobrazená s alternativními barvami pro jednotlivá pole.
- **Pohyb figurek**: Standardní pohyb pro každou šachovou figuru.
- **Zvýraznění**: Platné tahy pro vybranou figuru jsou zvýrazněny.
- **Šach/Šach-mat**: Hra detekuje šach a šach-mat.
- **Tahová hra**: Hráči střídají tahy mezi bílými a černými figurkami.

## Požadavky
Pro spuštění této hry potřebujete:
- Python 3.x
- Knihovna Pygame

Pygame nainstalujete příkazem:

```bash
pip install pygame
```

## Instalace a nastavení
1. Naklonujte nebo stáhněte tento repozitář do vašeho počítače.
2. Uložte obrázky pro šachové figurky do složky `images/` uvnitř adresáře projektu. Potřebné soubory obrázků:
   - `b_pawn.png`
   - `b_rook.png`
   - `b_knight.png`
   - `b_bishop.png`
   - `b_queen.png`
   - `b_king.png`
   - `w_pawn.png`
   - `w_rook.png`
   - `w_knight.png`
   - `w_bishop.png`
   - `w_queen.png`
   - `w_king.png`

   Obrázky by měly mít odpovídající velikost (ideálně 64x64 pixelů), aby se správně zobrazily na šachovnici.

3. Spusťte herní skript:

```bash
python main.py
```

## Jak hrát
- Klikněte na figuru, kterou chcete vybrat.
- Jakmile je figura vybrána, klikněte na platné pole, kam ji chcete přesunout.
- Hra střídá tahy mezi bílými a černými.
- Pokud je hráč v šachu-matu, hra skončí a oznámí vítěze.

## Vysvětlení kódu

### Klíčové funkce

- **`draw_board()`**: Kreslí šachovnici s alternativními barvami pro jednotlivá pole.
- **`draw_pieces(board)`**: Kreslí figury na šachovnici podle aktuálního stavu hry.
- **`draw_highlight(moves)`**: Zvýrazňuje platná pole, kam může vybraná figura přesunout.
- **`get_valid_moves(board, piece, pos, check_safety=True)`**: Vrací seznam platných tahů pro danou figuru. Obsahuje logiku pro různé typy figurek (pěšec, věž, jezdec, střelec, dáma, král).
- **`filter_safe_moves(board, moves, pos, color)`**: Filtruje tahy, které by vystavily krále hráče šachu.
- **`is_check(board, color)`**: Kontroluje, zda je král dané barvy v šachu.
- **`is_checkmate(board, color)`**: Kontroluje, zda je hráč v šach-matu.

### Průběh hry

1. Hra inicializuje šachovnici se standardním nastavením figurek.
2. Hlavní smyčka zpracovává události (kliknutí myši) a aktualizuje šachovnici:
   - Figura je vybrána kliknutím na ni.
   - Platné tahy pro vybranou figuru jsou zvýrazněny.
   - Pokud hráč klikne na platné pole, figura se přesune.
   - Po každém tahu hra kontroluje šach-mat a ukončí hru, pokud je detekován šach-mat.
3. Hra střídá tahy mezi bílými a černými hráči.

### Platné tahy
Každá figura má různé pravidla pohybu:
- **Pěšci**: Pohybují se o jedno pole vpřed, nebo o dvě pole z výchozí pozice. Chytají diagonálně.
- **Věže**: Pohybují se horizontálně nebo vertikálně libovolný počet polí.
- **Střelci**: Pohybují se diagonálně libovolný počet polí.
- **Dámy**: Kombinují pohyb věže a střelce.
- **Jezdci**: Pohybují se ve tvaru písmene "L" (dvě pole v jednom směru a jedno pole kolmo).
- **Králové**: Pohybují se o jedno pole v jakémkoli směru.

## Funkce k implementaci (volitelné)
- **Propagace pěšce**: Umožnit pěšcům, aby byli po dosažení poslední řady soupeře povýšeni.
- **Rošáda**: Přidat pohyby pro rošádu mezi králem a věží.
- **En passant**: Implementovat pravidlo en passant pro pěšce.
- **Vrácení tahu**: Implementovat možnost vrácení posledního tahu.
- **Časovač hry**: Přidat časovač pro tahy každého hráče.

## Licence
Tento projekt je licencován pod licencí MIT - podrobnosti naleznete v souboru [LICENSE](LICENSE).
