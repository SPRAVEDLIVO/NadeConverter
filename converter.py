#By SPRAVEDLIVO/retart1337

import json, os, argparse
parser = argparse.ArgumentParser()
parser.add_argument("--strategy", help="1: Resolve nade names manually\n2: resolve nade names automatically", default="2")
parser.add_argument("--file", help="File to convert")
args = parser.parse_args()

filePath = args.file

with open(filePath) as f:
    start = -1
    template = ""
    started = -1
    l = list(f.read().replace("\"", ""))
    print("[Converter] Stage 1: Converting to valid JSON.")
    for j, i in enumerate(l):
        if (i != "[" and i != "]" and i != "." and started == -1 and (not i.isdigit()) and i != "-") and i != "," and i != " ":
            started = j
            template += f'"{i}'
        elif (i == "," and started != -1):
            template += f'"{i}'
            started = -1
        elif (i == "]" and started != -1):
            template += '"]'
            started = -1
        elif (i.isdigit() and started != -1 or i == "-1" and started != -1):
            template += i
        else:
            template += i
    print("[Converter] Stage 2: Loading as JSON.")
    d = json.loads(template)
    print("[Converter] Stage 3: Resolving nades.")
    for it, nadeList in enumerate(d):
        content = nadeList[0]
        nadeName = content[3]
        if (not "(" in nadeName and not ")" in nadeName):
            d[it][0].append("S+T")
        else:
            if (args.strategy == "1"):
                print(nadeName)
                inp = input("Type is required to resolve: ")
                if (inp != ""):
                    content.append(inp.upper())
                    for j, i in enumerate(nadeName):
                        if (i == "("):
                            start = j
                        elif (i == ")" and inp != "other"):
                            l = list(nadeName)
                            del l[start-1:j+1]
                            newNadeName = "".join(l)
                            d[it][0][3] = newNadeName
                else:
                    d[it][0].append("S+T")
            else:
                tempNadeName = nadeName.lower()
                if ("run" in tempNadeName or "walk" in tempNadeName or "crouch" in tempNadeName):
                    content.append("OTHER")
                elif (("jump" in tempNadeName and "throw" in tempNadeName) or "j+t" in tempNadeName):
                    content.append("J+T")
                    for j, i in enumerate(nadeName):
                        if (i == "("):
                            start = j
                        elif (i == ")"):
                            l = list(nadeName)
                            del l[start-1:j+1]
                            newNadeName = "".join(l)
                            d[it][0][3] = newNadeName
                else:
                    print(f"Can't automatically resolve name: {nadeName}. Making it S+T.")
                    d[it][0].append("S+T")
    print("[Converter] Stage 4: Writing to file.")
    final = '\"'+str(d).replace("'", "").replace("\n","")+'\"'
    with open(filePath, "w") as newF:
        newF.write(final)
    print("[Converter] Stage 5: Done. Exiting.")