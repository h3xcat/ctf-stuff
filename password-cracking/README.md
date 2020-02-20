# Summary
The scripts are made based on the idea of linux pipes. It accepts input from stdin and outputs to stdout.

# filter-len.py \<len\>

Filters out words that are greater than the specified length. I'd recommend using this only to filter out really long words (>25). I seen some passwords from NCL up to 19 characters in length.

# filter-keywords.py [\<keyword-file\> ...]

Filters out words that are not part of specified keyword file. You can also specify multiple keyword files.

# filter-alphanum.py

Filters out any words that contains special characters and spaces. Words that only contain letters and numbers are going to get outputted.

# leatspeak.py

Generates word variations of leatspeak. I'd recommend using this with wordlist containing short words.

# cases.py

Generates word variations by switching letter cases. This generates even more data than `leatspeak.py`, so use it with care.

# string-gen.py \<pattern\> [\<wordlist\> ...]

Generates set of strings based on given pattern. The pattern syntax is similar to regex. It's also capable of using wordlist in the pattern by specifying \0 \1 \2 ... within the pattern.
`./string-gen.py "SKY-FLAG-\d{4}"`

# strip-accent.py

Removes accents from strings and replaces them with regular ASCII representation.

---
# Examples

* `cat wordlist/rockyou | ./filter-alphanum.py | ./filter-keywords.py keywords/countries | ./leatspeak.py > wordlist/countries` 
Extracts all country related passwords from rockyou wordlist and creates new wordlist with leatspeak variation.

* `./web-scrape.py "https://en.wikipedia.org/wiki/List_of_Law_%26_Order:_Special_Victims_Unit_episodes" | ./string-gen.py "\0\d\d" - | hashcat -m 0 ./law.hashes`
Generates wordlist from wikipedia page with 2 digits appened. Then the wordlist is piped to hashcat.