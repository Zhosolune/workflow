"""
可拖拽工作流系统
============

这是一个用Python实现的灵活可扩展的工作流系统，支持创建、编辑和执行模块化工作流。

主要特性:
- 基于模块化设计，每个模块具有明确的输入输出接口
- 支持任意类型的数据流转
- 可视化友好，支持与前端框架集成
- 可序列化，支持保存和加载工作流
- 提供可扩展的基类，支持自定义模块开发

示例:
```python
from workflow import WorkflowEngine, BaseModule, Workflow, gmodule_registry

# 注册自定义模块
gmodule_registry.register(MyCustomModule, "自定义")

# 创建工作流引擎
engine = WorkflowEngine(gmodule_registry)

# 创建工作流
workflow = engine.create_workflow("我的工作流")

# 添加模块并连接
mod1 = gmodule_registry.create_instance("MyCustomModule", "模块1")
mod2 = gmodule_registry.create_instance("MyCustomModule", "模块2")

workflow.add_module(mod1)
workflow.add_module(mod2)

# 连接模块
workflow.connect(
    mod1.id, mod1.output_ports[0].id,
    mod2.id, mod2.input_ports[0].id
)

# 执行工作流
engine.execute()
```
"""

# 导出核心类
from .core.base_module import BaseModule, Port
from .core.workflow import Workflow, Connection
from .core.module_registry import ModuleRegistry, gmodule_registry
from .core.engine import WorkflowEngine, ExecutionStatus, ProgressCallbackType

__all__ = [
    'BaseModule',
    'Port',
    'Workflow',
    'Connection',
    'ModuleRegistry',
    'gmodule_registry',
    'WorkflowEngine',
    'ExecutionStatus',
    'ProgressCallbackType'
] 