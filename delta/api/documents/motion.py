import json

class Motion(object):
    identifier = "mot"

    def parse_response(cell):
        """
        0: ID from Document
        1: Date from Document
        2: Title from Doucument
        3: Actual Document
        4: Type from Document
        5: ID from Motion
        6: Summary from Motion
        7: Party Affiliation Motion
        """
        return {  "id"     : cell[0]
               , "date"    : str(cell[1])
               , "title"   : cell[2]
               , "document": json.loads(str(cell[3]))
               , "type"    : cell[4]
               , "summary" : cell[6]
               , "party"   : cell[7]
               }

