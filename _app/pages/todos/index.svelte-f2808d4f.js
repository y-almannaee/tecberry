import{S as ue,i as re,s as de,e as v,k as U,c as m,a as O,m as N,d as T,b as a,R as ae,g as $,G as u,as as G,at as le,au as ce,av as _e,aw as fe,Q as he,ag as ne,T as pe,t as ve,O as me,h as be,ao as ge,p as Te,q as ye,o as Ee,ax as ke,ay as oe,n as Ue,az as Ne,L as we}from"../../chunks/vendor-ce2e2ef8.js";import{c as B}from"../../chunks/singletons-d1fb5791.js";B.disable_scroll_handling;B.goto;const Ie=B.invalidate;B.prefetch;B.prefetch_routes;B.before_navigate;B.after_navigate;function Q(r,{pending:t,error:e,result:o}={}){let p;async function y(c){const d=p={};c.preventDefault();const h=new FormData(r);t&&t({data:h,form:r});try{const l=await fetch(r.action,{method:r.method,headers:{accept:"application/json"},body:h});if(d!==p)return;if(l.ok){o&&o({data:h,form:r,response:l});const b=new URL(r.action);b.search=b.hash="",Ie(b.href)}else e?e({data:h,form:r,error:null,response:l}):console.error(await l.text())}catch(l){if(e)e({data:h,form:r,error:l,response:null});else throw l}}return r.addEventListener("submit",y),{destroy(){r.removeEventListener("submit",y)}}}function se(r,t,e){const o=r.slice();return o[3]=t[e],o[4]=t,o[5]=e,o}function ie(r,t){let e,o,p,y,c,d,h,l,b,P,M,C,f,E,s,i,n,R,q,w,J,I,D,S,K,F,V,j,W,L,X,Y=we,k,Z,x;function ee(...g){return t[1](t[3],t[4],t[5],...g)}function te(){return t[2](t[3],t[4],t[5])}return{key:r,first:null,c(){e=v("div"),o=v("form"),p=v("input"),c=U(),d=v("input"),l=U(),b=v("button"),C=U(),f=v("form"),E=v("input"),i=U(),n=v("input"),q=U(),w=v("button"),J=U(),I=v("form"),D=v("input"),K=U(),F=v("button"),W=U(),this.h()},l(g){e=m(g,"DIV",{class:!0});var _=O(e);o=m(_,"FORM",{action:!0,method:!0});var A=O(o);p=m(A,"INPUT",{type:!0,name:!0,class:!0}),c=N(A),d=m(A,"INPUT",{type:!0,name:!0,class:!0}),l=N(A),b=m(A,"BUTTON",{class:!0,"aria-label":!0}),O(b).forEach(T),A.forEach(T),C=N(_),f=m(_,"FORM",{class:!0,action:!0,method:!0});var H=O(f);E=m(H,"INPUT",{type:!0,name:!0,class:!0}),i=N(H),n=m(H,"INPUT",{"aria-label":!0,type:!0,name:!0,class:!0}),q=N(H),w=m(H,"BUTTON",{class:!0,"aria-label":!0}),O(w).forEach(T),H.forEach(T),J=N(_),I=m(_,"FORM",{action:!0,method:!0});var z=O(I);D=m(z,"INPUT",{type:!0,name:!0,class:!0}),K=N(z),F=m(z,"BUTTON",{class:!0,"aria-label":!0}),O(F).forEach(T),z.forEach(T),W=N(_),_.forEach(T),this.h()},h(){a(p,"type","hidden"),a(p,"name","uid"),p.value=y=t[3].uid,a(p,"class","svelte-16nsat"),a(d,"type","hidden"),a(d,"name","done"),d.value=h=t[3].done?"":"true",a(d,"class","svelte-16nsat"),a(b,"class","toggle svelte-16nsat"),a(b,"aria-label",P="Mark todo as "+(t[3].done?"not done":"done")),a(o,"action","/todos?_method=PATCH"),a(o,"method","post"),a(E,"type","hidden"),a(E,"name","uid"),E.value=s=t[3].uid,a(E,"class","svelte-16nsat"),a(n,"aria-label","Edit todo"),a(n,"type","text"),a(n,"name","text"),n.value=R=t[3].text,a(n,"class","svelte-16nsat"),a(w,"class","save svelte-16nsat"),a(w,"aria-label","Save todo"),a(f,"class","text svelte-16nsat"),a(f,"action","/todos?_method=PATCH"),a(f,"method","post"),a(D,"type","hidden"),a(D,"name","uid"),D.value=S=t[3].uid,a(D,"class","svelte-16nsat"),a(F,"class","delete svelte-16nsat"),a(F,"aria-label","Delete todo"),F.disabled=V=t[3].pending_delete,a(I,"action","/todos?_method=DELETE"),a(I,"method","post"),a(e,"class","todo svelte-16nsat"),ae(e,"done",t[3].done),this.first=e},m(g,_){$(g,e,_),u(e,o),u(o,p),u(o,c),u(o,d),u(o,l),u(o,b),u(e,C),u(e,f),u(f,E),u(f,i),u(f,n),u(f,q),u(f,w),u(e,J),u(e,I),u(I,D),u(I,K),u(I,F),u(e,W),k=!0,Z||(x=[G(M=Q.call(null,o,{pending:ee})),G(Q.call(null,f)),G(j=Q.call(null,I,{pending:te}))],Z=!0)},p(g,_){t=g,(!k||_&1&&y!==(y=t[3].uid))&&(p.value=y),(!k||_&1&&h!==(h=t[3].done?"":"true"))&&(d.value=h),(!k||_&1&&P!==(P="Mark todo as "+(t[3].done?"not done":"done")))&&a(b,"aria-label",P),M&&le(M.update)&&_&1&&M.update.call(null,{pending:ee}),(!k||_&1&&s!==(s=t[3].uid))&&(E.value=s),(!k||_&1&&R!==(R=t[3].text)&&n.value!==R)&&(n.value=R),(!k||_&1&&S!==(S=t[3].uid))&&(D.value=S),(!k||_&1&&V!==(V=t[3].pending_delete))&&(F.disabled=V),j&&le(j.update)&&_&1&&j.update.call(null,{pending:te}),_&1&&ae(e,"done",t[3].done)},r(){X=e.getBoundingClientRect()},f(){ce(e),Y(),_e(e,X)},a(){Y(),Y=fe(e,X,ke,{duration:200})},i(g){k||(g&&he(()=>{L||(L=ne(e,oe,{start:.7},!0)),L.run(1)}),k=!0)},o(g){g&&(L||(L=ne(e,oe,{start:.7},!1)),L.run(0)),k=!1},d(g){g&&T(e),g&&L&&L.end(),Z=!1,pe(x)}}}function Oe(r){let t,e,o,p,y,c,d,h,l=[],b=new Map,P,M,C,f=r[0];const E=s=>s[3].uid;for(let s=0;s<f.length;s+=1){let i=se(r,f,s),n=E(i);b.set(n,l[s]=ie(n,i))}return{c(){t=U(),e=v("div"),o=v("h1"),p=ve("Todos"),y=U(),c=v("form"),d=v("input"),h=U();for(let s=0;s<l.length;s+=1)l[s].c();this.h()},l(s){me('[data-svelte="svelte-181o7gf"]',document.head).forEach(T),t=N(s),e=m(s,"DIV",{class:!0});var n=O(e);o=m(n,"H1",{});var R=O(o);p=be(R,"Todos"),R.forEach(T),y=N(n),c=m(n,"FORM",{class:!0,action:!0,method:!0});var q=O(c);d=m(q,"INPUT",{name:!0,"aria-label":!0,placeholder:!0,class:!0}),q.forEach(T),h=N(n);for(let w=0;w<l.length;w+=1)l[w].l(n);n.forEach(T),this.h()},h(){document.title="Todos",a(d,"name","text"),a(d,"aria-label","Add todo"),a(d,"placeholder","+ tap to add a todo"),a(d,"class","svelte-16nsat"),a(c,"class","new svelte-16nsat"),a(c,"action","/todos"),a(c,"method","post"),a(e,"class","todos svelte-16nsat")},m(s,i){$(s,t,i),$(s,e,i),u(e,o),u(o,p),u(e,y),u(e,c),u(c,d),u(e,h);for(let n=0;n<l.length;n+=1)l[n].m(e,null);P=!0,M||(C=G(Q.call(null,c,{result:Pe})),M=!0)},p(s,[i]){if(i&1){f=s[0],Ue();for(let n=0;n<l.length;n+=1)l[n].r();l=ge(l,i,E,1,s,f,b,e,Ne,ie,null,se);for(let n=0;n<l.length;n+=1)l[n].a();Te()}},i(s){if(!P){for(let i=0;i<f.length;i+=1)ye(l[i]);P=!0}},o(s){for(let i=0;i<l.length;i+=1)Ee(l[i]);P=!1},d(s){s&&T(t),s&&T(e);for(let i=0;i<l.length;i+=1)l[i].d();M=!1,C()}}}const Pe=async({form:r})=>{r.reset()};function Me(r,t,e){let{todos:o}=t;const p=(c,d,h,{data:l})=>{e(0,d[h].done=!!l.get("done"),o)},y=(c,d,h)=>e(0,d[h].pending_delete=!0,o);return r.$$set=c=>{"todos"in c&&e(0,o=c.todos)},[o,p,y]}class Fe extends ue{constructor(t){super();re(this,t,Me,Oe,de,{todos:0})}}export{Fe as default};