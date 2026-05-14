import polib
from googletrans import Translator
import os

# Dossier où Django génère les fichiers .po
LOCALE_DIR = "locale"

# Langues à traduire
LANGUAGES = ["en", "es", "de", "it", "ja"]

translator = Translator()


def translate_po_files():
    for lang in LANGUAGES:
        po_path = os.path.join(LOCALE_DIR, lang, "LC_MESSAGES", "django.po")

        if not os.path.exists(po_path):
            print(f"❌ Fichier introuvable : {po_path}")
            continue

        print(f"🔄 Traitement : {po_path}")
        po = polib.pofile(po_path)

        for entry in po:
            if entry.msgstr.strip() == "" and entry.msgid.strip() != "":
                try:
                    translated = translator.translate(entry.msgid, dest=lang).text
                    entry.msgstr = translated
                    print(f"✔ {entry.msgid} → {translated}")
                except Exception as e:
                    print(f"⚠ Erreur traduction {entry.msgid}: {e}")

        po.save()
        print(f"💾 Sauvegardé : {po_path}")


if __name__ == "__main__":
    translate_po_files()
    print("🎉 Traduction automatique terminée !")
