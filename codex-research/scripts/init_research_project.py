#!/usr/bin/env python3
"""Create missing research records; preserve every existing regular file."""
import argparse
from datetime import date
from pathlib import Path


def initialize(project: Path, day: str):
    date.fromisoformat(day)
    root = project.expanduser().resolve(strict=True)
    if not root.is_dir():
        raise ValueError("Project must be an existing directory")

    records = {
        "AGENTS.md": """# 研究工作约定

## 强制底线
- 使用状态、路径、权重、结果和任务状态前先核实；摘要和旧记录不能代替当前事实。
- train用于参数更新，valid按既定协议选模，test只做最终评估；不得用test调参、筛样本或挑权重。
- 诊断、冒烟与正式训练/评估分开；诊断授权不能自动扩展为正式训练、test或大规模资源使用。
- 保留实验ID→源码/commit→配置→权重→评估→结果证据链，正式产物不得被无关运行覆盖。
- 删除、清理、覆盖、强推等不可逆操作只在用户明确范围内执行；运行中的源码快照、日志和产物不得擅自清理。
- 不虚构完成状态、退出码、比较优势或未核实原因；失败、跳过、协议偏差和限制如实记录。

## 接手与范围
- 每轮先读本文件和SUMMARY.md；涉及实验时再读EXPERIMENTS.md、配置和实际代码。
- 遵守用户指令和已明确项目边界，采用最小修改；未知协议标注待确认。
- 硬件、seed、预算、分支和提交推送权限按本项目实际约定，不继承其它项目设置。

## 实验命名
- 正式实验默认使用稳定语义ID，不使用E001、P001等纯顺序编号；优先采用<Track>-<Scope>-<Variant>[-<Qualifier>]。
- ID本身应表达研究主线、作用范围和核心变量；具体词汇按项目语义确定，保持简短、唯一、路径安全。
- seed、日期、GPU、job ID、checkpoint、resume/retry等属于运行标识或元数据，不写入实验ID。
- 同一研究设计的重复运行共享实验ID，但每次运行保留独立run标识和产物证据。
- 迁移旧编号时保留“旧ID→新语义ID”映射，并同步核对配置、脚本、权重/checkpoint、结果、TensorBoard、日志、manifest和文档引用；仅做命名迁移时不得改变模型、数据、训练或评估计算。

## 文档维护合同
- AGENTS维护长期硬约束和项目边界；EXPERIMENTS维护实验设计与主要结果；SUMMARY维护全部跨会话交接、关键决定和证据入口。
- 每轮最终回复前，将新决定、理由、更正、状态变化和未解决项合并到SUMMARY。
- 设计、实验状态或结果变化时更新EXPERIMENTS；底层规则或长期执行边界变化时更新AGENTS。
- 不创建或维护history/YYYY-MM-DD.md；旧history仅作为遗留证据按需读取，不主动删除。
- 不记录密钥，不虚构理由，不承诺后台自动记忆；读取或写入失败如实说明。

## 项目特定约定
尚未提炼：需依据项目代码、已有文档和当前会话核实后补充。
""",
        "EXPERIMENTS.md": f"""# 实验账本

更新：{day}。本文件仅初始化结构，实验事实尚未核实。
规则见[AGENTS](AGENTS.md)，当前交接见[SUMMARY](SUMMARY.md)。

## 1. 研究主线
| 主线 / 基线 | 核心问题 | 当前结论 | 证据 |
| --- | --- | --- | --- |
| 待提炼 | 待读取项目说明与本次目标 | 尚未核实 | 待补充 |

## 2. 实验 idea 与设计
| 语义 ID | 基准 / 核心变化 | 假设 | 关键设置 | 状态 |
| --- | --- | --- | --- | --- |
| 待登记（Track-Scope-Variant） | 待核实 | 待核实 | 待补充 | 尚未核实 |

命名：实验ID表达研究设计；seed、日期、checkpoint等执行信息放在run metadata，不写入实验ID。

协议：待核实数据划分、选模、评估端点及重要例外。

## 3. 结果与讨论
| ID / 端点 | 数据集 / 划分 | 主要指标 | 结果 | 证据 |
| --- | --- | --- | --- | --- |
| 待登记 | 待核实 | 待核实 | 尚未核实 | 待补充 |

| 结论 / 限制 | 内容 |
| --- | --- |
| 初始化状态 | 不能据此认定项目没有历史实验或正式结果。 |

## 4. 下一步
| 优先级 | 问题 / 动作 | 所需证据或前置条件 | 授权状态 |
| --- | --- | --- | --- |
| P0 | 完成项目阅读与事实提炼 | README、配置、代码、已有结果 | 仅核实 |
""",
        "SUMMARY.md": f"""# 当前交接

更新：{day}。本文件仅初始化结构，任务与资源状态尚未核实。

## 最近交接
建立三文件研究记录结构；需要继续用实际项目事实填充，不能将结构初始化视为接手完成。

## 长期约束
见[AGENTS](AGENTS.md)；项目特定约束待提炼。

## 当前状态
| 项目 | 状态 | 证据 / 核实时间 |
| --- | --- | --- |
| 项目事实 | 尚未核实 | {day} 初始化 |

## 关键决策与教训
| 决定 / 更正 | 理由与影响 | 证据 |
| --- | --- | --- |
| 使用三文件记录模型 | AGENTS管硬规则，EXPERIMENTS管实验账本，SUMMARY承担全部跨会话交接 | [规则](AGENTS.md)、[账本](EXPERIMENTS.md) |

## 下一步与保留限制
读取项目入口、配置和已有记录，核实实际状态；不覆盖历史产物，不将待办视为执行授权。

## 证据入口
[规则](AGENTS.md)、[账本](EXPERIMENTS.md)。
""",
    }

    for name in records:
        target = root / name
        if target.is_symlink() or (target.exists() and not target.is_file()):
            raise ValueError(f"Refusing non-regular document: {target}")

    for name, content in records.items():
        target = root / name
        try:
            with target.open("x", encoding="utf-8") as handle:
                handle.write(content)
            print(f"CREATED {target}")
        except FileExistsError:
            print(f"PRESERVED {target}")

    print("NEXT: read and merge actual project/session facts into the three main documents.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True, type=Path)
    parser.add_argument("--date", required=True, help="YYYY-MM-DD in the project timezone")
    args = parser.parse_args()
    try:
        initialize(args.project, args.date)
    except (ValueError, OSError) as error:
        parser.exit(1, f"ERROR: {error}\n")


if __name__ == "__main__":
    main()
