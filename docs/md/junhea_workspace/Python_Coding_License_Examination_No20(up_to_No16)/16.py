# 16번

def TranslateMos(a):
    mosalphabet = {'.-':'A', '-...':'B', '-.-.':'C', '-..':'D', '.':'E', '..-.':'F', '--.':'G', '....':'H', '..':'I', '.---':'J', '-.-':'K', '.-..':'L', '--':'M', '-.':'N', '---':'O', '.--.':'P', '--.-':'Q', '.-.':'R', '...':'S', '-':'T', '..-':'U', '...-':'V', '.--':'W', '-..-':'X', '-.--':'Y', '--..':'Z'}
    words = a.split('  ')
    answer = []
    for i in range(len(words)):
        alphabet = words[i].split()
        for j in range(len(alphabet)):
            answer.append(mosalphabet[alphabet[j]])
        answer.append(' ')
    return ''.join(answer)

print(TranslateMos('.... .  ... .-.. . . .--. ...  . .- .-. .-.. -.--'))