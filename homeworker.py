import wikipedia as wiki
from googletrans import Translator

translator = Translator()


def get_summary(topic: str, lang_to_search: str = 'en', num_sentences: int = 6, num_references: int = 3):
    '''Returns a summary of the given topic searching in the given language, with references
    example:

    get_summary(topic='Sponge Bob', lang_to_search='en', num_sentences=6, num_references=3)
    '''

    translated_topic = translator.translate(
        text=topic,
        src='pt',
        dest=lang_to_search
    )
    wiki.set_lang(lang_to_search)
    summary = wiki.summary(translated_topic.text, sentences=num_sentences)
    summary = translator.translate(
        text=summary,
        src=lang_to_search,
        dest='pt'
    )
    summary = summary.text

    references = []
    page = wiki.page(translated_topic.text)

    try:
        references = page.references[0:num_references]
    except:
        references = 'No references found'

    return {
        'topic': topic,
        'lang_search': lang_to_search,
        'summary': summary,
        'references': references
    }
