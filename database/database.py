import sqlite3

def initialize():
    sqlite3.connect('pipelineforge.db').close()
