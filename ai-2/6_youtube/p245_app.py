import deepl
from pathlib import Path
import os

def translate_text_file(input_path, target_lang="KO"):
    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()

    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_lang)

    path = Path(input_path)
    output_path = f'{path.parent}/{path.stem}_번역_{target_lang}{path.suffix}'

    output_path = Path(output_path)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(result.text)

    return output_path

input_path = './data/youtube_download.srt'

translate_file = translate_text_file(input_path)
print(f"- [번역 파일] {translate_file}\n")