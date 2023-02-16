import re
import argparse
import MeCab

def create_tagger():
    node_format = "[%m\s%h]"
    bos_format = ""
    eos_format = ""

    m = MeCab.Tagger(f"--node-format={node_format} --bos-format={bos_format} --eos-format={eos_format}")
    return m

def splitByBracket(string):
    i = 0
    result = []

    while i < len(string):
        if string[i] == "{":
            next = string.find("}", i) + 1
        elif string[i] == "[":
            next = string.find("]", i) + 1
        else:
            raise ValueError()

        result.append(string[i:next])
        i = next

    return result

def ord_str_uplus(string):
    return "".join([f"U+{ord(char):x}" for char in string])

def parse(tagger, text):
    regex = r"\s+"
    text_ = text.strip()

    def process(text):
        if len(text) == 0:
            return ""
        if text[0] == "#":
            return f"[{text} -1]"
        else:
            return tagger.parse(text)

    sep = re.findall(regex, text_)
    split = re.split(regex, text_)

    assert len(sep) == len(split) - 1, f"{sep}, {split}"

    sepCord = [f"{{{ord_str_uplus(t)}}}" for t in sep]
    parsed = [process(t) for t in split]

    result = splitByBracket(parsed[0])
    for i in range(1, len(parsed)):
        result.append(sepCord[i - 1])
        result.extend(splitByBracket(parsed[i]))

    return result

def pick_ngram(list, n, headStr, tailStr):
    list_ = [*([headStr] * (n - 1)), *list, *([tailStr] * (n - 1))]

    for i in range(len(list) + n - 1):
        yield list_[i:i+n]

def unescape(string):
    string_ = string.replace("\\n", "\n")

    return string_

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("output_file")
    parser.add_argument("input_files", nargs="+")
    parser.add_argument("-n", type=int, default=3)
    parser.add_argument("-v", "--verbose", action="store_true")

    args = parser.parse_args()
    output_file = args.output_file
    input_files = args.input_files
    ngram_n = args.n

    outFile = open(args.output_file, "w")
    tagger = create_tagger()

    for i, input_file in enumerate(input_files):
        print(f"[{i + 1:{len(str(len(input_file)))}}] {input_file}")
        file = open(input_file, "r")

        for line in file:
            line_ = unescape(line.strip())

            for l in pick_ngram(parse(tagger, line_), ngram_n, "^", "$"):
                outFile.write("".join(l) + "\n")

                if args.verbose:
                    print("".join(l))

if __name__ == "__main__":
    main()

