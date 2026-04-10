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
        # 检查是否为企业微信平台
        if event.get_platform_name() == "wecom":
            logger.info(f"收到企业微信消息：{event.message_str}")
            logger.info(f"原始消息：{event.message_obj.raw_message}")
            
            # 尝试从不同来源获取位置信息
            # 1. 从原始消息中获取
            raw_message = event.message_obj.raw_message
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
            
            # 2. 检查消息内容中是否包含位置信息
            if not event_data:
                # 尝试从消息字符串中提取位置信息
                message_str = event.message_str
                if "LOCATION事件" in message_str:
                    # 从消息字符串中提取位置信息
                    import re
                    lat_match = re.search(r'纬度=(.*?),', message_str)
                    lon_match = re.search(r'经度=(.*?),', message_str)
                    precision_match = re.search(r'精度=(.*?)米', message_str)
                    
                    if lat_match and lon_match and precision_match:
                        latitude = lat_match.group(1)
                        longitude = lon_match.group(1)
                        precision = precision_match.group(1)
                        
                        # 构造位置信息消息
                        location_info = f"收到位置信息：\n" \
                                      f"纬度：{latitude}\n" \
                                      f"经度：{longitude}\n" \
                                      f"精度：{precision}米"
                        
                        logger.info(f"处理LOCATION事件：{location_info}")
                        
                        # 发送位置信息回复
                        yield event.plain_result(location_info)
                    return
            
            # 3. 从事件数据中提取位置信息
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