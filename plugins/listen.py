# -*- coding: utf-8 -*-

import subprocess
from slackbot.bot import listen_to
 
@listen_to('^help')
def cabocha(message):
    message.send('Usage:\nmecab something\ncabocha something\nanalysis something')

@listen_to('^mecab (.+)')
def cabocha(message, text):
    stdout,stderr = shell_execute("echo '%s' | /usr/local/bin/mecab" % (text))
    message.send('(mecab)...\n```' + stdout + '```')

@listen_to('^cabocha (.+)')
def cabocha(message, text):
    stdout,stderr = shell_execute("echo '%s' | /usr/local/bin/cabocha" % (text))
    message.send('(cabcha)...\n```' + stdout + '```')

@listen_to('^analysis (.+)')
def cabocha(message, text):
    stdout,stderr = shell_execute("echo '%s' | /usr/local/bin/cabocha -O1" % (text))
    #message.send('(debug-1)...\n```' + stdout + '```')
    lines = [line for line in stdout.split('\n') if not line=='EOS']
    lines.reverse()
    sentence = detect_sentence(lines, 2)
    message.send('(debug-2)...\n```' + sentence + '```')

def shell_execute(cmd):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()
    stdout, stderr = p.communicate()
    return str(stdout, encoding='utf-8'), str(stderr, encoding='utf-8')


def detect_sentence(lines, depth):
    depth_count = 0
    list_sentence = []
    for line in lines:
        #print('***['+line+']\n')
        words = line.split()
        if len(words)==0: continue
        #print('+++'+words[0]+'\n')
        list_sentence.append(words[0])
        if len(words)>1 and words[1].startswith('名詞'):
            depth_count += 1
            if depth_count == depth: break
    list_sentence.reverse()
    return ''.join(list_sentence)

 
@listen_to('うんこ')
def reaction(message):
    message.react('+1')


