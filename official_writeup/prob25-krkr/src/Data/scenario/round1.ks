@eval exp="f.text = 'flag{'"
@eval exp="f.hash = 1337"

*round_1|�����һ��

���������һ�顣[p]

*sel_loop|��һ������

@jump storage="round2.ks" cond="f.text.charAt(f.text.length-1)=='}'"

��ǰ�ı���[emb exp="f.text"][r]

[link target=*sel_a clickse="SE_306"]> ���� A[endlink][r]
[link target=*sel_e clickse="SE_306"]> ���� E[endlink][r]
[link target=*sel_i clickse="SE_306"]> ���� I[endlink][r]
[link target=*sel_o clickse="SE_306"]> ���� O[endlink][r]
[link target=*sel_u clickse="SE_306"]> ���� U[endlink][r]
[link target=*sel_fin clickse="SE_306"]> ���� }[endlink][r]
[s]

*sel_a
@eval exp="f.text = f.text + 'A'"
@eval exp="f.hash = f.hash * 13337 + 11"
@jump target=*sel_end

*sel_e
@eval exp="f.text = f.text + 'E'"
@eval exp="f.hash = f.hash * 13337 + 22"
@jump target=*sel_end

*sel_i
@eval exp="f.text = f.text + 'I'"
@eval exp="f.hash = f.hash * 13337 + 33"
@jump target=*sel_end

*sel_o
@eval exp="f.text = f.text + 'O'"
@eval exp="f.hash = f.hash * 13337 + 44"
@jump target=*sel_end

*sel_u
@eval exp="f.text = f.text + 'U'"
@eval exp="f.hash = f.hash * 13337 + 55"
@jump target=*sel_end

*sel_fin
@eval exp="f.text = f.text + '}'"
@eval exp="f.hash = f.hash * 13337 + 66"
@jump target=*sel_end

*sel_end
@eval exp="f.hash = f.hash % 19260817"

������ɣ�[p]
@jump target=*sel_loop