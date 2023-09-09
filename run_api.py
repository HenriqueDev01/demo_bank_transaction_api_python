import os

def main():
  os.environ["FLASK_APP"] = __file__
  # os.environ["FLASK_DEBUG"] = "1"
  os.system("python -m flask --app bank_api run")

if __name__=='__main__':
  main()
  os.system('pause')
