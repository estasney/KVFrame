import seaborn as sns
import seaborn as sns
from flashtext import KeywordProcessor


def generate_highlighter_colors(n_colors):
    return sns.color_palette('colorblind', n_colors).as_hex()


class ColoredKeywordProcessor(KeywordProcessor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.kw_anchors = {}

    def checkout_anchor(self, color):
        current_count = self.kw_anchors.get(color, 0)
        self.kw_anchors[color] = current_count + 1
        return "{}_{}".format(color, current_count)


    def add_colored_keywords(self, keyword_colors):
        """
        {
            "#ffffff" : ["java", "web"]
        }

        """
        for color, keywords in keyword_colors.items():
            for keyword in keywords:
                self.add_keyword(keyword, color)

    def colorize_keywords(self, sentence):
        if not sentence:
            return sentence
        new_sentence = []
        orig_sentence = sentence
        if not self.case_sensitive:
            sentence = sentence.lower()
        current_word = ''
        current_dict = self.keyword_trie_dict
        current_white_space = ''
        sequence_end_pos = 0
        idx = 0
        sentence_len = len(sentence)
        while idx < sentence_len:
            char = sentence[idx]
            current_word += orig_sentence[idx]
            # when we reach whitespace
            if char not in self.non_word_boundaries:
                current_white_space = char
                # if end is present in current_dict
                if self._keyword in current_dict or char in current_dict:
                    # update longest sequence found
                    keyword_color = None
                    longest_sequence_found = None
                    is_longer_seq_found = False
                    if self._keyword in current_dict:
                        keyword_color = current_dict[self._keyword]
                        longest_sequence_found = current_dict[self._keyword]
                        sequence_end_pos = idx

                    # re look for longest_sequence from this position
                    if char in current_dict:
                        current_dict_continued = current_dict[char]
                        current_word_continued = current_word
                        idy = idx + 1
                        while idy < sentence_len:
                            inner_char = sentence[idy]
                            current_word_continued += orig_sentence[idy]
                            if inner_char not in self.non_word_boundaries and self._keyword in current_dict_continued:
                                # update longest sequence found
                                current_white_space = inner_char
                                longest_sequence_found = current_dict_continued[self._keyword]
                                sequence_end_pos = idy
                                is_longer_seq_found = True
                            if inner_char in current_dict_continued:
                                current_dict_continued = current_dict_continued[inner_char]
                            else:
                                break
                            idy += 1
                        else:
                            # end of sentence reached.
                            if self._keyword in current_dict_continued:
                                # update longest sequence found
                                current_white_space = ''
                                longest_sequence_found = current_dict_continued[self._keyword]
                                sequence_end_pos = idy
                                is_longer_seq_found = True
                        if is_longer_seq_found:
                            idx = sequence_end_pos
                            current_word = current_word_continued
                    current_dict = self.keyword_trie_dict
                    if longest_sequence_found:
                        colorized_text = current_word.strip()
                        if current_white_space != " ":
                            colorized_text = colorized_text.replace(current_white_space, "")
                        markup = "[ref={anchor}]{keyword}[/ref]{ws}".format(anchor=self.checkout_anchor(longest_sequence_found),

                                                                               keyword=colorized_text,
                                                                               ws=current_white_space)
                        new_sentence.append(markup)
                        current_word = ''
                        current_white_space = ''
                    else:
                        new_sentence.append(current_word)
                        current_word = ''
                        current_white_space = ''
                else:
                    # we reset current_dict
                    current_dict = self.keyword_trie_dict
                    new_sentence.append(current_word)
                    current_word = ''
                    current_white_space = ''
            elif char in current_dict:
                # we can continue from this char
                current_dict = current_dict[char]
            else:
                # we reset current_dict
                current_dict = self.keyword_trie_dict
                # skip to end of word
                idy = idx + 1
                while idy < sentence_len:
                    char = sentence[idy]
                    current_word += orig_sentence[idy]
                    if char not in self.non_word_boundaries:
                        break
                    idy += 1
                idx = idy
                new_sentence.append(current_word)
                current_word = ''
                current_white_space = ''
            # if we are end of sentence and have a sequence discovered
            if idx + 1 >= sentence_len:
                if self._keyword in current_dict:
                    keyword_color = current_dict[self._keyword]
                    # add markup
                    colorized_text = current_word.replace(current_white_space, "")
                    markup = "[ref={anchor}]{keyword}[/ref]{ws}".format(anchor=self.checkout_anchor(keyword_color),

                                                                                                keyword=colorized_text,
                                                                                                ws=current_white_space)
                    new_sentence.append(markup)
                else:
                    new_sentence.append(current_word)
            idx += 1
        return "".join(new_sentence)
