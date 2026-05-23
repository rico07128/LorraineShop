import os
import polib
import time
import random
import deepl

# -------------------------------------------------------------------
# 1) CONFIGURATION
# -------------------------------------------------------------------

LOCALE_DIR = "locale"
LANGUAGES = ["en", "es", "de", "it", "ja"]

# Mets ta clé DeepL ici
DEEPL_API_KEY = "699eea0a-88de-4aac-bc18-75a30cc1f9b0:fx"
translator = deepl.Translator(DEEPL_API_KEY)

# Dictionnaire e-commerce intelligent
SMART_ECOMMERCE_TRANSLATIONS = {
    "Commander": {
        "en": "Checkout",
        "es": "Pagar",
        "de": "Zur Kasse",
        "it": "Checkout",
        "ja": "購入手続きへ",
    },
    "Panier": {
        "en": "Cart",
        "es": "Carrito",
        "de": "Warenkorb",
        "it": "Carrello",
        "ja": "カート",
    },
    "Ajouter au panier": {
        "en": "Add to cart",
        "es": "Añadir al carrito",
        "de": "In den Warenkorb",
        "it": "Aggiungi al carrello",
        "ja": "カートに追加",
    },
    "Boutique": {
        "en": "Shop",
        "es": "Tienda",
        "de": "Shop",
        "it": "Negozio",
        "ja": "ショップ",
    },
    "Voir": {"en": "View", "es": "Ver", "de": "Ansehen", "it": "Vedi", "ja": "見る"},
}

# -------------------------------------------------------------------
# 2) FONCTION DE TRADUCTION
# -------------------------------------------------------------------

def smart_translate(msgid, lang):
    # Ne pas traduire les chaînes système Django
    if "%" in msgid or "{" in msgid or "}" in msgid:
        return msgid

    # Dictionnaire e-commerce
    if msgid in SMART_ECOMMERCE_TRANSLATIONS:
        return SMART_ECOMMERCE_TRANSLATIONS[msgid][lang]

    # DeepL exige des codes spécifiques
    deepl_lang = {
        "en": "EN-US",
        "es": "ES",
        "de": "DE",
        "it": "IT",
        "ja": "JA",
    }.get(lang, lang.upper())

    # Tentatives DeepL
    for attempt in range(5):
        try:
            result = translator.translate_text(msgid, target_lang=deepl_lang)
            return result.text
        except Exception as e:
            print(f"⚠️ Erreur DeepL (tentative {attempt+1}/5) : {e}")
            time.sleep(1 + random.random() * 2)

    print(f"❌ DeepL a échoué pour : {msgid} → fallback = msgid")
    return msgid


# -------------------------------------------------------------------
# 3) TRAITEMENT DES FICHIERS .PO
# -------------------------------------------------------------------

def translate_po_files():
    for lang in LANGUAGES:
        po_path = os.path.join(LOCALE_DIR, lang, "LC_MESSAGES", "django.po")

        if not os.path.exists(po_path):
            print(f"❌ Fichier introuvable : {po_path}")
            continue

        print(f"\n🔄 Traitement : {po_path}")
        po = polib.pofile(po_path)

        for entry in po:
            if entry.msgstr.strip() == "" and entry.msgid.strip() != "":
                entry.msgstr = smart_translate(entry.msgid, lang)
                print(f"✔ {entry.msgid} → {entry.msgstr}")

        po.save()
        print(f"💾 Sauvegardé : {po_path}")

# -------------------------------------------------------------------
# 4) LANCEMENT
# -------------------------------------------------------------------

if __name__ == "__main__":
    translate_po_files()
    print("\n🎉 Traduction intelligente terminée !")
