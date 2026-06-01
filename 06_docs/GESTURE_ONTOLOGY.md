# Gesture Ontology v1.1

赛博古琴不把古琴谱字简单存成一个 gesture_id 字符串。

本项目采用四层结构：

1. score_events：曲中事件；
2. gesture_templates：指法模板总览；
3. gesture_components：动作组件序列；
4. sample_assets：三曼实际采样实现。

sound_type 固定为散音、按音、泛音。
复杂技法通过 sound_profile、gesture_family 和 gesture_components 表达。

绰、默认吟猱等琴人习惯性实现不默认写进 gesture_id。
注、猱若谱面明示，则写入 notation_pre_action / notation_vibrato。
上、下、进复、退复、撞、反撞等谱面动作进入 post_motion component。
撞、反撞为 micro_returning_slide，不使用 percussive。
进复、退复是不可拆原子。
bo=擘，po=泼，la=剌。
泼、剌、滚、拂为可独立右手序列动作；泼剌、滚拂是组合名。
掐起、罨、带起是 left_hand_sound。
放合、应合属于 open_pressed_harmony。
分开不属于 open_pressed_harmony，也不单独创建 gesture_family；它属于 compound_both_hands，sound_profile=compound_pressed_motion，由三个组件构成：抹、上、注挑回原音位。
注挑回原音位已经包含回归本音方向，不另列下。
