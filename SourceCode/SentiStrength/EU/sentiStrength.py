import subprocess
import shlex
import os

def main():
    print(RateSentiment("School is difficult but it will be rewarding"))

def RateSentiment(sentiString):

    print(sentiString)

    # Get relative path
    dirname = os.path.dirname(__file__)

    getJar = "java -jar " + dirname + "/SentiStrengthCom.jar"
    getData = "stdin sentidata " + dirname + "/SentStrength_Data_Sept2011/"
    #option = "trinary (report positive-negative-neutral classification instead)"
    option = "scale"
    #open a subprocess using shlex to get the command line string into the correct args list format
    p = subprocess.Popen(shlex.split(getJar + " " + getData + " " + option),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    #communicate via stdin the string to be rated. Note that all spaces are replaced with +
    #Can't send string in Python 3, must send bytes
    b = bytes(sentiString.replace(" ","+"), 'utf-8')
    stdout_byte, stderr_text = p.communicate(b)
    #convert from byte
    stdout_text = stdout_byte.decode("utf-8") 
    #replace the tab with a space between the positive and negative ratings. e.g. 1    -5 -> 1 -5
    stdout_text = stdout_text.rstrip().replace("\t"," ")
    classification = stdout_text.split()
    positive = int(classification[0])
    negative = int(classification[1])
    overall = int(classification[2])

    # Switch/Casing classification definition
    if(-4 >= overall):
        sentiment = "Strong Negative"
    elif(-3 == overall):
        sentiment = "Negative"
    elif(0 > overall):
        sentiment = "Weak Negative"
    elif(0 == overall):
        sentiment = "Neutral"
    elif(3 > overall):
        sentiment = "Weak Positive"
    elif(3 == overall):
        sentiment = "Positive"
    else:
        sentiment = "Strong Positive"

    res = "Sentiment result is " + sentiment + " " + str(overall)
    return res


if __name__ == '__main__':
    main()