import re

class Tool:
    remove_img = re.compile('<img.*?>| {7}')
    remove_addr = re.compile('<a.*?>|</a>')
    replace_line = re.compile('<tr>|<div>|</div>|</p>')
    replace_td = re.compile('<td>')
    replace_p = re.compile('<p.*?>')
    replace_br = re.compile('<br><br>|<br>')
    remove_other_tags = re.compile('<.*?>')
    
    def replace(self, x):
        x = re.sub(self.remove_img, '', x)
        x = re.sub(self.remove_addr, '', x)
        x = re.sub(self.replace_line, '\n', x)
        x = re.sub(self.replace_td, '\t', x)
        x = re.sub(self.replace_p, '\n  ', x)
        x = re.sub(self.replace_br, '\n', x)
        x = re.sub(self.remove_other_tags, '', x)
        
        return x.strip()