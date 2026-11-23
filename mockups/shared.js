document.addEventListener('DOMContentLoaded',()=>{
  document.querySelectorAll('[data-nav]').forEach(el=>el.addEventListener('click',e=>{e.preventDefault();}));
  document.querySelectorAll('tr[data-selectable]').forEach(row=>row.addEventListener('click',()=>{
    row.closest('table').querySelectorAll('tr').forEach(r=>r.classList.remove('active-row'));
    row.classList.add('active-row');
  }));
});
