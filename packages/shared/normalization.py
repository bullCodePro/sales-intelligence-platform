import re
import unicodedata


LEGAL_SUFFIXES = {
    "inc",
    "llc",
    "ltd",
    "sa",
    "s a",
    "srl",
    "spa",
    "corp",
    "corporation",
    "company",
}


def normalize_company_name(name: str) -> str:
    value = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", " ", value)
    tokens = [token for token in value.split() if token not in LEGAL_SUFFIXES]
    return " ".join(tokens).strip()
