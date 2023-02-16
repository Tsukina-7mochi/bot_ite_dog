import argparse
import random
import re

def split_by_bracket(string):
    i = 0
    result = []

    while i < len(string):
        if string[i] == "{":
            next = string.find("}", i) + 1
        elif string[i] == "[":
            next = string.find("]", i) + 1
        else:
            next = i + 1

        result.append(string[i:next])
        i = next

    return result

def generate(start_string, input_file, ngram_n, head_string, tail_string):
    def extract_string(string):
        if string[0] == "[":
            w_o_bracket = string[1:-1]
            return w_o_bracket[:w_o_bracket.find(" ")]
        elif string[0] == "{":
            w_o_bracket = string[1:-1]

            return "".join([chr(int(t[2:], 16)) for t in re.findall(r"U\+\d+", w_o_bracket)])
        elif string == head_string or string == tail_string:
            return ""
        else:
            return string

    def pick_random(list):
        return list[random.randrange(len(list))]

    file = open(input_file, "r")

    candidates = []
    current = ([head_string] * (ngram_n - 1))
    current_str = "".join(current)
    result = ""

    if start_string == "":
        candidates.append("^")
    else:
        for line in file:
            line_ = line.strip()

            if line_.startswith(current_str):
                split = split_by_bracket(line_)

                if extract_string(split[-1]) == start_string:
                    candidates.append(split[-1])

    if len(candidates) < 1:
        return result

    while True:
        # pick one from candidates
        picked = pick_random(candidates)
        if picked == tail_string:
            break

        result += extract_string(picked)
        current = current[1:]
        current.append(picked)
        current_str = "".join(current)

        # reset
        candidates = []
        file.seek(0)

        for line in file:
            line_ = line.strip()

            if line_.startswith(current_str):
                split = split_by_bracket(line_)

                candidates.append(split[-1])

    return result

def main():
    print(generate("", "../text/dest/ngram.txt", 3, "^", "$"))

if __name__ == "__main__":
    main()
