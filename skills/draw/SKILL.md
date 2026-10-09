---
name: tarot-draw
description: Use when a tarot spread and its positions are fixed and cards need to be shuffled, selected by the customer, revealed, or recorded.
---

# DRAW — Deterministic shuffle & selection (Scheme B)

**Prerequisite:** 已经在客户报数之前确定牌阵的牌数和顺序。塔罗牌名清单见 `references/deck.md`，可执行洗牌程序在本 Skill 目录的 `scripts/tarot_shuffle.py`，**必须实际读取并运行程序，不得用语言模型假装已运行**。

## Methods

- **数字抽牌（首选，方案 B）**：洗牌用本轮开始时的 UTC Unix **毫秒时间戳**作为种子（不含客户数字），程序生成锁定的 78 张乱序牌组和 78 个正逆位。客户数字仅是牌堆的 1–78 位置。
- **咨询师代抽**：先运行同一 `prepare`，再运行 `reveal` 选位置 1 至 N（即抽洗好牌堆顶部 N 张）；标注为伪随机过程。
- **客户实体牌**：客户报告牌名和正逆位，直接记录；不执行自动洗牌。

用户已选数字抽牌时，不要再提问抽牌方法。

## Customer number choice

`prepare` 已成功、牌序和正逆位锁定后，直接邀请客户自由选择所需数量的数字。向客户的唯一数字选择提示为：

> 牌已经洗好了，请从 1–78 中自由选择 N 个互不重复的数字。

将 `N` 替换成已确定的牌数。**不提供任何示例数字、推荐号码、预填答案、候选数字组合，也不通过暗示、提问或主题联想引导客户选某些数。** 不主动展示内部洗牌方式或数字映射表。若客户已经直接给出有效数字，跳过邀请，立即使用当前锁定状态取牌。

## Executable integration — actually call the program

运行需要一个**能执行 Python 3 的工具环境**及持久保存 JSON 状态文件的工作目录。若仓库已挂载/检出，可执行下列命令；若 GitHub 文件只在连接器中可读取，应先**实际读取** `skills/draw/scripts/tarot_shuffle.py`，把原文放入可执行工具的文件系统，再执行；GitHub 读取操作本身不是代码执行。

**首次选择数字之前必须执行**：

```bash
python skills/draw/scripts/tarot_shuffle.py prepare --state .tarot-state/round-1.json
```

程序自动从执行环境当前时钟读取 Unix 毫秒时间戳，执行 SHA-256 计数流 + 无偏拒绝采样 + Fisher–Yates 洗牌，单独计算 78 个正逆位（正逆位各 50%），保存 `version`、`timestamp_ms`、`deck_ids`、`orientation_by_position`、`used_positions` 和 `commitment`。无第三方依赖。得到 `status=ready` 才算成功；**先保存状态，再请客户报数**。不要把内部状态、算法、编号与完整牌序主动展示给客户。

提示客户时只使用上方 **Customer number choice** 的中性文案，不添加任何数字示例、情绪铺垫或选号建议。

客户给出数字后，**必须使用已经存在的同一个状态文件**调用 `reveal`：将客户提供的全部位置整数按其原始顺序传入 `--numbers`，并用 `--count` 指定已固定的牌数。内部命令参数直接采用客户的实际输入，不自行生成或建议数字；不向客户展示命令。

**跨消息续抽核验：** 收到客户数字时，先从本轮 `state_file` 或此前 `prepare` 的实际执行记录定位原状态文件，运行 `verify` 核对其有效且所选位置未使用，再用**同一文件**执行 `reveal`。不得仅凭会话回忆推断 `prepare` 未执行，也不得未经核验就重新洗牌或要求客户改号。只有实际确认原文件缺失、不可读取或校验失败，才说明原因并与客户重新确定抽牌方式；新牌序不能冒充先前锁定的结果。

依照返回的 `cards` 数组顺序，把 `card` 与 `orientation` 分配到此前锁定的 N 个牌位，直接显示牌名和正逆位。客户在 `reveal` 前改选数字时，沿用原牌序并按最终确认的数字取牌；`reveal` 后牌面已锁定，不得替换已抽的牌，新需求按补牌或新轮次处理。错误数字使程序失败且不改变状态。不要用 `references/deck.md` 原始牌名顺序手工映射。

**补牌**：用同一轮状态文件调用 `reveal`、`--count` 为新增牌位数；程序会拒绝用过的位置。**新一轮独立问题**：改用全新状态文件（例如 `round-2.json`）并重新执行 `prepare`；不可覆写旧文件。

抽牌结束后如需审计，可执行：

```bash
python skills/draw/scripts/tarot_shuffle.py verify --state .tarot-state/round-1.json
```

仅在客户抽完牌后主动要求时，提供现存状态或复现参数。`commitment` 是牌序及方向的摘要，不能单凭该摘要证明运行时间或避免咨询师刻意挑时间戳；时间戳是**确定性伪随机种子**，不是保密或不可预测的高熵种子。

## Execution boundary

- **无需客户重复提供时间戳**，由 `prepare` 在抽牌前记录，除固定数据的测试/复现外不得使用 `--timestamp-ms` 覆盖当前时间。
- 客户报数前如果无法实际执行程序、无法读写跨轮状态文件、`prepare` 失败或状态丢失，就不能声称牌已洗好。请客户改用实体牌，或明确说明当前只能进行没有可核验保证的模拟抽牌；**不得在收到数字后新建状态再倒称先洗牌**。
- 不展示数字与牌面对应表，不需要向客户讲种子或散列计算；客户询问抽牌原理时可简短解释“牌序先由时间戳确定，数字只是洗牌后的位置”。
- `reveal` 运行成功后验证客户数字个数等于牌阵牌位数（补牌则等于新增牌位数），检查牌名与正逆位，设置 `draw.locked=true`，历史结果不许重写。

## Exit / Next

牌面、牌位、正逆位和抽牌来源已锁定。**REQUIRED NEXT SKILL:** 读取 `skills/interpret/SKILL.md`。
