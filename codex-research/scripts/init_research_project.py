#!/usr/bin/env python3
"""Create missing research records; preserve every existing regular file."""
import argparse
from datetime import date
from pathlib import Path


def initialize(project: Path, day: str):
    date.fromisoformat(day)
    root = project.expanduser().resolve(strict=True)
    if not root.is_dir():
        raise ValueError('Project must be an existing directory')
    history = root / 'history'
    if history.is_symlink() or (history.exists() and not history.is_dir()):
        raise ValueError('history must be a real directory')
    records = {
        'AGENTS.md': '''# 研究工作约定

## 接手与研究范围
- 每轮先读本文件、SUMMARY.md与history/README.md；实验任务再读EXPERIMENTS.md、配置和实际代码。
- 状态、路径和资源使用前核实；摘要、历史和待办不能代替当前事实或执行授权。
- 遵守用户指令和已明确项目边界，采用最小修改；未知协议标注待确认。

## 实验与评估
- 先明确基准、核心变量、假设及配置；多变量差异披露，不声称单因素因果。
- train更新参数，valid按合同选模，test只按预定协议评估，不用于调参、筛样本或挑权重。
- 保留实验ID→源码→配置→权重→评估→结果证据链，正式与诊断结果分开。
- 硬件、seed、预算、编号和提交推送权限按本项目实际约定，不继承其它项目设置。

## 文档维护合同
- AGENTS记录固定规则，EXPERIMENTS记录研究设计和主要结果，SUMMARY记录当前交接；history按日记录决定、理由、更正、未解决项和证据。
- 每轮最终回复前合并当天history/YYYY-MM-DD.md、更新history/README.md和SUMMARY；设计/结果变化时更新EXPERIMENTS，规则变化时更新AGENTS。
- 无实质变化时只更新最近交接，不追加重复流水账；当天记录不存在时注明仅核对/讨论。
- 压缩摘要前先归档唯一信息，跨日不覆盖旧日历史；补录和更正注明日期、来源与限制。
- 不记录密钥，不虚构理由，不承诺后台自动记忆；读取或写入失败如实说明。

## 项目特定约定
尚未提炼：需依据项目代码、已有文档和当前会话核实后补充。
''',
        'EXPERIMENTS.md': f'''# 实验账本

更新：{day}。本文件仅初始化结构，实验事实尚未核实。
规则见[AGENTS](AGENTS.md)，当前交接见[SUMMARY](SUMMARY.md)，历史见[索引](history/README.md)。

## 1. 研究主线
尚未提炼：需读取项目说明与本次目标。

## 2. 实验 idea 与设计
尚未登记：不能据此认定项目没有历史实验。需核实基准、变量、假设、配置和状态。

## 3. 结果与讨论
尚未核实正式结果；后续按数据集/任务组织，明确端点、指标、分母及证据。

## 4. 下一步
完成项目阅读与事实提炼；待办本身不提供训练或评估授权。
''',
        'SUMMARY.md': f'''# 当前交接

更新：{day}。本文件仅初始化结构，任务与资源状态尚未核实。

## 最近交接
建立研究记录结构；需要继续用实际项目事实填充，不能将结构初始化视为接手完成。

## 长期约束
见[AGENTS](AGENTS.md)；项目特定约束待提炼。

## 当前状态
尚未核实。

## 关键决策与教训
待依据当前会话与证据提炼。

## 下一步与保留限制
读取项目入口、配置和已有记录，核实实际状态；不覆盖历史产物。

## 证据入口
[规则](AGENTS.md)、[账本](EXPERIMENTS.md)、[历史索引](history/README.md)、[当天记录](history/{day}.md)。
''',
        'history/README.md': f'''# 每日会话提炼索引

[规则](../AGENTS.md)、[实验账本](../EXPERIMENTS.md)、[当前交接](../SUMMARY.md)。

| 日期 | 主题 |
| --- | --- |
| [{day}]({day}.md) | 研究记录初始化；具体会话提炼待补充 |

历史不是实时状态或新执行授权；补录须注明来源与不完整性，跨日保留旧记录。
''',
        f'history/{day}.md': f'''# {day}

## 研究记录初始化
- 决定：根据codex-research建立缺失的三份主文档、历史索引与当天记录，已有文档保持原样。
- 理由：区分固定规则、实验事实、当前交接与长期决策历史，防止滚动摘要覆盖唯一信息。
- 已执行：仅创建缺失文件；该记录不表示已经读取项目代码或验证实验状态。
- 待提炼：本次用户目标、实际讨论与理由、已核实状态、未解决项和证据入口。
- 证据：[规则](../AGENTS.md)、[账本](../EXPERIMENTS.md)、[摘要](../SUMMARY.md)。
''',
    }
    # Validate all destinations before creating any document.
    for name in records:
        target = root / name
        if target.is_symlink() or (target.exists() and not target.is_file()):
            raise ValueError(f'Refusing non-regular document: {target}')
    history.mkdir(exist_ok=True)
    for name, content in records.items():
        target = root / name
        try:
            with target.open('x', encoding='utf-8') as handle:
                handle.write(content)
            print(f'CREATED {target}')
        except FileExistsError:
            print(f'PRESERVED {target}')
    print('NEXT: read and merge actual project/session facts; update any existing index.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', required=True, type=Path)
    parser.add_argument('--date', required=True, help='YYYY-MM-DD in the project timezone')
    args = parser.parse_args()
    try:
        initialize(args.project, args.date)
    except (ValueError, OSError) as error:
        parser.exit(1, f'ERROR: {error}\n')


if __name__ == '__main__':
    main()
