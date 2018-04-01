# add two attributes
# @attribute num_positive
# @attribute num_negative

# and find and replace emoticons with emojis?

import re

data_path = "/Users/qufeichen/Documents/Repos/Sentiment-Analysis-in-Twitter-Messages/project_files/semeval_twitter_data.txt"
subjectivity_clues_path = "/Users/qufeichen/Documents/Repos/Sentiment-Analysis-in-Twitter-Messages/project_files/subjectivity_clues_hltemnlp05/subjclueslen1-HLTEMNLP05.txt"
output_file_name = "/Users/qufeichen/Documents/Repos/Sentiment-Analysis-in-Twitter-Messages/src/subj_data.arff"

data_lines = [line.rstrip('\n') for line in open(data_path)]
subjectivity_lines = [line.rstrip('\n') for line in open(subjectivity_clues_path)]

# print file header
print("@relation opinion", file=open(output_file_name, "a"))
print("@attribute sentence string", file=open(output_file_name, "a"))
print("@attribute category {positive,negative,neutral,objective}", file=open(output_file_name, "a"))
print("@attribute num_positive numeric", file=open(output_file_name, "a"))
print("@attribute num_negative numeric", file=open(output_file_name, "a"))
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

    score = num_positive - num_negative
    print(score)

    # remove quotes around judgement
    judgement = judgement.replace('"','')

    # write result to file
    final_string = "'" + ' '.join(words[3:]) + "'," + judgement + "," + str(num_positive) + "," + str(num_negative)
    print(final_string)
    print(final_string, file=open(output_file_name, "a"))
