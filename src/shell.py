import JLang

while True:
   text = input('JLang > ')
   result, error = JLang.run('testFile', text)
   
   if error:
      print(error.as_string())
   else:
      print(result)