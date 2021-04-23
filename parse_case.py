from testrail import *
import shlex

client = APIClient("http://10.0.18.130/testrail/")
client.user = 'stiger_he@ovt.com'
client.password = 'PfOf1KTtCAYDwRM9mh0q-utLfbuYwxVfa3s.lSJoM'
case = client.send_get('get_case/122')
# print(case)
# print(case['custom_preconds'])
# print(case['custom_steps_separated'])
cmdstr = case['custom_steps_separated'][0]['content'].split('\n')[0]
# print(case['custom_steps_separated'][0]['content'].split('\n'))
print(cmdstr)
# print(case['custom_steps_separated'][0]['expected'])
cmds = shlex.split(cmdstr)
print(cmds)
print(tuple(cmds[1:]))


