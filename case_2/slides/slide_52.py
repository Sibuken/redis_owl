def creates_speakers() -> list[Speaker]:
    speakers = []
    counter_id = 1
    for language in BookLanguageEnum:
        for _ in range(3):
            slug = f"{language.value}_speaker_{counter_id}"
            speaker = Speaker(
                id=counter_id,
                slug=slug,
                active=True,
                name={"eng": slug},
                is_recommended=True,
                extra_params={},
                book_language=language.value,
            )
            speakers.append(speaker)
            counter_id += 1

    return speakers
