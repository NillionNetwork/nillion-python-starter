import os
import py_nillion_client as nillion

def getUserKeyFromFile(userkey_filepath):
    return nillion.UserKey.from_file(userkey_filepath)

def getNodeKeyFromFile(nodekey_filepath):
    return nillion.NodeKey.from_file(nodekey_filepath)
