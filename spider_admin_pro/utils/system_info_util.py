# -*- coding: utf-8 -*-
import psutil


class SystemInfoUtil(object):

    @classmethod
    def get_format_byte(cls, value):
        """字节"""
        kb, b = divmod(value, 1024)
        mb, kb = divmod(kb, 1024)
        gb, mb = divmod(mb, 1024)

        if gb > 0:
            return f'{round(gb + mb * 0.001)}GB'
        elif mb > 0:
            return f'{round(mb + kb * 0.001)}MB'
        elif kb > 0:
            return f'{round(kb + b * 0.001)}KB'
        else:
            return f'{round(b)}B'

    @classmethod
    def get_virtual_memory(cls):
        """
        内存使用情况

        total:     总内存
        available: 可用内存
        percent:   内存使用率
        used:      已使用的内存
        :return:
        """
        virtual_memory = psutil.virtual_memory()

        return {
            'total': virtual_memory.total,
            'total_format': cls.get_format_byte(virtual_memory.total),
            'available': virtual_memory.available,
            'available_format': cls.get_format_byte(virtual_memory.available),
            'percent': round(virtual_memory.percent),
            'used': virtual_memory.used,
            'used_format': cls.get_format_byte(virtual_memory.used),
        }

    @classmethod
    def get_disk_usage(cls):
        """磁盘使用情况"""
        disk_usage = psutil.disk_usage('/')
        return {
            'total': disk_usage.total,
            'total_format': cls.get_format_byte(disk_usage.total),
            'used': disk_usage.used,
            'used_format': cls.get_format_byte(disk_usage.used),
            'free': disk_usage.free,
            'free_format': cls.get_format_byte(disk_usage.free),
            'percent': round(disk_usage.percent),
        }

    @classmethod
    def get_net_io_counters(cls):
        """
        查看网卡的网络 IO 统计信息

        bytes_sent: 发送的字节数
        bytes_recv: 接收的字节数
        packets_sent: 发送的包数据量
        packets_recv: 接收的包数据量
        errin: 接收包时, 出错的次数
        errout: 发送包时, 出错的次数
        dropin: 接收包时, 丢弃的次数
        dropout: 发送包时, 丢弃的次数

        """
        snetio = psutil.net_io_counters()

        return {
            'bytes_sent': snetio.bytes_sent,
            'bytes_sent_format': cls.get_format_byte(snetio.bytes_sent),
            'bytes_recv': snetio.bytes_recv,
            'bytes_recv_format': cls.get_format_byte(snetio.bytes_recv),
        }


if __name__ == '__main__':
    print(SystemInfoUtil.get_net_io_counters())
    print(SystemInfoUtil.get_virtual_memory())
    print(SystemInfoUtil.get_disk_usage())
