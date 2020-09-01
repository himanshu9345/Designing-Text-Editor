'''
1. not done tree rebalancing
2. after cut -> paste index should be less than or equal to length of remaining string.
    str1 = "qwerty"
    s.cut(1,3)
    str1 = "erty"
    s.paste(any number from 1 to 4)

'''
# class SimpleEditor:
#     def __init__(self, document):
#         self.document = document
#         self.dictionary = set()
#         # On windows, the dictionary can often be found at:
#         # C:/Users/{username}/AppData/Roaming/Microsoft/Spelling/en-US/default.dic
#         # with open("/usr/share/dict/words") as input_dictionary:
#         #     for line in input_dictionary:
#         #         words = line.strip().split(" ")
#         #         for word in words:
#         #             self.dictionary.add(word)
#         self.paste_text = ""


#     def cut(self, i, j):
#         self.paste_text = self.document[i:j]
#         self.document = self.document[:i] + self.document[j:]

#     def copy(self, i, j):
#         self.paste_text = self.document[i:j]

#     def paste(self, i):
#         self.document = self.document[:i] + self.paste_text + self.document[i:]

#     def get_text(self):
#         return self.document

#     def misspellings(self):
#         result = 0
#         for word in self.document.split(" "):
#             if word not in self.dictionary:
#                 result = result + 1
#         return result

import Ropes
class SimpleEditor:
    def __init__(self, document):
        self.document = document
        # dictionary stuff is missing
        self.dictionary = set()
        self.ropes = Ropes.Rope()
        self.rope_root,_ = self.ropes.createRopes(document, 1, len(document), None)


    def cut(self, i, j):
        self.rope_root, cut_node = self.ropes.deleteText(self.rope_root, i, j)
        self.paste_text = self.ropes.reportOperation(cut_node)
        # self.document = self.document[:i] + self.document[j:]
        # print(self.paste_text,"cut")

    def copy(self, i, j):
        self.paste_text = self.ropes.reportOperation(self.rope_root, i,j)
        # print(self.paste_text,"gggg")

    def paste(self, i):
        new_node, _ = self.ropes.createRopes(self.paste_text, 1, len(self.paste_text), None)
        left_part, right_part = self.ropes.split(self.rope_root, i)
        # print(self.ropes.reportOperation(left_part),"past oppp")
        # print(self.ropes.reportOperation(right_part),"paste oppp")

        left_merged = self.ropes.concatenationOperation(left_part, new_node)
        self.rope_root = self.ropes.concatenationOperation(left_merged,right_part)

    def get_text(self):
        return self.ropes.reportOperation(self.rope_root)

    def misspellings(self):
        result = 0
        for word in self.document.split(" "):
            if word not in self.dictionary:
                result = result + 1
        return result

import timeit

class EditorBenchmarker:
    new_editor_case = """
from __main__ import SimpleEditor
s = SimpleEditor('he;llo')"""
    
    editor_cut_paste = """
for n in range({}):
    if n%2 == 0:
        s.cut(1, 20)
    else:
        s.paste(2)"""

    editor_copy_paste = """
for n in range({}):
    if n%2 == 0:
        s.copy(1, 20)
    else:
        s.paste(2)"""

    editor_get_text = """
for n in range({}):
    s.get_text()"""

    editor_mispellings = """
for n in range({}):
    s.misspellings()"""

    def __init__(self, cases, N):
        self.cases = cases
        self.N = N
        self.editor_cut_paste = self.editor_cut_paste.format(N)
        self.editor_copy_paste = self.editor_copy_paste.format(N)
        self.editor_get_text = self.editor_get_text.format(N)
        self.editor_mispellings = self.editor_mispellings.format(N)

    def benchmark(self):
        for case in self.cases:
            print(case)
            print("Evaluating case: {}".format(case))
            new_editor = self.new_editor_case.format(case)
            t=timeit.timeit("s.lower()", "s = 'Hello World'", number=10000)
            print(self.editor_cut_paste, new_editor,t)
            # s = SimpleEditor(case)
            cut_paste_time = timeit.timeit(stmt=self.editor_cut_paste,setup=new_editor,number=1)
            print("{} cut paste operations took {} s".format(self.N, cut_paste_time))
            copy_paste_time = timeit.timeit(stmt=self.editor_copy_paste,setup=new_editor,number=1)
            print("{} copy paste operations took {} s".format(self.N, copy_paste_time))
            get_text_time = timeit.timeit(stmt=self.editor_get_text,setup=new_editor,number=1)
            print("{} text retrieval operations took {} s".format(self.N, get_text_time))
            mispellings_time = timeit.timeit(stmt=self.editor_mispellings,setup=new_editor,number=1)
            print("{} mispelling operations took {} s".format(self.N, mispellings_time))
            

if __name__ == "__main__":

    b = EditorBenchmarker(["hello friendshello friendshello friendshello friendshello friendshello friendshello friendshello friends"], 100)
    b.benchmark()
    # s = SimpleEditor("Hello_Friends")
    # s.copy(1,10)
    # print(s.get_text(),"gg1")
    
    # s.cut(1,10)
    # s.paste(1)


    # print(s.get_text(),"gg")