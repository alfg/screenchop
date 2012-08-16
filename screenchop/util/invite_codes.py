from screenchop.models import Invite_code
from time import strftime

class InviteCode(object):
    """ Class to check if a code is valid and/or to use the code """    

    def is_valid(self, code):
        try:
            # Query code to check if valid
            checkCode = Invite_code.objects.get(code=code)
            
            # If valid, return True, if not, False
            if checkCode.valid == False:
                return False
            
            return True
        
        # Exception = False. Usually because query is not found
        except:
            return False
    
    def use_code(self, code, user):
        """ Code to use the code, timestamp with user """
        code = Invite_code.objects.get(code=code)
        code.valid = False
        code.date_used = strftime("%Y-%m-%d_%H-%M-%S")
        code.used_by = user
        code.save()
        return True

