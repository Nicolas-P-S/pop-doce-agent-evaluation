/**
 * Verifica o campo `ferramentas` devolvido pela API da Lia.
 * Vars do caso: ferramentas_obrigatorias / ferramentas_proibidas (lista separada por virgula,
 * casamento por substring no nome, ex.: "consultar_pedido" casa com
 * "pedidos-e-cupons___consultar_pedido").
 */
const lista = (s) => String(s || "").split(",").map((x) => x.trim().toLowerCase()).filter(Boolean);

module.exports = (output, context) => {
  const vars = (context && context.vars) || {};
  const obrigatorias = lista(vars.ferramentas_obrigatorias);
  const proibidas = lista(vars.ferramentas_proibidas);
  if (!obrigatorias.length && !proibidas.length) {
    return { pass: true, score: 1, reason: "Caso sem exigência de ferramenta." };
  }
  let dados;
  try { dados = JSON.parse(output); }
  catch { return { pass: false, score: 0, reason: "Saída do provider não é JSON." }; }

  const chamadas = (dados.ferramentas_por_turno || [])
    .flatMap((t) => (t.ferramentas || []).map((f) => String((f && f.ferramenta) || "").toLowerCase()))
    .filter(Boolean);
  const faltando = obrigatorias.filter((o) => !chamadas.some((c) => c.includes(o)));
  const indevidas = proibidas.filter((p) => chamadas.some((c) => c.includes(p)));
  const pass = !faltando.length && !indevidas.length;
  const partes = [];
  if (faltando.length) partes.push(`ferramenta obrigatória não chamada: ${faltando.join(", ")}`);
  if (indevidas.length) partes.push(`ferramenta proibida chamada: ${indevidas.join(", ")}`);
  return {
    pass, score: pass ? 1 : 0,
    reason: pass ? `Ferramentas conforme esperado (chamadas: ${chamadas.join(", ") || "nenhuma"}).`
                 : `${partes.join("; ")} (chamadas: ${chamadas.join(", ") || "nenhuma"}).`
  };
};
