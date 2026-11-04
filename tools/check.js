const fs=require('fs'), vm=require('vm');
function load(files){ const ctx={window:{}}; vm.createContext(ctx); files.forEach(f=>vm.runInContext(fs.readFileSync(f,'utf8'),ctx)); return ctx.window; }
const R='/home/claude/sueo-study/', S=process.argv[2];
const NEW=load([R+'vocab.js',R+'signs.js',R+'signs-extra.js',R+'signs-nuri.js',R+'dialogs.js',R+'notes.js']);
const OLD=load([S+'/vocab.orig.js',S+'/dialogs.orig.js']);
const lv=W=>{const m={}; W.LEVELS.concat([{k:'m1'},{k:'m2'}]); W.TOPICS.forEach(t=>Object.entries(t.w).forEach(([k,a])=>a.forEach(w=>{ if(m[w]) console.log('DUP',w); m[w]=k;}))); return m;};
const ln=k=>+k.slice(1);
const mN=lv(NEW), mO=lv(OLD);
console.log('words', Object.keys(mO).length,'->',Object.keys(mN).length);
for(const w in mO) if(mN[w]!==mO[w]) console.log('LEVEL CHANGE',w,mO[w],mN[w]);
const g=(W,m)=>{const o={}; for(const tk in W.DIALOGS) W.DIALOGS[tk].forEach(d=>{ let mx=0; d.lines.forEach(l=>l.g.forEach(x=>{ if(x.startsWith('(')) return; if(!m[x]) console.log('MISSING g',tk,d.title,x); else mx=Math.max(mx,ln(m[x])); })); o[tk+'|'+d.title]=mx;}); return o;};
const dN=g(NEW,mN), dO=g(OLD,mO);
for(const k in dO) if(dN[k]!==dO[k]) console.log('DIALOG MOVED',k,dO[k],dN[k]);
for(const k in dN) if(!(k in dO)) console.log('NEW DIALOG',k,dN[k]);
const SW=NEW.SIGN_WORDS; for(const w in mN) if(!SW[w]) console.log('NO SIGN',w);
NEW.NOTES.filter(n=>n.lv==='c7').forEach(n=>n.body.forEach(b=>(b.ex||[]).forEach(x=>(x.pic||x.sl).forEach(w=>{ if(!SW[w] && !w.startsWith('{')) console.log('NOTE word w/o sign',n.id,w);}))));
const cnt={}; for(const w in mN) cnt[mN[w]]=(cnt[mN[w]]||0)+1; console.log(cnt);
const dc={}; Object.values(dN).forEach(v=>dc[v]=(dc[v]||0)+1); console.log('dialogs by level',dc);
console.log('c7 nopic', Object.keys(mN).filter(w=>mN[w]==='c7' && !(SW[w][1].length) && !(NEW.NURI_PIC||{})[w]));
