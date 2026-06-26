// XForge Manual - Shared Scripts (DR-0181 + DR-0182 + B-093)
// v50.5.0: Dropdown menus suspensos com auto-close
(function(){
  // ========== DARK MODE ==========
  var btn=document.getElementById('darkBtn');
  if(btn){
    btn.onclick=function(){
      document.body.classList.toggle('dark');
      try{localStorage.setItem('xforge-dark',document.body.classList.contains('dark')?'true':'false')}catch(e){}
    };
  }
  if(typeof localStorage!=='undefined'&&localStorage.getItem('xforge-dark')==='true'){
    document.body.classList.add('dark');
  }

  // ========== COPY BUTTON ON PRE>CODE ==========
  var pres=document.querySelectorAll('pre');
  Array.prototype.forEach.call(pres,function(p){
    var code=p.querySelector('code');
    if(!code)return;
    var b=document.createElement('button');
    b.className='copy-btn';
    b.textContent='Copiar';
    b.type='button';
    b.onclick=function(){
      var text=code.textContent;
      if(navigator.clipboard){
        navigator.clipboard.writeText(text).then(function(){
          b.textContent='OK!';
          setTimeout(function(){b.textContent='Copiar'},1200);
        }).catch(function(){
          fallbackCopy(text);b.textContent='OK!';setTimeout(function(){b.textContent='Copiar'},1200);
        });
      }else{fallbackCopy(text);b.textContent='OK!';setTimeout(function(){b.textContent='Copiar'},1200);}
    };
    p.appendChild(b);
  });
  function fallbackCopy(text){
    var ta=document.createElement('textarea');ta.value=text;document.body.appendChild(ta);ta.select();try{document.execCommand('copy')}catch(e){}document.body.removeChild(ta);
  }

  // ========== DROPDOWN MENUS SUSPENSOS (v50.6.0) ==========
  // Comportamento CORRETO:
  //   1. Click no <summary> - toggle natural (abre/fecha). Se abriu, fecha outros.
  //   2. Click em LINK dentro do menu - navega, menu fecha naturalmente (proxima pagina)
  //   3. Click em QUALQUER LUGAR FORA do nav - fecha todos
  //   4. ESC - fecha todos
  // NAO fecha ao clicar no proprio menu/submenu.
  var allDetails = document.querySelectorAll('header nav details');

  // Accordion: quando um details abre, fecha os outros do mesmo nivel
  Array.prototype.forEach.call(allDetails, function(d){
    d.addEventListener('toggle', function(){
      if (d.open) {
        // Acabou de abrir - fecha outros que estiverem abertos
        // (so fecha siblings no mesmo nav, nao children)
        var parent = d.parentElement;
        var siblings = parent ? parent.querySelectorAll(':scope > details') : [];
        Array.prototype.forEach.call(siblings, function(other){
          if (other !== d && other.hasAttribute('open')) {
            other.removeAttribute('open');
          }
        });
      }
    });
  });

  // Click FORA do nav fecha tudo (mas nao fecha ao clicar dentro do nav)
  document.addEventListener('click', function(e){
    if (e.target.closest('header nav')) return; // click dentro do nav: nao fecha
    Array.prototype.forEach.call(allDetails, function(d){
      d.removeAttribute('open');
    });
  });

  // ESC fecha todos
  document.addEventListener('keydown', function(e){
    if (e.key === 'Escape'){
      Array.prototype.forEach.call(allDetails, function(d){
        d.removeAttribute('open');
      });
    }
  });

  // ========== FORCAR FECHADO NO LOAD (v50.32.0) ==========
  // Garante que nenhum <details> inicie aberto (extensoes, cache, etc)
  Array.prototype.forEach.call(document.querySelectorAll('header nav details[open]'), function(d){
    d.removeAttribute('open');
  });
})();