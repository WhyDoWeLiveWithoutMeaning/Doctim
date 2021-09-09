# MIT License

# Copyright (c) 2021 Meaning

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import re

def _format(text: str) -> str:
    text = re.sub(r'([\“\”])+',"\"",text)
    text = re.sub(r'([\’])+', "'", text)
    match = re.split(r'(s.)((?:\s+)?(?:\+\+\s?(?:[\w\s\-\_\'\"\:\;\,\^\*\<\>\/\“\”\’]+)+\=\=\s?)+\s?)(.s)', text)
    full_length_list = []
    for element in match:
        full_length_list.extend(re.split(r'(\+\+)\s*([\w\s\-\_\'\^\"\:\;\,\*\<\>\/]+)\s*(\=\=)', element))
    for i in range(len(full_length_list)):
        if full_length_list[i] == "s.":
            full_length_list[i] = "<ul>"
        elif full_length_list[i] == ".s":
            full_length_list[i] = "</ul>"
        elif full_length_list[i] == "++":
            full_length_list[i] = "<li>"
        elif full_length_list[i] == "==":
            full_length_list[i] = "</li>"
    match = re.split(r'(\*{2})([\w\s\-\_\'\^\"\:\,\;\<\>\/][\w\s\-\_\'\"\:\^\;\,\*\<\>\/]+?)(\*{2})', ''.join(full_length_list) if full_length_list else text)
    if match:
        start = True
        for i in range(len(match)):
            if match[i] == "**":
                match[i] = "<b>" if start else "</b>"
                start = not start
    match = re.split(r'(\*)([\w\s\-\_\'\"\:\^\;\<\,\>\/]+?)(\*)', ''.join(match) if match else text)
    start = True
    for i in range(len(match)):
        if match[i] == "*":
            match[i] = "<em>" if start else "</em>"
            start = not start
    match = re.split(r'(\^{2})([\w\s\-\_\'\"\:\^\;\<\,\>\/]+?)(\^{2})', ''.join(match) if match else text)
    start = True
    for i in range(len(match)):
        if match[i] == "^^":
            match[i] = f"<sup><a id=\"superfoot\" href=\"#foot{match[i+1]}\">[" if start else "]</a></sup>"
            start = not start
    match = re.split(r'(\_{2})([\w\s\-\_\<\>\,\^\/]+?)(\_{2})', ''.join(match) if match else text)
    start = True
    for i in range(len(match)):
        if match[i] == "__":
            match[i] = "<u>" if start else "</u>"
            start = not start
    match = re.split(r'(\-{2})([\w\s\-\_\'\"\:\;\<\>\^\,\/]+?)(\-{2})', ''.join(match) if match else text)
    start = True
    for i in range(len(match)):
        if match[i] == "--":
            match[i] = "<s>" if start else "</s>"
            start = not start
    return ''.join(match) if match else text

class Erc:

    def __init__(self, text: str) -> None:
        self.text = text
        self.html = self._format_html()

    def _format_html(self) -> None:
        final_text = ""
        lines = self.text.split("\n")
        table = False

        for line in lines:
            if table:
                if line.strip() == "T":
                    table = False
                    final_text += "</table>\n</div>\n"
                else:
                    arguments = line.split("|")
                    final_text += "<tr>\n"
                    for argument in arguments:
                        final_text += f"<td>{_format(argument.strip())}</td>\n"
                    final_text += "</tr>\n"
            else:
                if line.strip() == "\n" or len(line.strip()) == 0:
                    final_text += "<br>\n"
                elif match := re.match(r'[!](\d)((\s[a-zA-Z\n\d\'\"\^\:\;\-\“\”\’\,\_\.\\\*]+)+)\s[!]', line):
                    final_text += f"<h{match.group(1)}>{_format(match.group(2).strip())}</h{match.group(1)}>\n"
                elif match := re.match(r'\?\s(([a-zA-Z\d\n\'\"\-\“\”\^\’\,\\:\;\_\.\\\*]+\s)+)\?', line):
                    final_text += f"<p>{_format(match.group(1))}</p>\n"
                elif match := re.match(r'\[(http[s]:\/\/([a-zA-Z\d\_\-\.\/]+)\.(png|jpg|jpeg))\]\(([a-zA-Z\'\"\“\”\’\,\^\s]+)+\)?', line):
                    final_text += f"<div class=\"img\">\n<img src=\"{match.group(1)}\">\n<under>{_format(match.group(4))}</under>\n</div>\n"
                elif match := re.match(r'F([\d]+)\s*(https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()!@:%_\+.~#?&\/\/=]*))', line):
                    final_text += "<div class=\"footnote\" id=\"foot{0}\"><a href=\"{1}\" target=\"_blank\">{0}. {1}</a></div>\n".format(match.group(1), match.group(2))
                elif line.strip() == "T": 
                    table = True
                    final_text += "<div>\n<table>\n"
                else:
                    print(line)
                    raise Exception("This is not a valid format")
        return final_text