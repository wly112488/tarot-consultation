---
name: tarot-draw
description: Use when a tarot spread and its card positions are fixed and cards need to be drawn, oriented, verified, or recorded.
---

# DRAW — Draw and lock

**Prerequisite:** 牌阵及牌位在抽取前固定；读取 `references/deck.md` 核查完整 78 张名录。

## Choose method

可选：
- **TOOL_RANDOM**：有可用随机工具才使用，明确算法为 78 张无放回取 `N` 张，正逆位独立等概率（除非此前已约定）；不得虚构工具结果或宣称密码学随机。
- **SIMULATED**：由模型模拟选择，不声称是可验证的随机抽样。明确告诉客户“模拟抽牌”，并在展示结果时保持牌面锁定。
- **CLIENT_CARDS**：由客户使用实体牌或提供已确定的牌名、正逆位，按其输入解读；缺失的方向需要在抽牌前约定处理方式。客户给数字/选位置时，须**先说明公开、固定的映射规则**，不得在得知偏好后随意映射。

先说明可选方式；客户已指定且可执行时直接开始。牌阵、正逆位规则、抽取方法先定，再显示结果。模型没有外部随机工具时，只能用模拟或客户牌，不得声称随机性已验证。

## Lock & handoff

将每张牌完整记为 `(牌位, 牌名, 正/逆位)`；检查无重复、牌名属于 78 张、数量与牌阵相同；将 `draw.locked=true`。必要时简短展示牌面，**不可**因客户对牌义的反应重抽或调整。

## Exit

牌阵各位置都有固定牌，方法与方向有记录，牌面已锁定。

## Next

**REQUIRED NEXT SKILL:** 读取 `skills/interpret/SKILL.md`。
