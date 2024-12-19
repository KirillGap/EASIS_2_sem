import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from string import punctuation
from nltk import pos_tag
import pymorphy3
from translate import Translator

translator = Translator(from_lang='english', to_lang='russian')

metadata = {
    "CC": "координирующая конъюнкция",
    "CD": "цифра",
    "DT": "артикль",
    "TO": "предлог to",
    "MD": "модальный глагол",
    "IN": "предлог/подчинительный союз",
    "JJ": "прилагательное",
    "JJR": "прилагательное сравнительное",
    "JJS": "прилагательное в превосходной ",
    "NN": "существительное в единственном числе",
    "NNS": "существительное во множественном числе",
    "NNP": "имя собственное в единственном числе",
    "NNPS": "имя собственное, множественное число",
    "PRP": "местоимение",
    "POS": "притяжательное окончание",
    "PRP$": "местоимение",
    "RB": "наречие",
    "RBR": "наречие в сравнительной степени",
    "RBS": "наречие в превосходной степени",
    "RP": "частица",
    "UH": "междометие",
    "VB": "глагол, базовая форма",
    "VBD": "глагол, прошедшее время",
    "VBG": "глагол, герундий/причастие настоящего времени",
    "VBN": "глагол, причастие прошедшего времени",
    "VBP": "глагол, петь. настоящее, не трехмерное действие",
    "VBZ": "глагол, поющий в 3-м лице. настоящее принимает",
    "WDT": "вопрос, который",
    "WP": "вопрос кто, что",
    "WRB": "вопрос, где, когда",
    "ADJA": "прилагательное, атрибутивное",
    "ADJD": "прилагательное, наречное или предикативное",
    "APPO": "постпозиция",
    "APPR": "предлог; циркумпозиция слева",
    "APPRART": "предлог с артиклем",
    "APZR": "циркумпозиция справа",
    "ART": "определённый или неопределённый артикль",
    "CARD": "количественное числительное",
    "FM": "материал на иностранном языке",
    "ITJ": "междометие",
    "KOKOM": "сравнительный союз",
    "KON": "координирующий союз",
    "KOUI": 'подчинительный союз с "zu" и инфинитивом',
    "KOUS": "подчинительный союз с предложением",
    "NE": "имя собственное",
    "NNE": "имя собственное",
    "PAV": "местоимённое наречие",
    "PROAV": "местоимённое наречие",
    "PDAT": "атрибутивное указательное местоимение",
    "PDS": "замещающее указательное местоимение",
    "PIAT": "атрибутивное неопределённое местоимение без определителя",
    "PIDAT": "атрибутивное неопределённое местоимение с определителем",
    "PIS": "замещающее неопределённое местоимение",
    "PPER": "не-рефлексивное личное местоимение",
    "PPOSAT": "атрибутивное притяжательное местоимение",
    "PPOSS": "замещающее притяжательное местоимение",
    "PRELAT": "атрибутивное относительное местоимение",
    "PRELS": "замещающее относительное местоимение",
    "PRF": "рефлексивное личное местоимение",
    "PTKA": "частица с прилагательным или наречием",
    "PTKANT": "частица для ответа",
    "PTKNEG": "отрицательная частица",
    "PTKVZ": "отделяемая глагольная частица",
    "PTKZU": '"zu" перед инфинитивом',
    "PWAT": "атрибутивное вопросительное местоимение",
    "PWAV": "наречное вопросительное или относительное местоимение",
    "PWS": "замещающее вопросительное местоимение",
    "TRUNC": "остаток слова",
    "VAFIN": "финитный глагол, вспомогательный",
    "VAIMP": "повелительное наклонение, вспомогательное",
    "VAINF": "инфинитив, вспомогательное",
    "VAPP": "причастие прошедшего времени, вспомогательное",
    "VMFIN": "финитный глагол, модальный",
    "VMINF": "инфинитив, модальный",
    "VMPP": "причастие прошедшего времени, модальный",
    "VVFIN": "финитный глагол, полный",
    "VVIMP": "повелительное наклонение, полный",
    "VVINF": "инфинитив, полный",
    "VVIZU": 'инфинитив с "zu", полный',
    "VVPP": "причастие прошедшего времени, полный",
    "XY": "не-слово, содержащее не-букву"
}


def analyze_russian_word(word):
    morph = pymorphy3.MorphAnalyzer()
    parsed_word = morph.parse(word)[0]
    word_info = {
        'word': word,
        'normal_form': parsed_word.normal_form,
        'part_of_speech': parsed_word.tag.POS if not parsed_word.tag.POS in metadata.keys() else metadata.get(parsed_word.tag.POS),
        'case': parsed_word.tag.case,
        'gender': parsed_word.tag.gender,
        'number': parsed_word.tag.number,
        'aspect': parsed_word.tag.aspect,
        'tense': parsed_word.tag.tense,
        'voice': parsed_word.tag.voice
    }

    return word_info


def analyze_word(word):
    # Tokenize and tag the word
    tokens = word_tokenize(word)
    tagged = pos_tag(tokens)
    # Get the WordNet synsets for the word
    word_info = {'word': word,
                 'part_of_speech': metadata.get(tagged[0][1]) if tagged else 'Unknown',
    }
    return word_info


def get_word_statistics(text: str, lang: str):
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    from nltk import pos_tag
    from string import punctuation

    # Загружаем стоп-слова
    stop_words_en = stopwords.words("english")
    stop_words_ru = stopwords.words("russian")

    if lang == 'russian':
        word_tokens = [word.lower() for word in word_tokenize(text) if (
            word.lower() not in stop_words_ru) and (word not in punctuation)]

    else:
        word_tokens = [word.lower() for word in word_tokenize(text) if (
                word.lower() not in stop_words_en) and (word not in punctuation)]

    # Подсчет количества слов
    word_count = {}
    for word in word_tokens:
        if word in word_count:
            word_count[word]["count"] += 1
        else:
            word_count[word] = {"count": 1, "pos": None}

    # Определение части речи для каждого слова
    pos_tags = pos_tag(word_count.keys())
    for word, pos in pos_tags:
        word_count[word]["pos"] = pos

    res = refactor_data(word_count)
    return res


def refactor_data(input: dict):
    result = []
    for key, value in input.items():
        word_stat = [key]
        for val in value.values():
            word_stat.append(metadata.get(val) if val in metadata.keys() else val)

        result.append(word_stat)

    result.sort(key=lambda x: x[1], reverse=True)
    return result
