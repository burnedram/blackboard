# -*- coding: utf-8 -*-
### Automatically generated by repyhelper.py ### /home/affe/tda596/blackboard/demokit/serialize.repy

### THIS FILE WILL BE OVERWRITTEN!
### DO NOT MAKE CHANGES HERE, INSTEAD EDIT THE ORIGINAL SOURCE FILE
###
### If changes to the src aren't propagating here, try manually deleting this file. 
### Deleting this file forces regeneration of a repy translation


from repyportability import *
import repyhelper
mycontext = repyhelper.get_shared_context()
callfunc = 'import'
callargs = []

"""
Author: Justin Cappos


Start date: October 9th, 2009

Purpose: A simple library that serializes and deserializes built-in repy types.
This includes strings, integers, floats, booleans, None, complex, tuples, 
lists, sets, frozensets, and dictionaries.

There are no plans for including objects.

Note: that all items are treated as separate references.   This means things
like 'a = []; a.append(a)' will result in an infinite loop.   If you have
'b = []; c = (b,b)' then 'c[0] is c[1]' is True.   After deserialization 
'c[0] is c[1]' is False.

I can add support or detection of this if desired.
"""

# The basic idea is simple.   Say the type (a character) followed by the 
# type specific data.    This is adequate for simple types
# that do not contain other types.   Types that contain other types, have
# a length indicator and then the underlying items listed sequentially.   
# For a dict, this is key1value1key2value2.



def serialize_serializedata(data):
  """
   <Purpose>
      Convert a data item of any type into a string such that we can 
      deserialize it later.

   <Arguments>
      data: the thing to seriailize.   Can be of essentially any type except
            objects.

   <Exceptions>
      TypeError if the type of 'data' isn't allowed

   <Side Effects>
      None.

   <Returns>
      A string suitable for deserialization.
  """

  # this is essentially one huge case statement...

  # None
  if type(data) == type(None):
    return 'N'

  # Boolean
  elif type(data) == type(True):
    if data == True:
      return 'BT'
    else:
      return 'BF'

  # Integer / Long
  elif type(data) is int or type(data) is long:
    datastr = str(data) 
    return 'I'+datastr


  # Float
  elif type(data) is float:
    datastr = str(data) 
    return 'F'+datastr


  # Complex
  elif type(data) is complex:
    datastr = str(data) 
    if datastr[0] == '(' and datastr[-1] == ')':
      datastr = datastr[1:-1]
    return 'C'+datastr



  # String
  elif type(data) is str:
    return 'S'+data


  # List or tuple or set or frozenset
  elif type(data) is list or type(data) is tuple or type(data) is set or type(data) is frozenset:
    # the only impact is the first letter...
    if type(data) is list:
      mystr = 'L'
    elif type(data) is tuple:
      mystr = 'T'
    elif type(data) is set:
      mystr = 's'
    elif type(data) is frozenset:
      mystr = 'f'
    else:
      raise Exception("InternalError: not a known type after checking")

    for item in data:
      thisitem = serialize_serializedata(item)
      # Append the length of the item, plus ':', plus the item.   1 -> '2:I1'
      mystr = mystr + str(len(thisitem))+":"+thisitem

    mystr = mystr + '0:'

    return mystr


  # dict
  elif type(data) is dict:
    mystr = 'D'

    keysstr = serialize_serializedata(data.keys())
    # Append the length of the list, plus ':', plus the list.  
    mystr = mystr + str(len(keysstr))+":"+keysstr
    
    # just plop the values on the end.
    valuestr = serialize_serializedata(data.values())
    mystr = mystr + valuestr

    return mystr


  # Unknown!!!
  else:
    raise TypeError("Unknown type '"+str(type(data))+"' for data :"+str(data))



def serialize_deserializedata(datastr):
  """
   <Purpose>
      Convert a serialized data string back into its original types.

   <Arguments>
      datastr: the string to deseriailize.

   <Exceptions>
      ValueError if the string is corrupted
      TypeError if the type of 'data' isn't allowed

   <Side Effects>
      None.

   <Returns>
      Items of the original type
  """

  if type(datastr) != str:
    raise TypeError("Cannot deserialize non-string of type '"+str(type(datastr))+"'")
  typeindicator = datastr[0]
  restofstring = datastr[1:]

  # this is essentially one huge case statement...

  # None
  if typeindicator == 'N':
    if restofstring != '':
      raise ValueError("Malformed None string '"+restofstring+"'")
    return None

  # Boolean
  elif typeindicator == 'B':
    if restofstring == 'T':
      return True
    elif restofstring == 'F':
      return False
    raise ValueError("Malformed Boolean string '"+restofstring+"'")

  # Integer / Long
  elif typeindicator == 'I':
    try:
      return int(restofstring) 
    except ValueError:
      raise ValueError("Malformed Integer string '"+restofstring+"'")


  # Float
  elif typeindicator == 'F':
    try:
      return float(restofstring) 
    except ValueError:
      raise ValueError("Malformed Float string '"+restofstring+"'")

  # Float
  elif typeindicator == 'C':
    try:
      return complex(restofstring) 
    except ValueError:
      raise ValueError("Malformed Complex string '"+restofstring+"'")



  # String
  elif typeindicator == 'S':
    return restofstring

  # List / Tuple / set / frozenset / dict
  elif typeindicator == 'L' or typeindicator == 'T' or typeindicator == 's' or typeindicator == 'f':
    # We'll split this and keep adding items to the list.   At the end, we'll
    # convert it to the right type

    thislist = []

    data = restofstring
    # We'll use '0:' as our 'end separator'
    while data != '0:':
      lengthstr, restofdata = data.split(':', 1)
      length = int(lengthstr)

      # get this item, convert to a string, append to the list.
      thisitemdata = restofdata[:length]
      thisitem = serialize_deserializedata(thisitemdata)
      thislist.append(thisitem)

      # Now toss away the part we parsed.
      data = restofdata[length:]

    if typeindicator == 'L':
      return thislist
    elif typeindicator == 'T':
      return tuple(thislist)
    elif typeindicator == 's':
      return set(thislist)
    elif typeindicator == 'f':
      return frozenset(thislist)
    else:
      raise Exception("InternalError: not a known type after checking")


  elif typeindicator == 'D':

    lengthstr, restofdata = restofstring.split(':', 1)
    length = int(lengthstr)

    # get this item, convert to a string, append to the list.
    keysdata = restofdata[:length]
    keys = serialize_deserializedata(keysdata)

    # The rest should be the values list.
    values = serialize_deserializedata(restofdata[length:])

    if type(keys) != list or type(values) != list or len(keys) != len(values):
      raise ValueError("Malformed Dict string '"+restofstring+"'")
    
    thisdict = {}
    for position in xrange(len(keys)):
      thisdict[keys[position]] = values[position]
    
    return thisdict




  # Unknown!!!
  else:
    raise ValueError("Unknown typeindicator '"+str(typeindicator)+"' for data :"+str(restofstring))




### Automatically generated by repyhelper.py ### /home/affe/tda596/blackboard/demokit/serialize.repy
