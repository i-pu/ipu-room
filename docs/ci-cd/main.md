<head>
<script src="https://unpkg.com/mermaid@8.0.0/dist/mermaid.min.js"></script>
<script>
const mermaiding = function() {
    const elements = document.querySelectorAll("pre>code.language-mermaid");
    for (let i = 0; i < elements.length; i++) {
        const e = elements[i];
        const pre = e.parentElement;
        const replace = function(graph) {
            const elem = document.createElement('div');
            elem.innerHTML = graph;
            elem.className = 'mermaid';
            elem.setAttribute('data-processed', 'true');
            pre.parentElement.replaceChild(elem, pre);
        }
        mermaid.mermaidAPI.render('id' + i, e.textContent, replace);
    }
}

if (document.readyState == 'interactive' || document.readyState == 'complete') {
    mermaiding();
}else{
    document.addEventListener("DOMContentLoaded", mermaiding);
}
</script>
</head>

# Overview
簡単そうなのでgoogle cloud build を使う．以下は全体図．
```mermaid
graph LR
  GIT[github master] --> GCB[google cloud build]
  GCB -- push --> DOCKER[docker.io]
  GCB -- build --> GCB 
  GCB -- trigger --> HELM[helm]
  DOCKER -- image --> HELM
  HELM -- install --> GKE
```

## Helm 
helm 以下のディレクトリにチャートが揃っており，
互いに共通の変数がディレクトリ直下の`values.yaml`にしまわれている．
チャートごとの変数はそれぞれのチャートのディレクトリ以下にしまわれている．

チャート名やリリース名はkubeのリソース名に含まれるので，`lowercase`で
`-`か`.`を使うようにする．

### dev
### prd
