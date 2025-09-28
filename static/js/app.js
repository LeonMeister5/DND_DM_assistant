const $ = (s)=>document.querySelector(s);
let currentMonster = null;

$("#btn-rand").onclick = async ()=>{
  const constraints = $("#constraints").value;
  const res = await fetch(`/api/random_monster?constraints=${encodeURIComponent(constraints)}`);
  const m = await res.json();
  currentMonster = m;
  $("#monster").textContent = JSON.stringify(m, null, 2);
  $("#btn-enrich").disabled = false;
};

$("#btn-enrich").onclick = async ()=>{
  if(!currentMonster) return;
  $("#desc").textContent = "请求中...";
  const res = await fetch("/api/llm_enrich", {
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body: JSON.stringify({ monster: currentMonster })
  });
  const data = await res.json();
  $("#desc").textContent = data.description || JSON.stringify(data);
};
