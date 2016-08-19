from abc import ABCMeta, abstractmethod
import time

_handler = None

def connect_loghandler(handler):
    global _handler
    _handler = handler

def log(subject, text):
    if not _handler:
        print time.strftime("%H:%M:%S ") + subject + ": " + text
    else:
        _handler.log(subject, text)


class CloudProvider:
    __metaclass__ = ABCMeta

    @abstractmethod
    def create_instance(self, region, subnet_id, name, is_privileged=False):
        return False

    @abstractmethod
    def create_vpc(self, vpc_name, vpc_region, cidr_block):
        return False

    @abstractmethod
    def shutdown_all_instances_in_subnet(self, region_name, subnet_id):
        return False

    @abstractmethod
    def delete_vpc(self, region_name, vpc_id):
        return False

    @abstractmethod
    def create_subnet(self, region_name, vpc_id, subnet_name, cidr_block, availability_zone):
        return False

    @abstractmethod
    def delete_subnet(self, region_name, subnet_id):
        return False