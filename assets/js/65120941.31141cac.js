"use strict";(self.webpackChunkdocs=self.webpackChunkdocs||[]).push([[57],{8074:(e,n,t)=>{t.r(n),t.d(n,{assets:()=>l,contentTitle:()=>a,default:()=>h,frontMatter:()=>r,metadata:()=>i,toc:()=>c});const i=JSON.parse('{"id":"Moderation/Features/Inactivity","title":"Inactivity Timeout","description":"The Inactivity Timeout feature ensures that Dollar will automatically leave a voice channel if it detects that no music is being played for a period of time. This is managed through Lavalink and its configuration settings.","source":"@site/docs/4-Moderation/2-Features/Inactivity.md","sourceDirName":"4-Moderation/2-Features","slug":"/Moderation/Features/Inactivity","permalink":"/dollar-discord-bot/docs/Moderation/Features/Inactivity","draft":false,"unlisted":false,"tags":[],"version":"current","frontMatter":{},"sidebar":"tutorialSidebar","previous":{"title":"Auto Channel Creation","permalink":"/dollar-discord-bot/docs/Moderation/Features/AutoChannelCreation"},"next":{"title":"Message Moderation","permalink":"/dollar-discord-bot/docs/Moderation/Features/Messages"}}');var s=t(4848),o=t(8453);const r={},a="Inactivity Timeout",l={},c=[{value:"Purpose",id:"purpose",level:2},{value:"How It Works",id:"how-it-works",level:2},{value:"Configuration",id:"configuration",level:3},{value:"Important Notes",id:"important-notes",level:3}];function d(e){const n={code:"code",h1:"h1",h2:"h2",h3:"h3",header:"header",li:"li",p:"p",pre:"pre",strong:"strong",ul:"ul",...(0,o.R)(),...e.components};return(0,s.jsxs)(s.Fragment,{children:[(0,s.jsx)(n.header,{children:(0,s.jsx)(n.h1,{id:"inactivity-timeout",children:"Inactivity Timeout"})}),"\n",(0,s.jsxs)(n.p,{children:["The ",(0,s.jsx)(n.strong,{children:"Inactivity Timeout"})," feature ensures that ",(0,s.jsx)(n.strong,{children:"Dollar"})," will automatically leave a voice channel if it detects that no music is being played for a period of time. This is managed through ",(0,s.jsx)(n.strong,{children:"Lavalink"})," and its configuration settings."]}),"\n",(0,s.jsx)(n.h2,{id:"purpose",children:"Purpose"}),"\n",(0,s.jsxs)(n.ul,{children:["\n",(0,s.jsxs)(n.li,{children:["The ",(0,s.jsx)(n.strong,{children:"Inactivity Timeout"})," feature prevents ",(0,s.jsx)(n.strong,{children:"Dollar"})," from staying in voice channels unnecessarily when there is no active music playing."]}),"\n",(0,s.jsx)(n.li,{children:"It helps manage resources and ensures that the bot does not remain connected to voice channels when no users are interacting with it."}),"\n",(0,s.jsx)(n.li,{children:"This is especially useful in large servers where voice channels may be frequently used for various activities, and you don\u2019t want idle bots taking up space."}),"\n"]}),"\n",(0,s.jsx)(n.h2,{id:"how-it-works",children:"How It Works"}),"\n",(0,s.jsxs)(n.ul,{children:["\n",(0,s.jsxs)(n.li,{children:[(0,s.jsx)(n.strong,{children:"Dollar"})," connects to the Lavalink server with a specified ",(0,s.jsx)(n.strong,{children:"inactive_player_timeout"})," parameter, which determines how long the bot will wait before leaving a voice channel due to inactivity."]}),"\n",(0,s.jsxs)(n.li,{children:["The ",(0,s.jsx)(n.code,{children:"inactive_player_timeout"})," is set to ",(0,s.jsx)(n.strong,{children:"600 seconds"})," (10 minutes), meaning that if no music has been played for 10 minutes, ",(0,s.jsx)(n.strong,{children:"Dollar"})," will automatically leave the voice channel."]}),"\n",(0,s.jsx)(n.li,{children:"This is configured in the Lavalink node setup where the bot is instructed to disconnect after 10 minutes of inactivity."}),"\n"]}),"\n",(0,s.jsx)(n.h3,{id:"configuration",children:"Configuration"}),"\n",(0,s.jsxs)(n.ul,{children:["\n",(0,s.jsx)(n.li,{children:"The Lavalink connection is set up as follows:"}),"\n"]}),"\n",(0,s.jsx)(n.pre,{children:(0,s.jsx)(n.code,{className:"language-python",children:'nodes = [lib.wavelink.Node(uri="http://lavalink:2333", password=LAVALINK_TOKEN, identifier="MAIN", \n\t\t\t\t\t\t\tretries=None, heartbeat=60, inactive_player_timeout=600)]\n'})}),"\n",(0,s.jsxs)(n.ul,{children:["\n",(0,s.jsxs)(n.li,{children:["The ",(0,s.jsx)(n.code,{children:"inactive_player_timeout"})," parameter is set to ",(0,s.jsx)(n.strong,{children:"600 seconds"})," (10 minutes) in the Lavalink node configuration."]}),"\n"]}),"\n",(0,s.jsx)(n.h3,{id:"important-notes",children:"Important Notes"}),"\n",(0,s.jsxs)(n.ul,{children:["\n",(0,s.jsxs)(n.li,{children:["The ",(0,s.jsx)(n.strong,{children:"Inactivity Timeout"})," feature is essential for managing resources and ensuring that ",(0,s.jsx)(n.strong,{children:"Dollar"})," does not remain connected to voice channels when not in use."]}),"\n",(0,s.jsx)(n.li,{children:"This feature helps maintain a clean and efficient server environment by automatically disconnecting the bot after a period of inactivity."}),"\n"]})]})}function h(e={}){const{wrapper:n}={...(0,o.R)(),...e.components};return n?(0,s.jsx)(n,{...e,children:(0,s.jsx)(d,{...e})}):d(e)}},8453:(e,n,t)=>{t.d(n,{R:()=>r,x:()=>a});var i=t(6540);const s={},o=i.createContext(s);function r(e){const n=i.useContext(o);return i.useMemo((function(){return"function"==typeof e?e(n):{...n,...e}}),[n,e])}function a(e){let n;return n=e.disableParentContext?"function"==typeof e.components?e.components(s):e.components||s:r(e.components),i.createElement(o.Provider,{value:n},e.children)}}}]);