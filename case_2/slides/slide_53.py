def group_speakers(speakers: list[Speaker]) -> dict[str, list[Speaker]]:
    grouped_speakers = collections.defaultdict(list)
    for speaker in speakers:
        book_language = speaker.book_language
        grouped_speakers[book_language].append(speaker)

    return grouped_speakers
