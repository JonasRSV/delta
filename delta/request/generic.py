
class Generic(object):
    def parse_response(cell):
        return {  "id"     : cell[0]
               , "date"    : str(cell[1])
               , "title"   : cell[2]
               , "document": json.loads(str(cell[3]))
               , "type"    : cell[4]
               }
