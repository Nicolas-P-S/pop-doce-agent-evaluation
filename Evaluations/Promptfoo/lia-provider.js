const fs = require("fs");
const path = require("path");

const URL_PADRAO = "https://rm4naioqykxiti2srofnqz6hqa0ctlav.lambda-url.us-east-1.on.aws/";

function somarMetricas(metricas) {
  let entrada = 0, saida = 0, latenciaModelo = 0;
  for (const m of Array.isArray(metricas) ? metricas : []) {
    const u = (m && m.usage) || {};
    entrada += (u.inputTokens || 0) + (u.cacheReadInputTokens || 0) + (u.cacheWriteInputTokens || 0);
    saida += u.outputTokens || 0;
    latenciaModelo += ((m && m.metrics) || {}).latencyMs || 0;
  }
  return { entrada, saida, latenciaModelo };
}

class LiaProvider {
  constructor(options = {}) {
    this.providerId = options.id || "lia-api-multiturno";
    this.config = options.config || {};
    this.versao = this.config.versao || "original";
    this._promptSistema = undefined;
  }

  id() { return this.providerId; }

  carregarPromptSistema() {
    if (this.versao !== "corrigida") return undefined; // original: nunca envia prompt_sistema
    if (this._promptSistema !== undefined) return this._promptSistema;
    const arquivo = this.config.prompt_sistema_arquivo || "prompt_corrigido.txt";
    const achado = [path.resolve(__dirname, arquivo), path.resolve(process.cwd(), arquivo)]
      .find((p) => fs.existsSync(p));
    if (!achado) throw new Error(`Arquivo do prompt corrigido não encontrado: ${arquivo}`);
    this._promptSistema = fs.readFileSync(achado, "utf8");
    return this._promptSistema;
  }

  async callApi(prompt) {
    const apiUrl = process.env.LIA_API_URL || URL_PADRAO;
    const apiKey = process.env.LIA_API_KEY;
    if (!apiKey) return { error: "Configure a variável de ambiente LIA_API_KEY." };

    let promptSistema;
    try { promptSistema = this.carregarPromptSistema(); }
    catch (e) { return { error: e.message }; }

    let input;
    try { input = JSON.parse(String(prompt)); } catch { input = { turnos: [String(prompt)] }; }
    const turnos = Array.isArray(input.turnos) && input.turnos.length
      ? input.turnos : (input.mensagem ? [input.mensagem] : []);
    if (!turnos.length || turnos.some((t) => typeof t !== "string" || !t.trim())) {
      return { error: "Entrada inválida: informe `turnos` como uma lista de mensagens não vazias." };
    }

    let sessao;
    const resultados = [];
    let tIn = 0, tOut = 0, latModelo = 0;
    for (let i = 0; i < turnos.length; i++) {
      const body = { mensagem: turnos[i] };
      if (sessao) body.sessao = sessao;
      if (promptSistema) body.prompt_sistema = promptSistema;

      const inicio = Date.now();
      try {
        const resp = await fetch(apiUrl, {
          method: "POST",
          headers: { "Content-Type": "application/json", "x-api-key": apiKey },
          body: JSON.stringify(body)
        });
        const raw = await resp.text();
        let data;
        try { data = JSON.parse(raw); }
        catch {
          resultados.push({ turno: i + 1, entrada: turnos[i], erro: `Resposta não JSON (HTTP ${resp.status})`,
            detalhe: raw.slice(0, 1000), latenciaMs: Date.now() - inicio, ferramentas: [], metricas: [] });
          break;
        }
        const tok = somarMetricas(data.metricas);
        tIn += tok.entrada; tOut += tok.saida; latModelo += tok.latenciaModelo;
        if (!resp.ok) {
          resultados.push({ turno: i + 1, entrada: turnos[i], erro: `Erro HTTP ${resp.status}`,
            detalhe: JSON.stringify(data).slice(0, 1000), latenciaMs: Date.now() - inicio,
            ferramentas: Array.isArray(data.ferramentas) ? data.ferramentas : [], metricas: data.metricas || [] });
          break;
        }
        if (data.sessao) sessao = data.sessao;
        resultados.push({
          turno: i + 1, entrada: turnos[i], resposta: data.resposta || "", sessao: data.sessao || sessao || "",
          versao: data.versao || "", ferramentas: Array.isArray(data.ferramentas) ? data.ferramentas : [],
          metricas: Array.isArray(data.metricas) ? data.metricas : [],
          tokens: { entrada: tok.entrada, saida: tok.saida }, latenciaMs: Date.now() - inicio
        });
      } catch (e) {
        resultados.push({ turno: i + 1, entrada: turnos[i], erro: `Falha na chamada à API: ${e.message}`,
          latenciaMs: Date.now() - inicio, ferramentas: [], metricas: [] });
        break;
      }
    }

    const versaoApi = resultados.map((t) => t.versao).filter(Boolean).at(-1) || "";
    const metadados = {
      sessao_final: sessao || "",
      versao_solicitada: this.versao,
      versao_api: versaoApi,
      latencia_total_ms: resultados.reduce((s, t) => s + (t.latenciaMs || 0), 0),
      latencia_modelo_ms: latModelo,
      erros: resultados.filter((t) => t.erro).length,
      chamadas: resultados.length,
      tokens_entrada: tIn,
      tokens_saida: tOut,
      tokens_total: tIn + tOut
    };
    const output = {
      case_id: input.case_id || "",
      turnos: resultados,
      transcricao: resultados.map((t) =>
        `Cliente (turno ${t.turno}): ${t.entrada}\nLia: ${t.resposta || "[sem resposta]"}`).join("\n\n"),
      ferramentas_por_turno: resultados.map((t) => ({ turno: t.turno, ferramentas: t.ferramentas })),
      metadados
    };
    const tokenUsage = { total: metadados.tokens_total, prompt: tIn, completion: tOut, numRequests: resultados.length };
    const saida = { output: JSON.stringify(output), tokenUsage, metadata: metadados };

    if (metadados.erros) {
      const primeiro = resultados.find((t) => t.erro);
      return { ...saida, error: `Turno ${primeiro.turno}: ${primeiro.erro}${primeiro.detalhe ? " — " + primeiro.detalhe : ""}` };
    }
    // garante que o prompt corrigido realmente foi aplicado (e que o original nao foi alterado)
    if (versaoApi && versaoApi !== this.versao) {
      return { ...saida, error: `A API respondeu versao="${versaoApi}", mas este provider pede "${this.versao}".` };
    }
    return saida;
  }
}
module.exports = LiaProvider;
