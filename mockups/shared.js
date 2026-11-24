document.addEventListener('DOMContentLoaded',()=>{
  const links={'Project':'project_setup.html','Results':'optimization_results.html','Run':'run_analysis.html'};
  document.querySelectorAll('[data-nav]').forEach((el,i)=>{
    const ico=el.querySelector('.ico');if(ico)ico.style.setProperty('--icon-index',i);
    const label=el.textContent.replace(ico?.textContent||'', '').trim();
    if(links[label]) el.href=links[label];else{el.setAttribute('aria-disabled','true');el.title='Not included in this visual prototype';}
  });
  document.querySelectorAll('tr[data-selectable]').forEach(row=>{
    row.tabIndex=0;const select=()=>{row.closest('table').querySelectorAll('tr').forEach(r=>r.classList.remove('active-row'));row.classList.add('active-row');};
    row.addEventListener('click',select);row.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();select();}});
  });
  const run=document.querySelector('.footer .primary');if(run&&run.textContent.includes('Run Analysis'))run.addEventListener('click',()=>location.href='run_analysis.html');
});
