import nltk

# Загружаем необходимые ресурсы
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Определяем грамматику
grammar = nltk.RegexpParser(
    """
        NP: {<DT>?<JJ>*<NN.*>}  # Существительные группы
        P: {<IN>}                # Предлоги
        V: {<V.*>}               # Глаголы
        PP: {<P> <NP>}           # Предложные фразы
        VP: {<V> <NP|PP>*}       # Глагольные фразы
        S:  {<NP> <VP>}          # Предложения (субъект + сказуемое)
    """
)


# Функция для построения дерева для выбранного предложения
def build_tree_for_sentence(sentence):
    # Токенизируем выбранное предложение
    tokens = nltk.word_tokenize(sentence)

    # Определяем части речи
    tags = nltk.pos_tag(tokens)

    # Применяем грамматику для парсинга
    tree = grammar.parse(tags)

    # Отображаем дерево с помощью draw()
    tree.draw()

