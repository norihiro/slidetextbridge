'''
Context for the program
'''

class Context:
    'Context class managing plugin instances'

    def __init__(self):
        self.instances = []

    def add_instance(self, inst):
        '''
        Add an instance of a plugin
        :param inst:  The instance to be added
        '''
        self.instances.append(inst)

    def get_instance(self, name=None):
        '''
        Find instance
        If no argument is specified, return the last
        :param name:  If given, find by name
        '''
        if name:
            for inst in self.instances:
                if inst.name == name:
                    return inst
        return self.instances[-1]

    async def initialize_all(self):
        for inst in self.instances:
            await inst.initialize()
