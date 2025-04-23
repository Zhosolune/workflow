import os
import sys
import json
from typing import Dict, Any

# 添加父目录到系统路径，以便导入核心模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.base_module import BaseModule
from core.workflow import Workflow
from core.module_registry import ModuleRegistry, gmodule_registry
from core.engine import WorkflowEngine

from examples.example_modules import (
    NumberGeneratorModule,
    MathOperationModule,
    TextProcessingModule,
    ConditionalModule,
    TimeDelayModule
)

def print_callback(event_type: str, event_data: Dict[str, Any]) -> None:
    """打印工作流执行进度的回调函数"""
    if event_type == "start":
        print(f"开始执行工作流: {event_data['workflow_name']}")
    elif event_type == "module_start":
        print(f"开始执行模块: {event_data['module_name']}")
    elif event_type == "module_complete":
        print(f"模块 {event_data['module_name']} 执行完成，输出: {event_data['outputs']}")
    elif event_type == "module_error":
        print(f"模块 {event_data['module_name']} 执行错误: {event_data['error']}")
    elif event_type == "pause":
        print("工作流执行暂停")
    elif event_type == "resume":
        print("工作流执行恢复")
    elif event_type == "complete":
        print("工作流执行完成")
    elif event_type == "error":
        print(f"工作流执行错误: {event_data['error']}")


def create_example_workflow() -> Workflow:
    """创建示例工作流"""
    # 创建工作流
    workflow = Workflow("示例工作流", "这是一个演示工作流系统功能的示例")
    
    # 创建模块
    num_gen1 = NumberGeneratorModule("随机数生成器1")
    num_gen1.set_parameter("min_value", 1)
    num_gen1.set_parameter("max_value", 10)
    
    num_gen2 = NumberGeneratorModule("随机数生成器2")
    num_gen2.set_parameter("min_value", 5)
    num_gen2.set_parameter("max_value", 15)
    
    math_op = MathOperationModule("加法运算")
    math_op.set_parameter("operation", "add")
    
    # 创建一个固定阈值生成器
    threshold_gen = NumberGeneratorModule("阈值生成器")
    threshold_gen.set_parameter("min_value", 15)
    threshold_gen.set_parameter("max_value", 15)  # 固定值为15
    
    condition = ConditionalModule("条件判断")
    condition.set_parameter("condition", "greater")
    
    delay = TimeDelayModule("延迟模块")
    delay.set_parameter("delay_seconds", 0.5)
    
    text_proc = TextProcessingModule("文本处理")
    text_proc.set_parameter("operation", "uppercase")
    
    # 为文本处理模块提供默认输入
    text_input = NumberGeneratorModule("文本默认输入")
    text_input.set_parameter("min_value", 123)
    text_input.set_parameter("max_value", 123)  # 固定值
    
    # 添加模块到工作流
    workflow.add_module(num_gen1)
    workflow.add_module(num_gen2)
    workflow.add_module(math_op)
    workflow.add_module(threshold_gen)
    workflow.add_module(condition)
    workflow.add_module(delay)
    workflow.add_module(text_proc)
    workflow.add_module(text_input)
    
    # 设置模块位置（用于UI显示）
    num_gen1.position = (100, 100)
    num_gen2.position = (100, 250)
    math_op.position = (300, 175)
    threshold_gen.position = (300, 325)
    condition.position = (500, 175)
    delay.position = (700, 100)
    text_proc.position = (700, 250)
    text_input.position = (500, 325)
    
    # 连接模块
    # 将随机数生成器连接到加法运算
    workflow.connect(
        num_gen1.id, list(num_gen1.output_ports.keys())[0],
        math_op.id, list(math_op.input_ports.keys())[0]
    )
    workflow.connect(
        num_gen2.id, list(num_gen2.output_ports.keys())[0],
        math_op.id, list(math_op.input_ports.keys())[1]
    )
    
    # 将加法结果连接到条件判断
    workflow.connect(
        math_op.id, list(math_op.output_ports.keys())[0],
        condition.id, list(condition.input_ports.keys())[0]
    )
    
    # 将阈值生成器连接到条件判断
    workflow.connect(
        threshold_gen.id, list(threshold_gen.output_ports.keys())[0],
        condition.id, list(condition.input_ports.keys())[1]
    )
    
    # 将条件判断结果连接到后续模块
    workflow.connect(
        condition.id, list(condition.output_ports.keys())[0],  # true_result
        delay.id, list(delay.input_ports.keys())[0]
    )
    
    # 为文本处理模块提供输入
    workflow.connect(
        text_input.id, list(text_input.output_ports.keys())[0],
        text_proc.id, list(text_proc.input_ports.keys())[0]
    )
    
    # 将条件判断的false结果连接到后续模块
    workflow.connect(
        condition.id, list(condition.output_ports.keys())[1],  # false_result
        text_proc.id, list(text_proc.input_ports.keys())[0]
    )
    
    return workflow


def main():
    """主函数"""
    print("开始注册模块...")
    
    # 注册模块类型
    gmodule_registry.register(NumberGeneratorModule, "基础")
    gmodule_registry.register(MathOperationModule, "基础")
    gmodule_registry.register(TextProcessingModule, "基础")
    gmodule_registry.register(ConditionalModule, "控制")
    gmodule_registry.register(TimeDelayModule, "控制")
    
    print(f"已注册的模块类别: {gmodule_registry.get_categories()}")
    
    # 创建工作流引擎
    engine = WorkflowEngine(gmodule_registry)
    
    # 注册进度回调
    engine.register_progress_callback(print_callback)
    
    # 创建示例工作流
    workflow = create_example_workflow()
    
    print(f"创建的工作流: {workflow.name}\n")
    print(f"工作流中的模块数量: {len(workflow.modules)}")
    print(f"工作流中的连接数量: {len(workflow.connections)}")
    
    # 保存工作流到文件
    save_path = os.path.join(os.path.dirname(__file__), "example_workflow.json")
    workflow.save(save_path)
    print(f"工作流已保存到: {save_path}")
    
    # 执行工作流
    print("\n开始执行工作流...")
    engine._workflows[workflow.id] = workflow
    engine._current_workflow_id = workflow.id
    engine.execute(async_run=False)  # 同步执行，便于演示
    
    # 输出执行结果
    print("\n执行结果:")
    for module_id, outputs in engine.execution_results.items():
        module_name = engine.current_workflow.modules[module_id].name
        print(f"模块 '{module_name}' 的输出: {outputs}")


if __name__ == "__main__":
    main() 