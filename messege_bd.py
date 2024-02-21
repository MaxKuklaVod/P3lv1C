
# -*- coding: cp1251 -*-

import sqlite3 as sq
import os
from pathlib import Path


class data_base:
    #имя, ключи
    __name="intituled"
    __keys=[]
    

    #путь к файлу
    __file_name=""
    
    #категории
    __categories={}
    

    #sqlite
    __connect=None
    __cursor=None 
    

    #создаём файл и получаем категории  
    #Словарь типа {'столбец':'значение'}
    def __init__(self,file:str="untituled.bd",cats:dict={}):
        self.name=file
        self.file_name=file 

        self.categories=cats
        

    #имя файла
    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self,value:str):
        if not isinstance(value,str):
            raise Exception("Неверный аргумент")

        value_stripped=value.strip()
        
        if value_stripped=="":
            raise Exception("Неверный аргумент")
        
        self.__name=value_stripped


    #полный путь к файлу
    @property 
    def file_name(self):
        return self.__file_name 
    
    @file_name.setter
    def file_name(self,value:str):
        
        value_stripped=value.strip()
        
        if value_stripped=="" or not(isinstance(value,str)):
            raise Exception
        self.__file_name=os.path.join(Path(__file__).parent,value_stripped)

    

    #обработка категорий и их параметров
    @property
    def categories(self):
        return self.__categories 
    

    @categories.setter 
    def categories(self,value:dict):
        if not isinstance(value,dict):
            raise Exception('wrong argument')
        
        #названия категорий
        self.__keys=list(value.keys())

        
        print(self.__keys)


        self.__categories=value
    
    #старт
    def start(self):
        print(self.__file_name)
        try:
            self.__connect=sq.connect(self.file_name)
            self.__cursor=self.__connect.cursor()
        except:
            raise Exception("error")
        

    #стоп
    def stop(self):
        self.__connect.close()
        
    #создание таблицы
    def create(self):
        #сборка команды и имени таблицы
        create_comand=f"create table if not exists {self.name.strip('.bd')}("
    
        


        #добавляем категории в команду
        for column in self.__keys:
            create_comand+= f'{column} {self.categories[column]}, '
            



        create_comand=create_comand.rstrip(', ')
        create_comand+=')'
        
        print(create_comand)
        
  

        self.__cursor.execute(create_comand)
        
        self.__connect.commit()
        

    #вставка в таблицу
    def insert(self, *args):
        
            
        table_name=f"{self.name.strip('.bd')}("
        



        for column in self.__keys:
            table_name+=column+', '
            
        table_name=table_name.strip(', ')+')'




        insert_comand=f'''INSERT INTO {table_name} VALUES(?,{' ?,'*(len(args)-2)} ?)'''
        
        print(insert_comand)
        
        self.__cursor.execute(insert_comand,args)
        
        self.__connect.commit()
        
    #взятие. Словарь типа {'столбец':'значение'}
    def get (self,args:dict):
        if not isinstance(args,dict):
            raise Exception("Нужен словарь")
        
        get_command=f'''select * from {self.name.strip('.bd')} where'''
        
        #ключи условий
        args_keys=list(args.keys())
        #args_args=list(args.items())
        
        for key in args_keys:
            #проверка на ошибку
            if key in self.__keys:
                get_command+=f' {key} = "{args[key]}" and'
                
        get_command=get_command[:-4]
        print(get_command)
        self.__cursor.execute(get_command)
        
        records=self.__cursor.fetchall()

        for row in records:
            return row

        
            
        
   



