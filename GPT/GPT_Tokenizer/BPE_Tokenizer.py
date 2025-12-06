class BPETokenizer:
    def __init__(self, text: str, iterations = 50):
        self.text = text
        self.char_to_idx = {}
        self.idx_to_char = {}
        self._create_vocab()
        self.iterations = iterations

    def _create_vocab(self):
        for idx, char in enumerate(list(set(self.text))):
            unicode_code_point = char.encode('utf-8')
            self.char_to_idx[unicode_code_point] = idx
            self.idx_to_char[idx] = unicode_code_point

    def encode(self, text: str, char_to_idx = None) -> list:
        byte_text = text.encode('utf-8')

        if char_to_idx:
            unicode_points = [char_to_idx[bytes([b])] for b in byte_text]
        else:
            unicode_points = [self.char_to_idx[bytes([b])] for b in byte_text]
        return unicode_points

    def decode(self, unicode_code_point_list: list, idx_to_char = None) -> str:

        if idx_to_char:
            byte_seq = b''.join([idx_to_char[idx] for idx in unicode_code_point_list])
        else:
            byte_seq = b''.join([self.idx_to_char[idx] for idx in unicode_code_point_list])
        
        return byte_seq.decode('utf-8')

    def _get_stats(self, unicode_code_point_list: list) -> dict:
        stats = {}
        for itm1, itm2 in zip(unicode_code_point_list, unicode_code_point_list[1:]):
            pair = (itm1, itm2)
            stats[pair] = stats.get(pair, 0) + 1
        return {k: v for k, v in sorted(stats.items(), key=lambda item: item[1], reverse=True)}

    def _merge(self, unicode_code_point_list: list) -> tuple:
        stats = self._get_stats(unicode_code_point_list)
        try:
            pair_with_max_occurrences = max(stats, key=stats.get)
        except ValueError:
            return unicode_code_point_list, False

        if stats[pair_with_max_occurrences] > 1:
            new_token = self.idx_to_char[pair_with_max_occurrences[0]] + self.idx_to_char[pair_with_max_occurrences[1]]
            new_token_idx = len(self.idx_to_char)

            self.char_to_idx[new_token] = new_token_idx
            self.idx_to_char[new_token_idx] = new_token

            i = 0
            while i < len(unicode_code_point_list) - 1:
                if (unicode_code_point_list[i], unicode_code_point_list[i + 1]) == pair_with_max_occurrences:
                    unicode_code_point_list[i] = new_token_idx
                    unicode_code_point_list.pop(i + 1)
                else:
                    i += 1
        else:
            return unicode_code_point_list, False

        return unicode_code_point_list, True

    def bpe(self) -> list:
        starting_vocab_size = len(self.idx_to_char)
        unicode_code_point_list = self.encode(self.text)
        raw_text_token_count = len(unicode_code_point_list)

        flag = True
        i = 0
        while flag and i < self.iterations:
            print(f"Iteration: {i+1}")
            unicode_code_point_list, flag = self._merge(unicode_code_point_list)
            print(f"char_to_idx: {len(self.char_to_idx)} | idx_to_char: {len(self.idx_to_char)}")
            print("==============================================================================")
            i += 1

        if flag and self.iterations > 1:
            print('Iterations completed')

        processed_text_token_count = len(unicode_code_point_list)
        final_vocab_size = len(self.idx_to_char)
        compression_ratio = (processed_text_token_count / raw_text_token_count) * 100

        print(f"Starting vocab size: {starting_vocab_size}")
        print(f"Final vocab size: {final_vocab_size}")
        print(f"total tokens in raw text: {raw_text_token_count}")
        print(f"total tokens after bpe: {processed_text_token_count}")
        print(f"compression ratio: {compression_ratio}")

        return unicode_code_point_list, self.idx_to_char, self.char_to_idx
