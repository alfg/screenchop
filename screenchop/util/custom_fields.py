from wtforms import Field
from wtforms.widgets import TextInput 

class TagListField(Field):                                          
    widget = TextInput()
        
    def _value(self):            
        if self.data:                                               
            return u', '.join(self.data)
        else:
            return u''                                              
        
    def process_formdata(self, valuelist):                          
        if valuelist:
            self.data = [x.strip() for x in valuelist[0].split(',')]
        else: 
            self.data = []                                          

