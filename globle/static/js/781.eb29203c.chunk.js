"use strict";(self.webpackChunkgloble=self.webpackChunkgloble||[]).push([[781],{9781:function(e,a,r){r.r(a),r.d(a,{default:function(){return C}});var t=r(2982),i=r(885),n=r(2791),l=r(6215),o=r(173),s=r(2606),c=r(8278),u=r(5906),d=r(8336),p=r(3925),v=r(762),m=r(4008),f=r(7832),b=r(6441),h=r(6027),g=(d.R,p.R,v.f,u.$,m.g,b.E,f.W,h.v,{"es-MX":"NAME_ES","en-CA":"NAME_EN","fr-FR":"NAME_FR","de-DE":"NAME_DE","hu-HU":"NAME_HU","pt-BR":"NAME_PT","pl-PL":"NAME_PL","it-IT":"NAME_IT","sv-SE":"NAME_SV"}),x=r(184);function N(e){var a=e.win,r=e.error,t=e.guesses,u=e.practiceMode,d=(0,n.useContext)(c.R).locale,p=l.U;if("en-CA"!==d){var v=g[d];p=l.v.properties[v]}if(u){var m=JSON.parse(localStorage.getItem("practice"));if(p=m.properties.NAME,"en-CA"!==d){var f=g[d];p=m.properties[f]}}return r?(0,x.jsx)("p",{className:"text-red-700 ",children:r}):a?(0,x.jsx)("p",{className:"text-green-800 dark:text-green-300 font-bold ",children:(0,x.jsx)(s.Z,{id:"Game7",values:{answer:p}})}):0===t?(0,x.jsx)("p",{className:"text-gray-700 dark:text-gray-400 ",children:(0,x.jsx)(s.Z,{id:"Game3"})}):1===t?(0,x.jsx)("p",{className:"text-gray-700 dark:text-gray-400 ",children:(0,x.jsx)(s.Z,{id:"Game4",values:{span:function(e){try{var a=JSON.parse(e),r=(0,i.Z)(a,2),t=r[0],n=r[1];return o.tq?(0,x.jsx)("span",{children:n}):(0,x.jsx)("span",{children:t})}catch(l){return(0,x.jsx)("span",{children:e})}}}})}):(0,x.jsx)("p",{className:"text-red-700 "})}var w=r(6013),y=r(7587),E=r(2320),A=r(9199).R,M=r(6746);function C(e){var a=e.guesses,r=e.setGuesses,o=e.win,u=e.setWin,d=e.practiceMode,p=(0,n.useState)(""),v=(0,i.Z)(p,2),m=v[0],f=v[1],b=(0,n.useState)(""),h=(0,i.Z)(b,2),C=h[0],j=h[1],k=(0,n.useContext)(y.N).theme.hideAutocomplete,L=(0,n.useContext)(c.R).locale,S=g[L],R=(0,n.useRef)(null);function z(e,a){return a.find((function(a){var r=a.properties,t=r.NAME,i=r.NAME_LONG,n=r.ABBREV,l=r.ADMIN,o=r.BRK_NAME,s=r.NAME_SORT;return t.toLowerCase()===e||i.toLowerCase()===e||l.toLowerCase()===e||n.toLowerCase()===e||n.replace(/\./g,"").toLowerCase()===e||t.replace(/-/g," ").toLowerCase()===e||o.toLowerCase()===e||s.toLowerCase()===e||a.properties[S].toLowerCase()===e}))}return(0,n.useEffect)((function(){var e;null===(e=R.current)||void 0===e||e.focus()}),[R]),(0,x.jsxs)("div",{className:"mt-10 mb-6 block mx-auto text-center",children:[(0,x.jsxs)("form",{onSubmit:function(e){e.preventDefault(),j("");var i=function(){var e,r=m.trim().toLowerCase().replace(/&/g,"and").replace(/^st\s/g,"st. "),t=M[L].find((function(e){return e.alternative===r})),i=t?t.real:r;if(z(i,a))return j(E.Z[L].Game6),void(null===(e=R.current)||void 0===e||e.select());var n,o=z(i,A);if(!o)return j(E.Z[L].Game5),void(null===(n=R.current)||void 0===n||n.select());if(d){var s=JSON.parse(localStorage.getItem("practice")).properties.NAME;o.properties.NAME===s&&u(!0)}else o.properties.NAME===l.U&&u(!0);return o}();if(d){var n=JSON.parse(localStorage.getItem("practice"));if(i&&n)return i.proximity=(0,w.z)(i,n),r([].concat((0,t.Z)(a),[i])),void f("")}i&&l.v&&(i.proximity=(0,w.z)(i,l.v),r([].concat((0,t.Z)(a),[i])),f(""))},className:"w-80 flex space-x-4 mx-auto my-2 justify-center flex-wrap",children:[(0,x.jsx)("input",{className:"shadow px-2 py-1 md:py-0\r text-gray-700 dark:bg-slate-200 dark:text-gray-900\r focus:outline-none\r focus:shadow-outline disabled:bg-slate-400\r border rounded disabled:border-slate-400\r w-full flex-1",type:"text",name:"guesser",id:"guesser",value:m,onChange:function(e){return f(e.currentTarget.value)},ref:R,disabled:o,placeholder:0===a.length?E.Z[L].Game1:"",autoComplete:"new-password"}),(0,x.jsx)("button",{className:"bg-blue-700 dark:bg-purple-800 hover:bg-blue-900\r dark:hover:bg-purple-900 disabled:bg-blue-900  text-white\r font-bold py-1 md:py-2 px-4 rounded focus:shadow-outline ",type:"submit",disabled:o,children:(0,x.jsx)(s.Z,{id:"Game2"})}),(0,x.jsx)("div",{className:"shadow px-2 py-0\r text-gray-700 dark:bg-slate-300 focus:outline-none\r focus:shadow-outline disabled:bg-slate-400\r rounded disabled:border-slate-400\r w-full bg-white !mx-0",children:function(e){if(k)return[];var a=e.trim(),r=a.length;if(r>=2){var t=A.map((function(e){return e.properties.NAME})),i=A.filter((function(e){return e.properties.NAME.toLowerCase().slice(0,r)===a.toLowerCase()}));return 1===i.length&&t.includes(a)?[]:i.slice(0,3)}return[]}(m).map((function(e){return(0,x.jsx)("div",{className:"text-left",onClick:function(){return f(e.properties.NAME)},children:e.properties.NAME},e.properties.ADMIN)}))})]}),(0,x.jsx)(N,{win:o,error:C,guesses:a.length,practiceMode:d})]})}},6746:function(e){e.exports=JSON.parse('{"en-CA":[{"real":"eswatini","alternative":"swaziland"},{"real":"myanmar","alternative":"burma"},{"real":"north macedonia","alternative":"macedonia"},{"real":"congo","alternative":"congo-brazzaville"},{"real":"vatican","alternative":"holy see"},{"real":"vatican","alternative":"vatican city"},{"real":"cabo verde","alternative":"cape verde"},{"real":"democratic republic of the congo","alternative":"democratic republic of congo"},{"real":"democratic republic of the congo","alternative":"dr congo"},{"real":"bosnia and herzegovina","alternative":"bosnia"},{"real":"ivory coast","alternative":"cote d\'ivoire"},{"real":"ivory coast","alternative":"c\xf4te d\'ivoire"},{"real":"ivory coast","alternative":"cote divoire"},{"real":"turkey","alternative":"turkiye"}],"fr-FR":[{"real":"eswatini","alternative":"swaziland"},{"real":"myanmar","alternative":"byrmanie"},{"real":"united arab emirates","alternative":"eau"},{"real":"united arab emirates","alternative":"\xe9mirats"},{"real":"czechia","alternative":"r\xe9publique tch\xe8que"}],"es-MX":[{"real":"netherlands","alternative":"holanda"}],"de-DE":[],"hu-HU":[],"pt-BR":[{"real":"czechia","alternative":"rep\xfablica tcheca"},{"real":"czechia","alternative":"tch\xe9quia"},{"real":"democratic republic of the congo","alternative":"rd congo"},{"real":"democratic republic of the congo","alternative":"rdc"},{"real":"eswatini","alternative":"suazil\xe2ndia"},{"real":"djibouti","alternative":"djibuti"},{"real":"malawi","alternative":"malaui"},{"real":"mauritius","alternative":"maur\xedcio"},{"real":"papua new guinea","alternative":"papua nova guin\xe9"},{"real":"turkmenistan","alternative":"turcomenist\xe3o"},{"real":"vietnam","alternative":"vietn\xe3"},{"real":"bahrain","alternative":"barein"},{"real":"bahrain","alternative":"bareine"},{"real":"bahrain","alternative":"bar\xe9m"},{"real":"united arab emirates","alternative":"emirados \xe1rabes"},{"real":"ireland","alternative":"irlanda"},{"real":"seychelles","alternative":"seicheles"}],"it-IT":[],"pl-PL":[{"real":"georgia","alternative":"abchazja"},{"real":"china","alternative":"chiny"}],"sv-SE":[]}')}}]);
//# sourceMappingURL=781.eb29203c.chunk.js.map