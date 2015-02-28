import json

class Session:

    def __init__(self, id_number, start_time, duration, location=-1):
        self.id = id_number
        self.start = start_time
        self.duration = duration;
        self.chars = []
        self.location= location

    def addMembers(self, chars):
        for char in chars:
            self.chars.append(char)
        return

class Character:
    def __init__(self, id_number, name):
        self.id = id_number
        self.name = name

class JsonEncoder(json.JSONEncoder):  
    def default(self, obj):  
        return obj.__dict__ 
            
    
def loadData(iflnm):

    sessions = []
    characters = []
    node_count = 0
    interaction_session_count = 0

    ifl = open(iflnm)
    for i in range(5):
        line = ifl.readline()
        ary = line.split('=')
        if ary[0].strip() == 'INTERACTION_SESSION_COUNT':
            interaction_session_count = int(ary[1])
        elif ary[0].strip() == 'NODE_COUNT':
            node_count = int(ary[1])
    
    ## Get node names
    line = ifl.readline().strip().strip('}')
    ary = line.split(',')
    assert len(ary) == node_count
    for tmp_name_val in ary:
        [tmp_name, tmp_val] = tmp_name_val.split(':')
        name = tmp_name[ tmp_name.index('\'')+1: tmp_name.rindex('\'')]
        val = int(tmp_val)
        characters.append(Character(val, name))
    
    ## skip locations
    ifl.readline();
    
    ## Get interaction sessions
    for is_idx in range(interaction_session_count):
        ifl.readline()
        id_number = int(ifl.readline().split(':')[1].strip())
        start = int(ifl.readline().split(':')[1].strip())
        end = int(ifl.readline().split(':')[1].strip())
        members_str = ifl.readline().split(':')[1].strip().strip('[]').split(',')
        location = -1
        try:
            location = int(ifl.readline().split(':')[-1].strip())
        except ValueError:
            location = -1
        ifl.readline()
        members = [int(i) for i in members_str]
        session = Session(id_number, start, end-start, location)
        session.addMembers(members)
        sessions.append(session)

    ifl.close()
    print json.dumps({"characters": characters, "sessions": sessions}, cls=JsonEncoder, indent=4, separators=(',', ': '))

if __name__ == '__main__':
    base_dir="/Users/wangjian/Documents/workspace/personal/hopic-py/data/"
    loadData(base_dir + "thematrix_interaction_sessions.txt")