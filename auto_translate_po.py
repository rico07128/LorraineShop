import os
import polib
import time
import random
from googletrans import Translator

# -------------------------------------------------------------------
# 1) CONFIGURATION
# -------------------------------------------------------------------

LOCALE_DIR = "locale"
LANGUAGES = ["en", "es", "de", "it", "ja"]

translator = Translator()

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
# 2) FONCTION DE TRADUCTION SÉCURISÉE
# -------------------------------------------------------------------


def smart_translate(msgid, lang):
    # 1) Ne jamais traduire les chaînes système Django
    if "%" in msgid or "{" in msgid or "}" in msgid:
        return msgid

    # 2) Correction e-commerce prioritaire
    if msgid in SMART_ECOMMERCE_TRANSLATIONS:
        return SMART_ECOMMERCE_TRANSLATIONS[msgid][lang]

    # 3) Tentatives Google Translate (max 5)
    for attempt in range(5):
        try:
            translated = translator.translate(msgid, src="fr", dest=lang).text
            return translated
        except Exception as e:
            print(f"⚠️ Erreur Google (tentative {attempt+1}/5) : {e}")
            time.sleep(1 + random.random() * 2)

    # 4) Fallback si Google échoue
    print(f"❌ Google a échoué pour : {msgid} → fallback = msgid")
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
            # Ne traduire que les msgstr vides
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
