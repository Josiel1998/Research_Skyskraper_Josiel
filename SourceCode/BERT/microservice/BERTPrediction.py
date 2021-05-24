# importing os module 
import os
import pprint

from dotenv import load_dotenv
load_dotenv()

def main():
    # Print the list of user's
    # environment variables
    #os.environ['dbName'] = 'skyskraper'
    print("User's Environment variable:")
    user = os.environ.get('DBNAME')
    #pprint.pprint(dict(os.environ.get('DBUSER')), width = 1)
    print(user)

if __name__ == '__main__':
    main()

# importing os module 
import os
import pprint
  
