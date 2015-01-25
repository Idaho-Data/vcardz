import binascii
import os


def xstr(s):
    if s is None:
        return ''
    else:
        return str(s)

def smash(val, delim):
    tokens = list(filter((lambda x: x), val.split()))
    return delim.join(tokens)

def new_id():
    return binascii.b2a_hex(os.urandom(8)).decode('utf-8')

# def log_mongoStream(uuid, field):
#   conn = Connection(os.environ['MONGOURL'])
#   db_name = os.environ['MONGODB']
#   db = getattr(conn, db_name) # enables db_name to be configurable
#   doc = db.mergelog.find_one({'uuid': uuid})
#   return io.StringIO(doc[field])

# def contacts_mongoStream(uuid, field):
#   conn = Connection(os.environ['MONGOURL'])
#   db_name = os.environ['MONGODB']
#   db = getattr(conn, db_name) # enables db_name to be configurable
#   doc = db.contacts.find_one({'uuid': uuid})
#   return io.StringIO(doc[field])

# def contacts_saveScrub(uuid, scrub, subway):
#   conn = Connection(os.environ['MONGOURL'])
#   sys.stderr.write(__file__ + " got connection, updating mongodb for uuid: [%s]\n" % (uuid))
#   db_name = os.environ['MONGODB']
#   db = getattr(conn, db_name) # enables db_name to be configurable
#   db.contacts.find_and_modify({'uuid': uuid},
#                                 update= {'$set': {'scrub': scrub,
#                                           'subway': subway,
#                                           'status': 'done'}
#                                  })
#   sys.stderr.write(__file__ + " updated mongodb for uuid: [%s]\n" % (uuid))

# def options():
#   parser = argparse.ArgumentParser(description='Kontexa sandbox')
#   parser.add_argument("--mongo", 
#                       help="pull vCard data from [MONGOURL].contacts",
#                       action="store_true")  
#   parser.add_argument("--log", 
#                       help="pull vCard data from [MONGOURL].mergelog",
#                       action="store_true")
#   parser.add_argument("--file", 
#                       help="use vCard file")
#   parser.add_argument("-o", "--output",
#                       help="store vCard and map data in a file")
#   parser.add_argument("--uuid", 
#                       help="person ID")
#   parser.add_argument("--goauth2",
#                       help="Google OAuth2")
  
#   args = parser.parse_args()
  
#   opts = {}
#   opts['file'] = None
#   if args.mongo:
#     opts['stream'] = contacts_mongoStream(args.uuid, 'vcards')
#   elif args.log:
#     opts['stream'] = log_mongoStream(args.uuid, 'vcards')
#   elif args.file:
#     name, extension = os.path.splitext(args.file)
#     if ".pst" == extension.lower():
#       opts['file'] = args.file
#       opts['stream'] = None
#     else:
#       opts['stream'] = open(args.file)
  
#   opts['output'] = args.output
#   opts['uuid'] = args.uuid
#   opts['goauth2'] = args.goauth2
#   return opts
