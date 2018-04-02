# add two attributes
# @attribute num_positive
# @attribute num_negative

# and find and replace emoticons with emojis?
import re

data_path = "/Users/qufeichen/Documents/Repos/Sentiment-Analysis-in-Twitter-Messages/project_files/semeval_twitter_data.txt"
subjectivity_clues_path = "/Users/qufeichen/Documents/Repos/Sentiment-Analysis-in-Twitter-Messages/project_files/subjectivity_clues_hltemnlp05/subjclueslen1-HLTEMNLP05.txt"
output_file_name = "/Users/qufeichen/Documents/Repos/Sentiment-Analysis-in-Twitter-Messages/src/subj_data2.arff"

def main():
    # read data and subjectivity from file
    data_lines = [line.rstrip('\n') for line in open(data_path)]
    subjectivity_lines = [line.rstrip('\n') for line in open(subjectivity_clues_path)]

    # print file header
    print("@relation opinion", file=open(output_file_name, "a"))
    print("@attribute sentence string", file=open(output_file_name, "a"))
    print("@attribute category {positive,negative,neutral,objective}", file=open(output_file_name, "a"))
    print("@attribute positive_negative_score numeric", file=open(output_file_name, "a"))
    print("@data", file=open(output_file_name, "a"))
    print("", file=open(output_file_name, "a"))

    # exctract subjectivity dictionary
    subjectivity_dict = {}

    for line in subjectivity_lines:
        # find word between "word1" and next space
        word = re.findall(r'word1=(.*)\spos', line)[0]
        # find sentiment
        sentiment = re.findall(r'priorpolarity=(.*)$', line)[0]
        subjectivity_dict[word] = sentiment

    # format of tweet = id, id, sentiment, words
    # count number of positive and negative words
    for line in data_lines:
        words = line.split()
        num_positive = 0
        num_negative = 0

        # positive, negative, neutral, objective
        judgement = words[2]

        for i in range(2,len(words)):
            if subjectivity_dict.get(words[i]) is not None:
                if "positive" in subjectivity_dict.get(words[i]):
                    num_positive += 1
                elif "negative" in subjectivity_dict.get(words[i]):
                    num_negative += 1

        # compute score
        score = num_positive - num_negative

        # remove quotes around judgement
        judgement = judgement.replace('"','')

        # join words into string
        text_string = ' '.join(words[3:])
        # parse emojis into unicode
        text_string = replace_emojis(text_string)
        # remove backslash
        text_string = text_string.replace("\\", "")
        # remove rogue apostrophes
        text_string = text_string.replace("'", "")

        # write result to file
        final_string = "'" + text_string + "'," + judgement + "," + str(score)

        # print(final_string)
        print(final_string, file=open(output_file_name, "a"))

def replace_emojis(text_string):
    # text_string = text_string.replace(😔, " :( ")
    # text_string = text_string.replace(😍, " :heart_eyes: ")
    # text_string = text_string.replace(😏, " ;) ")
    # text_string = text_string.replace(👍, " :thumbs_up: ")
    # text_string = text_string.replace(😩, " D: ")
    # text_string = text_string.replace(😊, " :) ")
    # text_string = text_string.replace(☀, " :snowflake: ")
    # text_string = text_string.replace(🐚, " :conch: ")
    # text_string = text_string.replace(🌴, " :palm_tree: ")
    # text_string = text_string.replace(🏊, " :swim: ")
    # text_string = text_string.replace(👼, " :baby: ")
    # text_string = text_string.replace(🙏, " :pray: ")
    # text_string = text_string.replace(💦, " :water: ")
    # text_string = text_string.replace(😂, " :D ")
    # text_string = text_string.replace(🍫, " :chocolate: ")
    # text_string = text_string.replace(🏃, " :run: ")
    # text_string = text_string.replace(💨, " :wind: ")
    # text_string = text_string.replace(🌟, " :star: ")
    # text_string = text_string.replace(😷, " :sick: ")
    # text_string = text_string.replace(😎, " B) ")

    u = ''.join(utf16(c) for c in text_string)

    return repr(u)

def pairup(b):
    return [(b[i] << 8 | b[i+1]) for i in range(0, len(b), 2)]

def utf16(c):
    e = c.encode('utf_16_be')
    return ' '.join(chr(x) for x in pairup(e))

if __name__ == "__main__":
    main()
