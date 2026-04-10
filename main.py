#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
企业微信LOCATION事件处理插件
"""

from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star
from astrbot.api import logger

class WecomLocationPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        logger.info("企业微信LOCATION事件处理插件初始化")

    @filter.event_message_type(filter.EventMessageType.ALL)
    async def handle_location_event(self, event: AstrMessageEvent):
        """
        处理企业微信LOCATION事件
        """
        # 获取原始消息
        raw_message = event.message_obj.raw_message
        
        # 检查是否为企业微信平台的LOCATION事件
        if event.get_platform_name() == "wecom":
            # 处理事件对象
            event_data = {}
            if hasattr(raw_message, '__dict__'):
                # 将对象转换为字典
                event_data = vars(raw_message)
                # 检查是否有 _data 属性（可能是事件对象的内部数据）
                if hasattr(raw_message, '_data'):
                    event_data = raw_message._data
            elif isinstance(raw_message, dict):
                # 已经是字典，直接使用
                event_data = raw_message
            
            # 检查消息类型和事件类型
            if event_data.get('MsgType') == 'event' and event_data.get('Event') == 'LOCATION':
                # 提取位置信息
                latitude = event_data.get('Latitude', '0')
                longitude = event_data.get('Longitude', '0')
                precision = event_data.get('Precision', '0')
                
                # 构造位置信息消息
                location_info = f"收到位置信息：\n" \
                              f"纬度：{latitude}\n" \
                              f"经度：{longitude}\n" \
                              f"精度：{precision}米"
                
                logger.info(f"处理LOCATION事件：{location_info}")
                
                # 发送位置信息回复
                yield event.plain_result(location_info)

    async def terminate(self):
        """
        插件被卸载/停用时调用
        """
        logger.info("企业微信LOCATION事件处理插件已停止")

# 导出插件实例
plugin = WecomLocationPlugin

__all__ = ['plugin']