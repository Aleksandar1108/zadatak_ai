Za mene je bio najzahtevniji drugi deo zadatka (semantička pretraga za „svemirski vampiri“)**.

Glavni problem je bio što data-manga.csv ima preko 48 hiljada redova, a svaki opis može biti dosta dugačak. Ako bih odmah pustio embedding model na celu bazu, prvi run bi trajao jako dugo i API bi praktično bio neupotrebljiv dok se ne završi računanje. Zato sam odlučio da prvo uradim brzi TF-IDF prefilter — izvučem nekoliko stotina kandidata koji bar u tekstualnom smislu imaju neku vezu sa temom (space, vampire, sci-fi itd.), pa tek onda na tom manjem skupu radim **semantičko rangiranje pomoću paraphrase-multilingual-MiniLM-L12-v2.

Izabrao sam baš taj model jer upit dolazi na srpskom („svemirski vampiri“), a opisi u datasetu su uglavnom na engleskom — multilingual model mi deluje prirodniji izbor od običnog TF-IDF-a sam po sebi, koji ne hvata baš dobro semantiku između jezika.

Još jedna važna odluka bila je keširanje rezultata u backend/cache/. Podaci se ne menjaju svaki dan, pa nema smisla da svaki put kad neko otvori frontend ponovo računamo isto. Dug proces ostaje za prvi run ili kad korisnik eksplicitno klikne „Recompute from files“.

Kod Task 3 sam pazio da srednja_zarada bude računata samo iz train perioda, da ne bih slučajno „procureo“ test podatke u feature engineering. To mi deluje kao mala ali bitna stvar — lako je napraviti model koji izgleda dobro, ali zapravo vara jer koristi informacije koje u realnosti ne bi imao unapred.
