import re


class Code:
    def __init__(self, code: str):
        self.code = code
        self.syntax_error = 0
        self.syntax_msg = ''
        self.ofu = 'R|S|Ł|Ps|Br|Wsr|W|Lzr|Ls|Lz|B|Ba|Bi|Bp|Bz|K|dr|Tk|Ti|Tp|N|Wp|Ws|Tr'
        self.ozu = 'R|Ł|Ps|Ls|Lz|N'
        self.ozk = 'I|II|III|IIIa|IIIb|IV|IVa|IVb|V|VI|VIz'
        self.ofu_1 = 'R|S|Br|Wsr|W|Lzr'
        self.ofu_2 = 'Ł|S|Br|Wsr|W|Lzr'
        self.ofu_3 = 'Ps|S|Br|Wsr|W|Lzr'
        self.ofu_4 = 'Ls|W'
        self.ofu_5 = 'Lz|W'
        self.ofu_6 = 'Ls|Lz|B|Ba|Bi|Bp|Bz|K|dr|Tk|Ti|Tp|N|Wp|Ws|Tr'
        self.ozu_1 = 'R'
        self.ozu_2 = 'Ł|Ps|Ls|Lz'
        self.ozu_3 = 'N'
        self.ozk_1 = 'I|II|III|IV|V|VI'
        self.ozk_2 = 'I|II|IIIa|IIIb|IVa|IVb|V|VI|VIz'

    def __str__(self):
        return f'{self.code}'

    def syntax_validator(self):
        pattern = '^(\d{1,3}-\d{1,3})/(\w{1,5}-?\w{0,5})$'
        if x := re.search(pattern, self.code):
            patt = x.group(2)
            if self.check_ofu(x.group(2)):
                if re.search(f'^({self.ofu})-(\w[a-z]?)([A-Z]+[a-z]?)$', patt):
                    self.check_ofu_ozu_ozk(patt)
                if y := re.search(f'^(\w[a-z]?)([A-Z]+[a-z]?)$', patt):
                    self.check_ozu_ozk(patt)
                if re.fullmatch(f'^{self.ofu_6}$', patt):
                    self.syntax_error = 1
        else:
            self.syntax_error = 2

    def check_ofu(self, code):
        if re.search(f'^({self.ofu})(\w{0, 4})?(-)?(\w{0,5})?', code):
            return True
        else:
            self.syntax_error = 3
            return False

    def check_ofu_ozu_ozk(self, code):
        if re.search(f'({self.ofu})-({self.ozu})([A-Z]+[a-z]?)$', code):
            if y := re.search(f'({self.ofu})-({self.ozu})({self.ozk})$', code):
                if re.fullmatch(f'^({self.ofu_1})-({self.ozu_1})({self.ozk_2})$', y.group()) \
                        and y.group(1) != y.group(2):
                    self.syntax_error = 1
                    return True
                elif re.fullmatch(f'^({self.ofu_2}|{self.ofu_3}|{self.ofu_4}|{self.ofu_5})-({self.ozu_2})'
                                  f'({self.ozk_1})$', y.group()) and y.group(1) != y.group(2):
                    self.syntax_error = 1
                    return True
                else:
                    self.syntax_error = 6
                    return False
            else:
                self.syntax_error = 5
                return False
        else:
            self.syntax_error = 4
            return False

    def check_ozu_ozk(self, code):
        if re.search(f'({self.ozu})([A-Z]+[a-z]?)$', code):
            if y := re.search(f'({self.ozu})({self.ozk})$', code):
                if re.fullmatch(f'^({self.ozu_1})({self.ozk_2})$', y.group()):
                    self.syntax_error = 1
                    return True
                elif re.fullmatch(f'^({self.ozu_2})({self.ozk_1})$', y.group()):
                    self.syntax_error = 1
                    return True
                else:
                    self.syntax_error = 7
                    return False
            else:
                self.syntax_error = 5
                return False
        else:
            self.syntax_error = 4
            return False

    def syntax_message(self):
        self.syntax_validator()
        if self.syntax_error == 0:
            self.syntax_msg = 'Nieprawidłowy'
        if self.syntax_error == 1:
            self.syntax_msg = 'Prawidłowy'
        if self.syntax_error == 2:
            self.syntax_msg = 'Nieprawidłowa składnia'
        if self.syntax_error == 3:
            self.syntax_msg = 'Nieprawidłowy OFU'
        if self.syntax_error == 4:
            self.syntax_msg = 'Nieprawidłowy OZU'
        if self.syntax_error == 5:
            self.syntax_msg = 'Nieprawidłowy OZK'
        if self.syntax_error == 6:
            self.syntax_msg = 'Nieprawidłowa relacja OFU i OZU'
        if self.syntax_error == 7:
            self.syntax_msg = 'Nieprawidłowa relacja OZU i OZK'

    def validator(self):
        if self.syntax_error == 1:
            return True
        else:
            return False


def open_file(path: str):
    codes = []
    with open(path, encoding='Cp1250') as f:
        for line in f:
            line1 = line.strip()
            if not line1:
                break
            # print(line1)
            codes.append(line1)
            f.readline()
            for i in range(0, int(f.readline().strip()) + 1):
                f.readline()
    return codes


def open_file3(path: str):
    codes = []
    corrects = []
    incorrects = []
    with open(path, encoding='Cp1250') as f:
        for line in f:
            line1 = line.strip()
            if not line1:
                break
            code = Code(line1)
            code.syntax_message()
            if code.validator():
                corrects.append(f'{code}')
            else:
                incorrects.append(f'{code}   {code.syntax_msg}')
            codes.append(f'{code} {code.syntax_msg}')
            print(code)
            f.readline()
            for i in range(0, int(f.readline().strip()) + 1):
                f.readline()
    print('Niepoprawne: ' + str(len(incorrects)))
    print('Poprawne: ' + str(len(corrects)))
    return codes, corrects, incorrects


def check_pattern(code):
    pattern = '\d{1,3}-\d{1,3}/\w{1,5}-?\w{0,5}'
    if re.fullmatch(pattern, code) is not None:
        return True
    else:
        # print(code)
        return False


def check_ofu_ozu_ozk(code):
    ofu = 'R|S|Ł|Ps|Br|Wsr|W|Lzr|Ls|Lz|B|Ba|Bi|Bp|Bz|K|dr|Tk|Ti|Tp|N|Wp|Ws|Tr'
    ozu = 'R|Ł|Ps|Ls|Lz|N'
    ozk = 'I|II|III|IIIa|IIIb|IV|IVa|IVb|V|VI|VIz'
    ofu_1 = 'R|S|Br|Wsr|W|Lzr'
    ofu_2 = 'Ł|S|Br|Wsr|W|Lzr'
    ofu_3 = 'Ps|S|Br|Wsr|W|Lzr'
    ofu_4 = 'Ls|W'
    ofu_5 = 'Lz|W'
    ofu_6 = 'Ls|Lz|B|Ba|Bi|Bp|Bz|K|dr|Tk|Ti|Tp|N|Wp|Ws|Tr'
    ozu_1 = 'R'
    ozu_2 = 'Ł|Ps|Ls|Lz'
    ozu_3 = 'N'
    ozk_1 = 'I|II|III|IV|V|VI'
    ozk_2 = 'I|II|IIIa|IIIb|IVa|IVb|V|VI|VIz'
    # match case upload python 3.10
    long_pattern = f'/({ofu})-({ozu})({ozk})$'
    shorter_pattern = f'/({ozu})({ozk})$'
    shortest_pattern = f'/({ofu})$'
    if (x := re.search(long_pattern, code)) is not None:
        # if (re.search(f'({ofu_1})', x.group(1)) and re.search(f'({ozu_1})', x.group(2))
        #     and re.search(f'({ozk_2})', x.group(3))) is not None and x.group(1) != x.group(2):
        if re.fullmatch(f'^/({ofu_1})-({ozu_1})({ozk_2})$', x.group()) is not None and x.group(1) != x.group(2):
            # print(code)
            return True
        # elif (re.search(f'({ofu_2}|{ofu_3}|{ofu_4}|{ofu_5})', x.group(1)) and re.search(f'({ozu_2})', x.group(2))
        #       and re.search(f'({ozk_1})', x.group(3))) is not None and x.group(1) != x.group(2):
        elif re.fullmatch(f'^/({ofu_2}|{ofu_3}|{ofu_4}|{ofu_5})-({ozu_2})({ozk_1})$', x.group()) is not None \
                and x.group(1) != x.group(2):
            # print(code)
            return True
        # elif re.fullmatch(f'^/({ofu})-({ozu_3})$', x.group()) is not None and x.group(1) != x.group(2):
        #     # print(code)
        #     return True
        else:
            return False
    if (y := re.search(shorter_pattern, code)) is not None:
        # if (re.search(f'({ozu_1})', y.group(1)) and re.search(f'({ozk_2})$', y.group(2))) is not None:
        if re.fullmatch(f'^/({ozu_1})({ozk_2})$', y.group()) is not None:
            # print(code)
            return True
        # elif (re.search(f'({ozu_2})', y.group(1)) and re.search(f'({ozk_1})', y.group(2))) is not None:
        elif re.fullmatch(f'^/({ozu_2})({ozk_1})$', y.group()) is not None:
            # print(code)
            return True
        else:
            return False
    if (z := re.search(shortest_pattern, code)) is not None:
        # if re.search(f'({ofu_6})', z.group(1)) is not None:
        if re.fullmatch(f'^/({ofu})$', z.group()) is not None:
            return True
        else:
            return False


def validator(codes_list):
    corrects_codes = []
    incorrects_codes = []
    for code in codes_list:
        # if check_pattern(code):
        if check_pattern(code) and check_ofu_ozu_ozk(code):
            # boolean, error_code = syntax
            corrects_codes.append(code)
            # print(code)
        else:
            incorrects_codes.append(code)
            print('NIEPOPRAWNY:', code)
    print('Niepoprawne:', len(incorrects_codes))
    print('Poprawne:', len(corrects_codes))
    # print(len(checked_codes))
    return corrects_codes, incorrects_codes


if __name__ == '__main__':
    # file = 'D:\projekty\python\kataster_1\Kontury_eksport_dz.txt'
    # open_file2(file)
    # codes = check_ozu(open_file(file))
    validator(open_file(file))
