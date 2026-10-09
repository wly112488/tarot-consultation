---
name: tarot-interpret
description: Use when cards and positions are locked and the client needs an initial tarot interpretation grounded in traditional card meanings.
---

# INTERPRET — Independent initial reading

**Prerequisite:** `draw.locked=true`，客户问题、各牌位含义与牌面完整。

## Do

依次解释：(1) 每张牌在该牌位的传统核心意义以及正逆位差异；(2) 牌之间相互支持、冲突、反复出现的主题；(3) 结合客户原始问题作整体判断及其边界。不要机械给每张牌堆砌多个同义词；客户若要求逐张翻牌，可以逐张解释但最后仍要整合。

**在开始询问客户是否符合现实之前**，形成和表达可以被回顾的初步解读，保存为 `original_interpretation`；把确定的牌义与不确定的现实推断分开。整体判断需标明其关键牌位与牌间关系，保留无法确定或互相矛盾的部分，供后续反馈核对。不得先套出事实再宣称“牌已经预测到了”；不给第三人真实内心、疾病、录取、财务回报或未来事件作确证。

**逐张展示的时点规则：** 在展示第一张牌前，先依据本轮全部已锁定牌面形成并保留整轮 `original_interpretation`，再按客户要求逐张呈现。客户中途反馈只用于单独记录和修订，不改变尚未展示牌面的原始判断，也不把修订描述成此前已经作出的判断。

## Exit

客户已看到初解（完整或按其要求逐张），独立判断已保存，接下来可听取反馈或追问。不强制逐张询问“对吗”。

## Next

客户回应初解、提出现实信息或否认：**REQUIRED NEXT SKILL** `skills/feedback/SKILL.md`。客户仅要求更多牌义或新问题：`skills/follow-up/SKILL.md`。客户结束：`skills/closing/SKILL.md`。
