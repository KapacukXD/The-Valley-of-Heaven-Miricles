from subprocess import call

for i in range(3):
    call(["python", "nice_board.py"])
'''
f = open('data/enemies.txt', 'w')
f.write('pengu pengu coiner')
f.close()
call(["python", "nice_board.py"])
'''
