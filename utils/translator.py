from deep_translator import GoogleTranslator

async def translate_srt(srt_path, lang_code):
    with open(srt_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    translated_lines = []
    for line in lines:
        if line.strip() and not line[0].isdigit() and "-->" not in line:
            try:
                translated = GoogleTranslator(source='auto', target=lang_code).translate(line.strip())
                translated_lines.append(translated + "\n")
            except:
                translated_lines.append(line)
        else:
            translated_lines.append(line)

    new_path = srt_path.replace(".srt", f"_{lang_code}.srt")
    with open(new_path, "w", encoding="utf-8") as f:
        f.writelines(translated_lines)

    return new_path
