from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import numpy as np
import json
import os
import asyncio
import re


PLUGIN_DIR=os.path.dirname(__file__)
DATA_DIR=os.path.join(PLUGIN_DIR,"data","help_dic.json")


@register("helloworld", "YourName", "一个简单的 Hello World 插件", "1.0.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""
    
    # 注册指令的装饰器。指令名为 helloworld。注册成功后，发送 `/helloworld` 就会触发这个指令，并回复 `你好, {user_name}!`
    @filter.permission_type(filter.PermissionType.ADMIN)
    @filter.command("添加帮助")
    async def add_help(self,event,hk:str):
        from astrbot.core.platform.sources.aiocqhttp.aiocqhttp_message_event import AiocqhttpMessageEvent
        data_dic={}
        with open(f"{DATA_DIR}","r",encoding="utf-8") as f:
            data_dic=json.load(f)
        
        if hk in data_dic:
            yield event.plain_result(f"已有该条目，无法重复创建")
        else:
            massage_list=event.message_str
            pattern = r'(?:\s.*?){2}(.*)'
            help = re.search(pattern, massage_list)

            massage=help.group(1)
            data_dic[hk]=massage
            with open(f"{DATA_DIR}","w",encoding="utf-8") as f:
                data_j=json.dumps(data_dic,ensure_ascii=False)
                f.write(data_j)
            yield event.plain_result(f"恭喜成功创建帮助条目")
    

    
    @filter.permission_type(filter.PermissionType.ADMIN)
    @filter.command("删除帮助")
    async def del_help(self,event,hk:str):
        data_dic={}
        with open(f"{DATA_DIR}","r",encoding="utf-8") as f:
            data_dic=json.load(f)
        
        if hk in data_dic:
            del data_dic[hk]
            with open(f"{DATA_DIR}","w",encoding="utf-8") as f:
                data_j=json.dumps(data_dic,ensure_ascii=False)
                f.write(data_j)
            yield event.plain_result(f"恭喜成功删除该条目")
        else:
            yield event.plain_result(f"该条目不存在")


    @filter.permission_type(filter.PermissionType.ADMIN)
    @filter.command("修改帮助")
    async def fix_help(self,event,hk:str,nhv:str):
        from astrbot.core.platform.sources.aiocqhttp.aiocqhttp_message_event import AiocqhttpMessageEvent
        data_dic={}
        with open(f"{DATA_DIR}","r",encoding="utf-8") as f:
            data_dic=json.load(f)
        
        if hk in data_dic:
            massage_list=event.message_str
            pattern = r'(?:\s.*?){2}(.*)'
            help = re.search(pattern, massage_list)

            massage=help.group(1)
            data_dic[hk]=nhv
            with open(f"{DATA_DIR}","w",encoding="utf-8") as f:
                data_j=json.dumps(data_dic,ensure_ascii=False)
                f.write(data_j)
            yield event.plain_result(f"恭喜成功修改该条目")
        else:
            yield event.plain_result(f"该条目不存在")
    

    @filter.command("帮助")
    async def help_list(self,event:AstrMessageEvent):
        data_dic={}
        with open(f"{DATA_DIR}","r",encoding="utf-8") as f:
            data_dic=json.load(f)
        yield event.plain_result("\n".join(f"{key}:{vel}"for key,vel in data_dic.items()) )
    

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
