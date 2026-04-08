"""处理器注册表"""
from .kf import KFProcessor
from .qms import QMSProcessor
from .failure_case import FailureCaseProcessor

_PROCESSORS = {
    'kf': KFProcessor,
    'qms': QMSProcessor,
    'failure_case': FailureCaseProcessor,
}


def get_processor(name: str = 'kf'):
    """获取处理器实例"""
    cls = _PROCESSORS.get(name)
    if cls is None:
        available = list(_PROCESSORS.keys())
        raise ValueError(f"未知处理器: {name}，可用: {available}")
    return cls()


def list_processors():
    """列出所有可用处理器"""
    return [
        {'name': name, 'display_name': cls().display_name}
        for name, cls in _PROCESSORS.items()
    ]
