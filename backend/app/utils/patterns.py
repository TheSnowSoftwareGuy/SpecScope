import re

CSI_DIVISION_REGEX = re.compile(r"(DIVISION\s+0?1\b|\b01\s\d{2}\s\d{2})", re.IGNORECASE)
ADDENDA_REGEX = re.compile(r"\b(Addendum|Addenda)\b", re.IGNORECASE)
MODAL_VERBS_REGEX = re.compile(r"\b(shall|must|required|contractor(?:\sresponsible)?)\b", re.IGNORECASE)

TOPIC_PATTERNS = {
    "bonds": re.compile(r"\b(bid|performance|payment)\s+bond[s]?\b", re.IGNORECASE),
    "insurance": re.compile(r"\b(insur|liability|workers[’']? compensation)\b", re.IGNORECASE),
    "liquidated_damages": re.compile(r"\bliquidated\s+damages\b|\bLD\b", re.IGNORECASE),
    "submittals": re.compile(r"\bsubmittal[s]?\b", re.IGNORECASE),
    "alternates": re.compile(r"\balternate[s]?\b", re.IGNORECASE),
}