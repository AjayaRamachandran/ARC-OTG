keylog = [["l", 1000],
          ["l", 1000],
          ["-1", 1000.1],
          ["l", 1000.2]]

for direction in ["u", "r", "d", "l"]:
    if [item[0] for item in keylog[-3:]] == [direction, "-1", direction] and keylog[-1][1] - keylog[-3][1] < 0.5:
        keylog[-1][0] = direction + direction