
from lt_db_ops.constants import *


class BaseFilter:
    def __init__(self, table=None)->None:
        self._filter_string = ''
        self.__where = ' WHERE '
        self.table = table
        self.__base_query = f'SELECT * FROM {self.table}'
    
    def create_filter(self, obj)->str:
        return self._filter_string


    def apply_filter(self)->str:
        if len(self._filter_string) == 0:
            return self.__base_query
        return self.__base_query + self.__where + self._filter_string



class TicketsFilter(BaseFilter):
    def __init__(self)->None:
        super().__init__(TABLE_TICKETS)
        self.__table = self.table
    

    def __status_filter(self, obj)->str:
        status_filter = ''
        try:
            s_f = obj['by-status']
            if int(s_f) == -1:
                status_filter = f' ({COL_TIC_STATUS} = 0 or {COL_TIC_STATUS} = 2) ';
            else:
                status_filter = f' ( {COL_TIC_STATUS} = {s_f} )'
            return status_filter
        except KeyError as ke:
            return False
       
    
    def __association_filter(self, obj)->str:
        me_filter = ''
        try:
            m = obj['by-me']
            me_filter = f' ( {COL_TIC_ASSIGNED_TO} = {m} OR {COL_TIC_OWNER} = {m}) '
            return me_filter
        except KeyError as ke:
            return False
        
    def __department_filter(self, obj)->str:
        d_filter = ''
        try:
            d_f = obj.getlist('by-department')
            if len(d_f) <= 0:
                raise ValueError("List empty")
            c = " , ".join(d_f)
            d_filter = f" ( {COL_TIC_DEPARTMENT} IN ( {c} ) )"
            return d_filter
        except KeyError as ke:
            return False
        
        except ValueError as ve:
            return False
    

    def create_filter(self, obj) -> None:
        status_filter = self.__status_filter(obj)
        department_filter = self.__department_filter(obj)
        association_filter = self.__association_filter(obj)
        _or = ' AND '
        if type(status_filter) is not bool:
            self._filter_string = status_filter
        
        if type(department_filter) is not bool:
            self._filter_string +=( _or + department_filter)
        
        if type(association_filter) is not bool:
            self._filter_string += (_or + association_filter)

        return super().create_filter(obj)

    
        
