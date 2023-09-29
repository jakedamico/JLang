#token type constants
TT_INT = 'INT'
TT_FLOAT = 'FLOAT'
TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_MUL = 'MUL'
TT_DIV = 'DIV'
TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'

DIGITS = '0123456789'

class Error:
   def __init__(self, position_start, position_end, error_name, details):
      self.position_start = position_start
      self.position_end = position_end
      self.error_name = error_name
      self.details = details
      
   def as_string(self):
      result = f'{self.error_name}: {self.details} \n'
      result += f'File {self.position_start.fileName}, line {self.position_start.line + 1}'
      return result

class IllegalCharError(Error):
   def __init__(self, position_start, position_end, details):
      super().__init__(position_start, position_end, 'Illegal Character', details)

class Position:
   def __init__(self, index, line, column, fileName, fileText):
      self.index = index
      self.line = line
      self.column = column
      self.fileName = fileName
      self.fileText = fileText
      
   def advance(self, current_char):
      self.index += 1
      self.column += 1
      
      if current_char == '\n':
         self.line += 1
         self.col = 0
      
      return self
   
   def copy(self):
      return Position(self.index, self.line, self.column, self.fileName, self.fileText)

class Token:
   def __init__(self, type_, value=None):
      self.type = type_
      self.value = value

   def __repr__(self):
      if self.value: 
         return f'{self.type}:{self.value}'
      return f'{self.type}'

class Lexer:
   def __init__(self, fileName, text):
      self.fileName = fileName
      self.text = text
      self.position = Position(-1, 0, -1, fileName, text)
      self.current_char = None
      self.advance()

   def advance(self):
      self.position.advance(self.current_char)
      if self.position.index < len(self.text):
         self.current_char = self.text[self.position.index]
      else:
         self.current_char = None
         
   def create_tokens(self):
      tokens = []
      
      while self.current_char != None:
         if self.current_char in ' \t':
            self.advance()
         elif self.current_char in DIGITS:
            tokens.append(self.generate_num_token())
         elif self.current_char == '+':
            tokens.append(Token(TT_PLUS))
            self.advance()
         elif self.current_char == '-':
            tokens.append(Token(TT_MINUS))
            self.advance()
         elif self.current_char == '*':
            tokens.append(Token(TT_MUL))
            self.advance()
         elif self.current_char == '/':
            tokens.append(Token(TT_DIV))
            self.advance()
         elif self.current_char == '(':
            tokens.append(Token(TT_LPAREN))
            self.advance()
         elif self.current_char == ')':
            tokens.append(Token(TT_RPAREN))
            self.advance()
         else:
            #no character found return error
            position_start = self.position.copy()
            char = self.current_char
            self.advance()
            return [], IllegalCharError(position_start, self.position, "'" + char + "'")
         
      return tokens, None
   
   def generate_num_token(self):
      num_str = ''
      dot_count = 0
      
      while self.current_char != None and self.current_char in DIGITS + '.':
         if self.current_char == '.':
            if dot_count == 1: break
            dot_count += 1
            num_str += '.'
         else:
            num_str += self.current_char
         self.advance()
      
      if dot_count == 0:
         return Token(TT_INT, int(num_str))
      else:
         return Token(TT_FLOAT, float(num_str))

#run function
def run(fileName, text):
   lexer = Lexer(fileName, text)
   tokens, error = lexer.create_tokens()
   
   return tokens, error