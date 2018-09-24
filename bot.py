from requests_oauthlib import OAuth1Session

import MeCab

import random

CK = “XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX”

CS = “XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX”

AT = “XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX”

AS = “XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX”

def wakati(text):

   mt = MeCab.Tagger(“-Owakati”)

   m = mt.parse(text)

   result = m.rstrip(“ \n”).split(“ ”)

   return result

def markovtweet():

#data.txtは過去のツイートのcsvからツイート文章部分だけを取り出してまとめたテキストデータです。

   f = “data.txt”

   tweet = open(f).read()

   wordlist = wakati(tweet)

#ここからは分かち書きした文章を元に、ある2つの言葉の次に来る言葉を記録してます。

   markov2 = {}

   w1 = “”

   w2 = “”

   for word in wordlist:

        if w1 and w2:

            if (w1,w2) not in markov2:

                markov2[(w1,w2)] = []

            markov2[(w1,w2)].append(word)

        w1,w2 = w2,word

#ここから文章作成してます

   count = 0

   sentence = “”

   w1,w2 = random.choice(list(markov2.keys()))#最初の言葉はランダムに決めてます

   while count < len(wordlist):

       if len(sentence) > random.randint(80,130):

           break

       tmp = random.choice(list(markov2[(w1,w2)]))

       sentence += tmp

       w1,w2 = w2,tmp

       count += 1

   start = sentence.find(“。”)+1

   end = sentence.find(“。”,60,130)+1

   if start>=end:

       sentence = “にゃーん”

   else:

       sentence = sentence[start:end]

   print(sentence)

   return sentence

def posttweet(text):

   if len(text) >140:

       print(“text is long over 140 characters.”)

       return

   params = {“status”:str(text)}

   url = “https://api.twitter.com/1.1/statuses/update.json”

   twitter = OAuth1Session(CK,CS,AT,AS)

   req = twitter.post(url,params = params)

def main():

   s = markovtweet()

   s += “ #bot”

   posttweet(s)

if __name__ == ’__main__’:

   main()