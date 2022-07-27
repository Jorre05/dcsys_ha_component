from __future__ import annotations

import logging
import requests

from .const import *
#http://dcsys.struyve.local/cgi-bin/main?item=-1&atype=exeseq&oname=60&parameter=1

_LOGGER = logging.getLogger(__name__)

def getIoRawValue(host,io_id) -> str:
    request = HTTP_PREFIX + host + HTTP_GET_IO_PATH + io_id
    _LOGGER.debug("getIoRawValue: " + io_id + " " +request)
    response = requests.get(request)
    _LOGGER.debug("getIoRawValue response: " +  response.text)
    return response.text

def setIoRawValue(host,io_id,parm)  -> None:
    request = HTTP_PREFIX + host + HTTP_SET_IO_PATH + io_id + HTTP_OVAL_PREFIX + str(parm)
    _LOGGER.debug("setIoRawValue: " + io_id + " " +request)
    response = requests.get(request)
    _LOGGER.debug("setIoRawValue response: " +  response.text)

def execSequence(host,seq_id,parm)  -> None:
    request = HTTP_PREFIX + host + HTTP_GET_EXEC_PATH + seq_id + HTTP_PARM_PREFIX + str(parm)
    _LOGGER.debug("execSequence: " + seq_id + " " +request)
    response = requests.get(request)
    _LOGGER.debug("execSequence response: " +  response.text)

def getIoCalculatedValue(host,io_id) -> str:
    request = HTTP_PREFIX + host + HTTP_GET_IOCV_PATH + io_id
    _LOGGER.debug("getIoCalculatedValue: " + io_id + " " +request)
    response = requests.get(request)
    _LOGGER.debug("getIoCalculatedValue response: " +  response.text)
    return response.text
    
def getIoSwoCalculatedValue(host,io_id) -> str:
    request = HTTP_PREFIX + host + HTTP_GET_IOSWCV_PATH + io_id
    _LOGGER.debug("getIoSwoCalculatedValue: " + io_id + " " +request)
    response = requests.get(request)
    _LOGGER.debug("getIoSwoCalculatedValue response: " +  response.text)
    return response.text