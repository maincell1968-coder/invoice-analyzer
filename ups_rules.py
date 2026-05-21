import os
import re
import json

# Default values for 2026
DEFAULT_RULES = {
    "correzione_indirizzo": 11.40,
    "movimentazione_aggiuntiva": 14.15,
    "pacco_grande": 72.85,
    "peso_eccessivo": 508.45,
    "domicilio_privato": 4.00,
    "correction_fee_min": 1.50,
    "correction_fee_pct": 0.08,
    "correction_fee_threshold": 25.0
}

def load_ups_rules(pdf_path):
    """
    Loads UPS rules from a cached JSON file or parses them from the service guide PDF.
    If the JSON is newer than the PDF, it loads it. Otherwise, it re-parses the PDF.
    """
    json_path = os.path.join(os.path.dirname(pdf_path), "parametri_ups.json")
    
    # 1. Check if we can use the cached JSON
    if os.path.exists(json_path):
        json_mtime = os.path.getmtime(json_path)
        pdf_mtime = os.path.getmtime(pdf_path) if os.path.exists(pdf_path) else 0
        
        if json_mtime > pdf_mtime:
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass # If reading JSON fails, we'll try to re-parse or use defaults

    # 2. If PDF doesn't exist, use defaults
    if not os.path.exists(pdf_path):
        return DEFAULT_RULES

    # 3. Parse PDF
    try:
        import pypdf
        reader = pypdf.PdfReader(pdf_path)
        
        full_text = ""
        for page in reader.pages:
            full_text += page.extract_text() + "\n"
        
        # Replace multiple spaces/newlines with a single space to normalize
        text_norm = re.sub(r'\s+', ' ', full_text)
        
        rules = {}
        
        def get_first_eur_after(text, keyword, max_chars=1000):
            match = re.search(re.escape(keyword), text, re.IGNORECASE)
            if not match:
                return None
            start_idx = match.end()
            sub_text = text[start_idx:start_idx+max_chars]
            eur_match = re.search(r'EUR\s*(\d+,\d{2})', sub_text)
            if eur_match:
                return float(eur_match.group(1).replace(",", "."))
            return None

        # 1. Correzione indirizzo
        rules["correzione_indirizzo"] = get_first_eur_after(text_norm, "Correzione di indirizzo") or get_first_eur_after(text_norm, "Correzione indirizzo") or DEFAULT_RULES["correzione_indirizzo"]

        # 2. Movimentazione aggiuntiva
        rules["movimentazione_aggiuntiva"] = get_first_eur_after(text_norm, "Addebito per movimentazione aggiuntiva") or get_first_eur_after(text_norm, "movimentazione aggiuntiva") or DEFAULT_RULES["movimentazione_aggiuntiva"]

        # 3. Pacco grande
        rules["pacco_grande"] = get_first_eur_after(text_norm, "Sovrapprezzo per pacchi grandi") or get_first_eur_after(text_norm, "pacchi grandi") or DEFAULT_RULES["pacco_grande"]

        # 4. Peso/dimensioni eccessive
        rules["peso_eccessivo"] = get_first_eur_after(text_norm, "Addebito per pacco di peso/ dimensioni eccessive") or get_first_eur_after(text_norm, "Addebito per pacco di peso/dimensioni eccessive") or DEFAULT_RULES["peso_eccessivo"]

        # 5. Domicilio privato
        domicilio_idx = text_norm.find("UPS offre un servizio di consegna a indirizzi sia residenziali che commerciali")
        if domicilio_idx != -1:
            domicilio_sub = text_norm[domicilio_idx:domicilio_idx+1500]
            altri_idx = domicilio_sub.find("Tutti gli altri servizi principali")
            if altri_idx != -1:
                altri_sub = domicilio_sub[altri_idx:]
                eur_match = re.search(r'EUR\s*(\d+,\d{2})', altri_sub)
                if eur_match:
                    rules["domicilio_privato"] = float(eur_match.group(1).replace(",", "."))
                else:
                    rules["domicilio_privato"] = DEFAULT_RULES["domicilio_privato"]
            else:
                rules["domicilio_privato"] = DEFAULT_RULES["domicilio_privato"]
        else:
            rules["domicilio_privato"] = DEFAULT_RULES["domicilio_privato"]

        # 6. Correction Fee rules
        cf_idx = text_norm.lower().find("correzione delle spese di spedizione")
        if cf_idx != -1:
            cf_sub = text_norm[cf_idx:cf_idx+1500]
            
            # Min eur
            min_match = re.search(r'EUR\s*(\d+,\d{2})\s+per\s+spedizione', cf_sub, re.IGNORECASE)
            rules["correction_fee_min"] = float(min_match.group(1).replace(",", ".")) if min_match else DEFAULT_RULES["correction_fee_min"]
            
            # Pct
            pct_match = re.search(r'(\d+)%\s+dell[\'’]importo\s+totale', cf_sub, re.IGNORECASE)
            rules["correction_fee_pct"] = float(pct_match.group(1)) / 100.0 if pct_match else DEFAULT_RULES["correction_fee_pct"]
            
            # Threshold
            thresh_match = re.search(r'pari\s+o\s+superiore\s+al\s+(\d+)%', cf_sub, re.IGNORECASE)
            rules["correction_fee_threshold"] = float(thresh_match.group(1)) if thresh_match else DEFAULT_RULES["correction_fee_threshold"]
        else:
            rules["correction_fee_min"] = DEFAULT_RULES["correction_fee_min"]
            rules["correction_fee_pct"] = DEFAULT_RULES["correction_fee_pct"]
            rules["correction_fee_threshold"] = DEFAULT_RULES["correction_fee_threshold"]

        # Save to JSON for caching
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(rules, f, indent=4, ensure_ascii=False)
            
        return rules
        
    except Exception:
        # If any parsing issue happens, fallback to default 2026 rules
        return DEFAULT_RULES
