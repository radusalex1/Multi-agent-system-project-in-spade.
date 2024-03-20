#CONSTANTS
AGENT1_JID = 'radusalex@xmpp.jp'
AGENT2_JID = 'agent1_radu_mas@xmpp.jp'
AGENT3_JID = 'agent_radu_maas@xmpp.jp'

def get_password():
    with open("password.txt",'r') as f:
        return f.read()
    
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
