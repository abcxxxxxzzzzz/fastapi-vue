from typing import Union,List,Optional
from fastapi import Query



class CommonQueryParams:
    def __init__(
                self, 
                skip: Optional[int] = 1, 
                limit: Optional[int] = 10,
                keyword: Optional[str] = None,
                # filter_field: Union[str, None] = None, 
                # filter_value: Union[str, None] = None, 
                # q_field: Union[str, None] = None, 
                # q_value: Union[str, None] = None, 
                # time_field: Union[str, None] = None, 
                # start_time: Union[str, None] = None, 
                # end_time: Union[str, None] = None, 
                # order_field: Union[str, None] = None,
                # order_value: Union[str, None] = None, 
                # order_value: Union[str, None] = Query(default='desc'), 
            ):
        
        self.skip = skip
        self.limit = limit
        self.keyword = keyword
        # self.q_field = q_field
        # self.q_value = q_value
        # self.filter_field = filter_field
        # self.filter_value = filter_value
        # self.time_field = time_field
        # self.start_time = start_time
        # self.end_time = end_time
        # self.order_field = order_field
        # self.order_value = order_value
