import json,sys,os
for s in ["base","rp105","rp110gen"]:
    if not os.path.exists(s+".json"): continue
    R=json.load(open(s+".json")); n=len(R)
    calls=[x[k] for x in R for k in ("ner","triples")]
    hit=sum(c["hit_max"] for c in calls); fail=sum(not c["parse_ok"] for c in calls)
    loop=sum(x["triples"]["max_run_same_subj_pred"]>=4 for x in R)
    ok_n=[x["triples"]["n"] for x in R if x["triples"]["parse_ok"] and x["triples"]["max_run_same_subj_pred"]<4]
    tok=sum(c["completion_tokens"] for c in calls); sec=sum(c["sec"] for c in calls)
    print(f"{s:9s} samples={n} calls={len(calls)} parse_fail={fail} hit_max={hit} triple_loop(run>=4)={loop} clean_triple_samples={len(ok_n)} clean_n={ok_n} tokens={tok} sec={sec:.0f}")
    for x in R:
        t=x["triples"];e=x["ner"]
        print(f"   {x['video'][:6]} c{x['chunk']} s{x['sample']} NER {e['completion_tokens']:4d}t ok={int(e['parse_ok'])} | TRI {t['completion_tokens']:4d}t ok={int(t['parse_ok'])} max={int(t['hit_max'])} n={t['n']:3d} run={t['max_run_same_subj_pred']}")
