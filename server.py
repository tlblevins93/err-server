from errbot import BotPlugin, botcmd, botmatch
import subprocess, tempfile, re, time

class AutoSysServer(BotPlugin):
    """AutoSys server plugin for Errbot"""

    @botcmd
    def server_target(self, msg, args):
        """Target server for jobs"""
        self['target_server'] = args
        self.target_server = args
        #with open('/var/errbot/target_server', 'w+') as file:
        #    proc = subprocess.Popen(['echo',args], stdout=file)
        #    proc.wait()
        #    file.seek(0)
        #    target_server = str(target_server) + str(file.read())
        return "Targeted server: " + self['target_server']
    
    @botcmd
    def server_active(self, msg, args):
        """Retrieve targeted server"""
        #target_server = ""
        #with open('/var/errbot/target_server', 'r') as file:
        #    target_server = str(file.read())
        return "Currently targeted server: " + self['target_server']

    @botcmd
    def retrieve(self, msg, args):
        """Get the log file from errbot"""
        msg.ctx['tries'] = 10
        self.send(msg.frm, "OK to execute command " + msg.body + " [Y/N]?")
        
    @botmatch(r'^[a-zA-Z]$', flow_only=True)
    def confirm(self, msg, match):
        msg.ctx['tries'] -= 1
        guess = match.string.lower()
        if guess == 'y':
            self.send_stream_request(user=msg.frm, fsource=open(args, 'rb'), name='log.txt')
            return "File found!"
        if guess == 'n' or msg.ctx['tries'] == 0:
            return "Permission denied!"
        return "Invalid. Please try again."

from errbot import botflow, FlowRoot, BotFlow, FLOW_END

class ConfFlow(BotFlow):
    """ Conversation flows related to polls"""

    @botflow
    def conf(self, flow: FlowRoot):
        """ This is a flow that can set a guessing game."""
        # setup Flow
        dialogue = flow.connect('retrieve', auto_trigger=True)
        conf = dialogue.connect('confirm')
        conf.connect('confirm')
        conf.connect(FLOW_END, predicate=lambda ctx: ctx['tries'] == 0)
# Used to run commands in terminal and capture the result in string var.
#with tempfile.TemporaryFile() as tempf:
#    proc = subprocess.Popen(['ls','-l'], stdout=tempf)
#    proc.wait()
#    tempf.seek(0)
#    string = str(string) + str(tempf.read())
