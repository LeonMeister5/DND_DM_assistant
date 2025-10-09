// 简易DOM选择器
const $ = (s) => document.querySelector(s);

// 每格像素大小
const CELL_SIZE = 40;

// 点击按钮时请求后端生成房间
$("#btn-generate").onclick = async () => {
  const theme = $("#theme").value;
  const width = parseInt($("#width").value);
  const height = parseInt($("#height").value);

  if (!width || !height || width < 3 || height < 3) {
    alert("宽和高必须是3以上的整数。");
    return;
  }

  $("#json").textContent = "生成中...";

  try {
    const res = await fetch("/api/llm_enrich", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ monster: [theme, width, height] })
    });
    const data = await res.json();
    const text = data.description || "{}";
    const room = JSON.parse(text);
    $("#json").textContent = JSON.stringify(room, null, 2);
    drawRoom(room);
  } catch (err) {
    $("#json").textContent = "生成失败: " + err;
  }
};

// 绘制房间在canvas上
function drawRoom(room) {
  const canvas = $("#map");
  const ctx = canvas.getContext("2d");
  const w = room.meta.room_width;
  const h = room.meta.room_height;
  const objs = room.objects || [];

  canvas.width = w * CELL_SIZE;
  canvas.height = h * CELL_SIZE;
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // 画网格
  ctx.strokeStyle = "#444";
  for (let x = 0; x <= w; x++) {
    ctx.beginPath();
    ctx.moveTo(x * CELL_SIZE, 0);
    ctx.lineTo(x * CELL_SIZE, h * CELL_SIZE);
    ctx.stroke();
  }
  for (let y = 0; y <= h; y++) {
    ctx.beginPath();
    ctx.moveTo(0, y * CELL_SIZE);
    ctx.lineTo(w * CELL_SIZE, y * CELL_SIZE);
    ctx.stroke();
  }

  // 绘制物件
  for (const o of objs) {
    const { x, y } = o.pos;
    const color = getColor(o.type);
    ctx.fillStyle = color;
    ctx.fillRect(
      x * CELL_SIZE + 4,
      y * CELL_SIZE + 4,
      CELL_SIZE - 8,
      CELL_SIZE - 8
    );

    // 在格子里写首字母
    ctx.fillStyle = "#000";
    ctx.font = "bold 14px monospace";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText(o.type[0], x * CELL_SIZE + CELL_SIZE / 2, y * CELL_SIZE + CELL_SIZE / 2);
  }
}

// 颜色规则
function getColor(type) {
  switch (type) {
    case "MONSTER_SLOT": return "#f55";
    case "陷阱": return "#ff0";
    case "战利品": return "#0f0";
    case "装饰": return "#09f";
    default: return "#ccc";
  }
}
