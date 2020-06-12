'''
Created on 2020/06/06

@author: HIROTO
'''
import ulid as ud


class ExperimentID():
    """
    Generate a unique ID to identify each experiment using ulid

    Attributes
    ---------------
    idobj : object <class 'ulid'>
        experiment id object
    id : String
        experiment id String
    """
    def __init__(self):
        self.idobj= ud.new()
        self.id=self.idobj.str




