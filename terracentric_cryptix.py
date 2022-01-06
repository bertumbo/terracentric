import numpy as np

default_font = {}

c1 = np.array([0, 0, 0])
c2 = np.array([0, 255, 0])
c3 = np.array([255, 0, 0])
c4 = np.array([0, 0, 255])

default_font["-fill"] = np.array([
    [c1, c4, c1]
])

default_font["-fill2"] = np.array([
    [c1, c1, c1]
])

default_font["--start"] = np.array([
    [c2, c2, c2],
    #[c2, c1, c2]
])

default_font["--end"] = np.array([
    #[c2, c1, c2],
    [c2, c2, c2]
])

default_font["-sep"] = np.array([
    [c1, c1, c1]
])

default_font["+"] = np.array([
    [c1, c2, c1],
    [c2, c2, c2],
    [c1, c2, c1],
])

default_font["a"] = np.array([
    [c2, c2, c2],
    [c1, c1, c3],
    [c2, c2, c2],
])
default_font["b"] = np.array([
    [c2, c2, c2],
    [c3, c1, c3],
    [c1, c3, c1],
])
default_font["c"] = np.array([
    [c2, c2, c2],
    [c2, c1, c2],
    [c2, c1, c2],
])
default_font["d"] = np.array([
    [c2, c2, c2],
    [c2, c1, c2],
    [c1, c2, c1],
])
default_font["e"] = np.array([
    [c2, c2, c2],
    [c3, c1, c3],
    [c3, c1, c3],
])

default_font["g"] = np.array([
    [c2, c2, c2],
    [c2, c1, c2],
    [c2, c1, c3],
])

default_font["i"] = np.array([
    [c2, c1, c2],
    [c2, c2, c2],
    [c2, c1, c2],
])

default_font["n"] = np.array([
    [c2, c2, c1],
    [c1, c1, c2],
    [c2, c2, c1],
])

default_font["r"] = np.array([
    [c2, c2, c2],
    [c1, c1, c3],
    [c2, c3, c1],
])

default_font["s"] = np.array([
    [c3, c1, c2],
    [c3, c1, c3],
    [c2, c1, c3],
])

default_font["t"] = np.array([
    [c1, c1, c2],
    [c2, c2, c2],
    [c1, c1, c2],
])

default_font["u"] = np.array([
    [c1, c1, c1],
    [c2, c2, c2],
    [c3, c3, c3],
])

default_font["-"] = np.array([
    [c1, c2, c1],
    [c1, c2, c1],
    [c1, c2, c1],
])

print(default_font)


class Word():
    pass

def generate_letter_list(input_string):


    char = ["--start", "-sep"]
    for ind_literal, literal in enumerate(input_string):
        char.append(literal)
        char.append("-sep")
    char.append("--end")

    #print(char)
    return char


def generate_array_from_letter_list(letter_list, animation_step):
    string = np.ones(shape=(0, 3, 3))

    for char in letter_list:
        string = np.concatenate((
            string,
            default_font[char]
        ))

    len = string.shape[0]
    #if animation_step < (len/2):
    #print(len)

    const_a = 2         # len of start + 1

    #for ind in range(animation_step - 1):
    if animation_step < (len - 1) / 2:
        for ind in range(animation_step - 1):
            #len = string.shape[0]
            string = np.delete(string, ind + const_a, 0)
            string = np.concatenate((default_font["-fill"], string))
            string = np.delete(string, len - 1 - ind - const_a, 0)
            string = np.concatenate((string, default_font["-fill"]))
    elif animation_step == (len - 1) / 2:
        for ind in range(animation_step - 1):
            string = np.delete(string, ind + const_a, 0)
            string = np.concatenate((default_font["-fill"], string))
            string = np.delete(string, len - 1 - ind - const_a, 0)
            string = np.concatenate((string, default_font["-fill"]))
    elif animation_step < len - 1:

        help_step = int((len - 1) / 2)
        for ind in range(help_step - 1):
            string = np.delete(string, ind + const_a, 0)
            string = np.concatenate((default_font["-fill"], string))
            string = np.delete(string, len - 1 - ind - const_a, 0)
            string = np.concatenate((string, default_font["-fill"]))
        if animation_step > help_step:
            for ind in range(help_step - 1, animation_step - 1):
                shape = string.shape[0]
                string = np.delete(string, shape-1, 0)
                string = np.delete(string, 0, 0)
        # elif animation_step < len:
        # #for ind in range(animation_step - 1):
        #     #len = string.shape[0]
        #     string = np.delete(string, ind + const_a, 0)
        #     string = np.concatenate((default_font["-fill2"], string))
        #     string = np.delete(string, len - 1 - ind - const_a, 0)
        #     string = np.concatenate((string, default_font["-fill2"]))

    else:
        pass
        string = default_font["+"]
        #string = np.concatenate(((len - 3) / 2, ))
    #cutoff x steps



    return string


#char0 = generate_letter_list("string")
#print(generate_array_from_letter_list(char0))
