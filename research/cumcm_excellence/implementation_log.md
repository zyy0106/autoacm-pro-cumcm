# AutoMCM-Pro 国赛 Skill 实施日志

实施日期：2026-09-10。范围仅为 CUMCM/国赛；CM-11 未启用。

## CM-01 案例证据协议

- 修改：扩展 `cumcm-case-study-review`，新增冻结、E0--E4、原页视觉核验、附件血缘、论文—代码匹配状态、反例与回放规则；新增 `evidence-schemas.md`。
- 原不足：OCR 摘要和 README 存在即可进入总结，无法阻止断裂公式、未知代码关系和单篇经验被过度推广。
- 提升/Agent 帮助：Agent 必须区分事实、解释、规则候选和不可迁移项；只有 E3 可成为默认候选，E4 还需独立回放。
- 依据：OCR 数据库特征为主；公式断行与代码对应不确定性来自本次语料审计。

## CM-02 问题指纹与问题图

- 修改：SOP、CUMCM Master 和各 runtime 绑定要求输出 `problem_fingerprint.json`、`problem_graph.json`。
- 原不足：按小问罗列模型，没有共享状态、接口、依赖与交付物映射。
- 提升/Agent 帮助：Agent 先识别模型单元再分工；当前 A 题可表达 M1(Q1--Q3) 与 M2(Q4)，但允许有依据的不同拆分。
- 依据：A 题结构 + 数据库 P-001（E3）。

## CM-03 国赛动态流水线

- 修改：`pipeline_manager.py` 新增 CUMCM-only 的 `--questions`、`--model-units`、`--model-map`，动态生成模型阶段并按 `depends_on` 调度；状态显示小问/单元映射。
- 原不足：固定三个模型槽，把问题数量等同模型数量，并假定所有 build 可同时运行。
- 提升/Agent 帮助：共享模型验证完成前，下游单元不会被并行启动；旧 `--problems` 仍兼容，MCM/ICM 分支保持原状态形状。
- 依据：A 题依赖结构 + 数据库 P-001（E3）。

## CM-04 附件与交付契约

- 修改：新增 `quality_gate.py artifact-contract`；检查输入/输出 ID、路径、schema、单位、处理、来源、验证和开放歧义；终稿模式用标准库解析 XLSX 的工作表、行列、省略号和小数精度。
- 原不足：EDA 不约束题面附件和最终模板，求解网格、附件采样和输出网格容易混淆。
- 提升/Agent 帮助：Agent 在建模前锁定输入输出接口；Q4 时变表面列作为 WARN 进入 Checkpoint，不会被静默猜测。
- 依据：A 题及附件 authoritative；数据库只作工作流旁证。

## CM-05 基线驱动的模型选择

- 修改：SOP、Master 和绑定加入“机制→约束→最小基线→失效→求解器→新增收益→回退”。
- 原不足：先报算法名，缺少可解释基线、失败条件和回退。
- 提升/Agent 帮助：复杂模型必须证明相对基线增加了什么；没有合理基线时记录原因，不伪造解析解。
- 依据：数据库 P-002（E3）+ A 题非线性系数特征。

## CM-06 验证 profile

- 修改：CUMCM 将原固定验证菜单改为按失效源选择；连续场候选含初边值、对称/边界残差、系数定义域、时空收敛、简化基准、事件夹逼和移动域一致性。
- 原不足：普通 ODE/回归阈值被写成普适规定，缺少 PDE、移动边界与事件检查。
- 提升/Agent 帮助：Agent 必须给阈值的量纲、输入精度、容差或收敛依据，并记录证据位置。
- 依据：数据库 P-003（E3）+ A 题 PDE/移动域特征。

## CM-07 证据账本

- 修改：新增 `quality_gate.py evidence-ledger`；只有核心且 `verified` 的条目能覆盖小问和指定交付物，缺来源为 FAIL，非核心草稿为 WARN。
- 原不足：旧 `consist` 仅正则扫描少数物理常数，无法校验正文结论与程序/Excel 输出血缘。
- 提升/Agent 帮助：摘要和结论只能消费已验证条目，冲突可定位到文件/字段。
- 依据：《修改方向》P0 + A 题多问、多文件特征。

## CM-08 动态论文骨架

- 修改：删除国赛 Master/模板中的固定十章、5--7条假设、固定 ±10/±20、至少8篇文献、固定优缺点条数；改为功能覆盖和模型单元组织。
- 原不足：数量硬编码诱导套话、无依据扰动和凑文献。
- 提升/Agent 帮助：假设逐条说明依据、影响和边界；敏感性范围来自真实误差；摘要最后从证据账本生成。
- 依据：数据库 P-004（E3）+ A 题共享模型结构。

## CM-09 2026 国赛完整代码附录

- 修改：SOP、国赛模板和 Claude 绑定纠正为支撑材料清单 + 全部完整可运行源码；launch-check 检查遗漏与 `firstline/lastline` 节选。
- 原不足：SOP 的国赛“默认节选”与本地 2026 官方格式第五、十一条冲突。
- 提升/Agent 帮助：Agent 不会因沿用美赛式页限策略遗漏国赛完整程序；MCM/ICM 节选规则未变。
- 依据：本地 `format2026.doc` authoritative。

## CM-10 证据型写作警告

- 修改：`style_check.py evidence-scan` 提示未引用图、摘要数值无账本、比较无基线和假设无下游引用；只 WARN，不自动改文。
- 原不足：原检查只看列表、套话、句长和重复，不能发现论证缺口。
- 提升/Agent 帮助：Agent 得到带行号的证据问题，而不会把文风分数误当论文质量。
- 依据：数据库图表—结论闭环特征 +《修改方向》证据链要求。

## 隔离与验证

- 未修改 `templates/mcm_template.tex` 和 `templates/mcm_memo_template.tex`；当前 SHA-256 分别为 `EA7CF2EC5DCDE4E6FC04ACE0B4E5FEAC5ED977F196686BF90E3E0498F28CF790`、`9AA6FCD10B23403659FC360B23FF3F1B39071AA2DF94BD1C4F29BE17171546EE`。
- Python 语法检查通过；三个主要 Skill 的 `quick_validate.py` 通过。
- 单元测试覆盖 4问/2单元依赖调度、MCM 旧阶段形状、金融/决策型非物理附件契约、artifact WARN 和 evidence PASS/FAIL；通用门禁不要求 PDE 字段。
- 当前 A 题静态附件契约返回 WARN，唯一开放项为 Q4 时变表面列约定，符合预期。
- 国赛模板使用本机 TeX Live 2025 / XeLaTeX 编译成功（6 页）；最终日志无 LaTeX、未定义引用、页眉高度或 overfull 警告，`evidence-scan` 为 PASS。
- 标准库 XLSX 检查器对原始 `result1.xlsx` 模板识别出省略号、仅4个数据行和仅5个半径列，证明终稿门禁能拦截未填充模板。
- DSH 绑定保留其既有 `whenToUse` frontmatter；该字段不属于 Codex `quick_validate.py` schema，因此 DSH 文件仅做 YAML/内容审计，不为迎合 Codex 验证器删除运行时专属字段。
- 这些结果证明流程行为和回归边界，不证明获奖概率提升；E3 规则尚未因本次静态测试自动升级为 E4。
