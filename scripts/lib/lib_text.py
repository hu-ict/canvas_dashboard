import re

REG_EX = "(?i)@LU\s*\d+\s*[+-]?"
# REG_EX = "@LU\s*\d+\s*"
# REG_EX = "@LU"
REG_EX_ALG = "@\w+"

def get_lu_from_extracted_text(text):
    text_lu_result = []
    print("LTXT03 -", text)
    at_sign_words = [woord[1:] for woord in re.findall(REG_EX_ALG, text)]
    print("LTXT05 -", at_sign_words)
    return at_sign_words


def get_extracted_text(text):
    text_lu_result = []
    text_parts = []
    # if text[0] != "@":
    #     print("LTXT31 -", text)
    if text.count("@") > 0:
        text_part_list = text.strip().split("@")
        for text_part in text_part_list:
            if len(text_part) > 0 and text_part[0:2].upper() == "LU":
                text_parts.append("@" + text_part)
    else:
        text_parts.append(text)
    # print("LTXT32 -", text_parts)
    for text_part in text_parts:
        # print("LTXT33 -", text_part)
        # Vind alle woorden die beginnen met @
        # print("LTXT34 -", re.findall(REG_EX, text_part))
        at_sign_words = [woord[1:] for woord in re.findall(REG_EX, text_part)]
        if len(at_sign_words) == 0:
            continue
        # print("LTXT35 -", at_sign_words)
        # Verwijder deze woorden inclusief eventuele spatie ervoor
        aangepaste_tekst = re.sub(REG_EX, '', text_part)
        # Extra spaties opruimen
        aangepaste_tekst = aangepaste_tekst.strip()
        at_sign_words[0] = at_sign_words[0].upper().replace(" ", "")
        if at_sign_words[0][-1] == "-":
            positive_neutral_negative = "-"
            at_sign_words[0] = at_sign_words[0][:-1]
        elif at_sign_words[0][-1] == "+":
            positive_neutral_negative = "+"
            at_sign_words[0] = at_sign_words[0][:-1]
        else:
            positive_neutral_negative = "N"
        text_lu_result.append({"lu": at_sign_words[0], "positive_neutral_negative": positive_neutral_negative, "text": aangepaste_tekst})
    return text_lu_result
