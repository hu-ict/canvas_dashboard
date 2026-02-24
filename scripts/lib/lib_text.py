import re


def get_extracted_text(text):
    text_lu_result = []
    text_parts = []
    # print("GC31 -", text)
    if text.count("@") > 1:
        text_part_list = text.strip().split("@")
        for text_part in text_part_list:
            if len(text_part) > 0 and text_part[0] != "@":
                text_parts.append("@" + text_part)
    else:
        text_parts.append(text)
    # print("GC32 -", text_parts)
    for text_part in text_parts:
        # print("GC33 -", text_part)
        # Vind alle woorden die beginnen met @
        at_sign_words = [woord[1:] for woord in re.findall(r'@\w+', text_part)]
        if len(at_sign_words) == 0:
            break
        # print("GC34 -", at_sign_words)
        # Verwijder deze woorden inclusief eventuele spatie ervoor
        aangepaste_tekst = re.sub(r'\s?@\w+', '', text_part)
        # Extra spaties opruimen
        aangepaste_tekst = re.sub(r'\s+', ' ', aangepaste_tekst).strip()
        if len(aangepaste_tekst) > 0:
            if aangepaste_tekst[0] == "-":
                positive_neutral_negative = "-"
                aangepaste_tekst = aangepaste_tekst[1:].strip()
            elif aangepaste_tekst[0] == "+":
                positive_neutral_negative = "+"
                aangepaste_tekst = aangepaste_tekst[1:].strip()
            else:
                positive_neutral_negative = "N"
        else:
            positive_neutral_negative = "N"
        text_lu_result.append({"lu": at_sign_words[0], "positive_neutral_negative": positive_neutral_negative, "text": aangepaste_tekst})
    return text_lu_result