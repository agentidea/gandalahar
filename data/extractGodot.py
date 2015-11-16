

actors=['ESTRAGON:', 'VLADIMIR:']

def readAhead(who, content, lineNum):


    accum =[who]
    while(True):
        lineNum = lineNum+1
        try:
            line = content[lineNum].strip()

            if line in actors:
                break
            else:
                accum.append(line)

        except:
            break

    return accum, lineNum




def getAccumNonBlankLines(accum):
    newAccum = []
    for index in range(1,len(accum)):
        line = accum[index].strip()
        if len(line)>0:
            newAccum.append(line)
    return " ".join(newAccum)


def writeToActor(actorName, accum):

    if len(accum) > 2:
        print accum

    with open("./data/output/{}.txt".format(actorName), "a") as actorFile:
        actorFile.write("{}\r\n".format(getAccumNonBlankLines(accum)))



def process(content):
    print len(content)
    lineNum=0
    for line in content:
        lineNum = lineNum + 1
        line = line.strip()

        if len(line) == 0: continue

        if line in actors:
            accum, x =readAhead(line, content, lineNum)
            lineNum=x
            if len(accum)>1:
                writeToActor(accum[0].replace(':',''),accum)





def loadFile(src = "./data/WaitingForGodot.txt"):

    with open(src) as f:
        content = f.readlines()

    process(content)

if __name__ == '__main__':
    loadFile()