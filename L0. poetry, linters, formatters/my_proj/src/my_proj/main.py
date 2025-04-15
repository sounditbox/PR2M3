from functools import reduce
from typing import Any, AnyStr, List, Union

from module import mod_var

a:int =mod_var
a+=12

j = [1,
     2,
     3
]
def f(nums: Union[List[AnyStr] | List[int]])                   -> Any:
    print(
                                                                      reduce(lambda x, y: x + y, nums))


f(
    [
        '1',
   '2',
   '3'
   ]
  )
